# -*- coding: utf-8 -*-
# Copyright (c) 2018  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Ralph Bean <rbean@redhat.com>
#            Matt Prahl <mprahl@redhat.com>
#            Jan Kaluza <jkaluza@redhat.com>
import re
import time
import shutil
import tempfile
import os
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

from module_build_service import conf, db, log, models, Modulemd
from module_build_service.errors import (
    ValidationError, UnprocessableEntity, Forbidden, Conflict)
from module_build_service import glib
import module_build_service.scm
from .mse import generate_expanded_mmds


def _scm_get_latest(pkg):
    try:
        # If the modulemd specifies that the 'f25' branch is what
        # we want to pull from, we need to resolve that f25 branch
        # to the specific commit available at the time of
        # submission (now).
        pkgref = module_build_service.scm.SCM(
            pkg.get_repository()).get_latest(pkg.get_ref())
    except Exception as e:
        log.exception(e)
        return {'error': "Failed to get the latest commit for %s#%s" % (
            pkg.get_repository(), pkg.get_ref())}

    return {
        'pkg_name': pkg.get_name(),
        'pkg_ref': pkgref,
        'error': None
    }


def format_mmd(mmd, scmurl, session=None):
    """
    Prepares the modulemd for the MBS. This does things such as replacing the
    branches of components with commit hashes and adding metadata in the xmd
    dictionary.
    :param mmd: the ModuleMetadata object to format
    :param scmurl: the url to the modulemd
    """
    # Import it here, because SCM uses utils methods and fails to import
    # them because of dep-chain.
    from module_build_service.scm import SCM

    if not session:
        session = db.session

    xmd = glib.from_variant_dict(mmd.get_xmd())
    if 'mbs' not in xmd:
        xmd['mbs'] = {}
    if 'scmurl' not in xmd['mbs']:
        xmd['mbs']['scmurl'] = scmurl or ''
    if 'commit' not in xmd['mbs']:
        xmd['mbs']['commit'] = ''

    local_modules = models.ModuleBuild.local_modules(session)
    local_modules = {m.name + "-" + m.stream: m for m in local_modules}

    # If module build was submitted via yaml file, there is no scmurl
    if scmurl:
        scm = SCM(scmurl)
        # If a commit hash is provided, add that information to the modulemd
        if scm.commit:
            # We want to make sure we have the full commit hash for consistency
            if SCM.is_full_commit_hash(scm.scheme, scm.commit):
                full_scm_hash = scm.commit
            else:
                full_scm_hash = scm.get_full_commit_hash()

            xmd['mbs']['commit'] = full_scm_hash
        # If a commit hash wasn't provided then just get the latest from master
        else:
            xmd['mbs']['commit'] = scm.get_latest()

    if mmd.get_rpm_components() or mmd.get_module_components():
        if 'rpms' not in xmd['mbs']:
            xmd['mbs']['rpms'] = {}
        # Add missing data in RPM components
        for pkgname, pkg in mmd.get_rpm_components().items():
            if pkg.get_repository() and not conf.rpms_allow_repository:
                raise Forbidden(
                    "Custom component repositories aren't allowed.  "
                    "%r bears repository %r" % (pkgname, pkg.get_repository()))
            if pkg.get_cache() and not conf.rpms_allow_cache:
                raise Forbidden(
                    "Custom component caches aren't allowed.  "
                    "%r bears cache %r" % (pkgname, pkg.cache))
            if not pkg.get_repository():
                pkg.set_repository(conf.rpms_default_repository + pkgname)
            if not pkg.get_cache():
                pkg.set_cache(conf.rpms_default_cache + pkgname)
            if not pkg.get_ref():
                pkg.set_ref('master')

        # Add missing data in included modules components
        for modname, mod in mmd.get_module_components().items():
            if mod.get_repository() and not conf.modules_allow_repository:
                raise Forbidden(
                    "Custom module repositories aren't allowed.  "
                    "%r bears repository %r" % (modname, mod.get_repository()))
            if not mod.get_repository():
                mod.set_repository(conf.modules_default_repository + modname)
            if not mod.get_ref():
                mod.set_ref('master')

        # Check that SCM URL is valid and replace potential branches in pkg refs
        # by real SCM hash and store the result to our private xmd place in modulemd.
        pool = ThreadPool(20)
        pkg_dicts = pool.map(_scm_get_latest, mmd.get_rpm_components().values())
        err_msg = ""
        for pkg_dict in pkg_dicts:
            if pkg_dict["error"]:
                err_msg += pkg_dict["error"] + "\n"
            else:
                pkg_name = pkg_dict["pkg_name"]
                pkg_ref = pkg_dict["pkg_ref"]
                xmd['mbs']['rpms'][pkg_name] = {'ref': pkg_ref}
        if err_msg:
            raise UnprocessableEntity(err_msg)

    # Set the modified xmd back to the modulemd
    mmd.set_xmd(glib.dict_values(xmd))


def validate_mmd(mmd):
    for modname, mod in mmd.get_module_components().items():
        if mod.get_repository() and not conf.modules_allow_repository:
            raise Forbidden(
                "Custom module repositories aren't allowed.  "
                "%r bears repository %r" % (modname, mod.get_repository()))


def merge_included_mmd(mmd, included_mmd):
    """
    Merges two modulemds. This merges only metadata which are needed in
    the `main` when it includes another module defined by `included_mmd`
    """
    included_xmd = glib.from_variant_dict(included_mmd.get_xmd())
    if 'rpms' in included_xmd['mbs']:
        xmd = glib.from_variant_dict(mmd.get_xmd())
        if 'rpms' not in xmd['mbs']:
            xmd['mbs']['rpms'] = included_xmd['mbs']['rpms']
        else:
            xmd['mbs']['rpms'].update(included_xmd['mbs']['rpms'])
    # Set the modified xmd back to the modulemd
    mmd.set_xmd(glib.dict_values(xmd))


def record_component_builds(mmd, module, initial_batch=1,
                            previous_buildorder=None, main_mmd=None, session=None):
    # Imported here to allow import of utils in GenericBuilder.
    import module_build_service.builder

    if not session:
        session = db.session

    # Format the modulemd by putting in defaults and replacing streams that
    # are branches with commit hashes
    format_mmd(mmd, module.scmurl, session=session)

    # When main_mmd is set, merge the metadata from this mmd to main_mmd,
    # otherwise our current mmd is main_mmd.
    if main_mmd:
        # Check for components that are in both MMDs before merging since MBS
        # currently can't handle that situation.
        duplicate_components = [rpm for rpm in main_mmd.get_rpm_components().keys()
                                if rpm in mmd.get_rpm_components()]
        if duplicate_components:
            error_msg = (
                'The included module "{0}" in "{1}" have the following '
                'conflicting components: {2}'.format(
                    mmd.get_name(), main_mmd.get_name(), ', '.join(duplicate_components)))
            raise UnprocessableEntity(error_msg)
        merge_included_mmd(main_mmd, mmd)
    else:
        main_mmd = mmd

    # If the modulemd yaml specifies components, then submit them for build
    rpm_components = mmd.get_rpm_components().values()
    module_components = mmd.get_module_components().values()
    all_components = list(rpm_components) + list(module_components)
    if not all_components:
        return

    rpm_weights = module_build_service.builder.GenericBuilder.get_build_weights(
        [c.get_name() for c in rpm_components])
    all_components.sort(key=lambda x: x.get_buildorder())
    # We do not start with batch = 0 here, because the first batch is
    # reserved for module-build-macros. First real components must be
    # planned for batch 2 and following.
    batch = initial_batch

    for component in all_components:
        # Increment the batch number when buildorder increases.
        if previous_buildorder != component.get_buildorder():
            previous_buildorder = component.get_buildorder()
            batch += 1

        # If the component is another module, we fetch its modulemd file
        # and record its components recursively with the initial_batch
        # set to our current batch, so the components of this module
        # are built in the right global order.
        if isinstance(component, Modulemd.ComponentModule):
            full_url = component.get_repository() + "?#" + component.get_ref()
            # It is OK to whitelist all URLs here, because the validity
            # of every URL have been already checked in format_mmd(...).
            included_mmd = _fetch_mmd(full_url, whitelist_url=True)[0]
            batch = record_component_builds(included_mmd, module, batch,
                                            previous_buildorder, main_mmd, session=session)
            continue

        component_ref = mmd.get_xmd()['mbs']['rpms'][component.get_name()]['ref']
        full_url = component.get_repository() + "?#" + component_ref
        build = models.ComponentBuild(
            module_id=module.id,
            package=component.get_name(),
            format="rpms",
            scmurl=full_url,
            batch=batch,
            ref=component_ref,
            weight=rpm_weights[component.get_name()]
        )
        session.add(build)

    return batch


def submit_module_build_from_yaml(username, handle, stream=None, skiptests=False,
                                  optional_params=None):
    yaml_file = handle.read()
    mmd = load_mmd(yaml_file)

    # Mimic the way how default values are generated for modules that are stored in SCM
    # We can take filename as the module name as opposed to repo name,
    # and also we can take numeric representation of current datetime
    # as opposed to datetime of the last commit
    dt = datetime.utcfromtimestamp(int(time.time()))
    def_name = str(os.path.splitext(os.path.basename(handle.filename))[0])
    def_version = int(dt.strftime("%Y%m%d%H%M%S"))
    mmd.set_name(mmd.get_name() or def_name)
    mmd.set_stream(stream or mmd.get_stream() or "master")
    mmd.set_version(mmd.get_version() or def_version)
    if skiptests:
        buildopts = mmd.get_rpm_buildopts()
        buildopts["macros"] = buildopts.get("macros", "") + "\n\n%__spec_check_pre exit 0\n"
        mmd.set_rpm_buildopts(buildopts)
    return submit_module_build(username, None, mmd, None, optional_params)


_url_check_re = re.compile(r"^[^:/]+:.*$")


def submit_module_build_from_scm(username, url, branch, allow_local_url=False,
                                 optional_params=None):
    # Translate local paths into file:// URL
    if allow_local_url and not _url_check_re.match(url):
        log.info(
            "'{}' is not a valid URL, assuming local path".format(url))
        url = os.path.abspath(url)
        url = "file://" + url
    mmd, scm = _fetch_mmd(url, branch, allow_local_url)

    return submit_module_build(username, url, mmd, scm, optional_params)


def submit_module_build(username, url, mmd, scm, optional_params=None):
    """
    Submits new module build.

    :param str username: Username of the build's owner.
    :param str url: SCM URL of submitted build.
    :param Modulemd.Module mmd: Modulemd defining the build.
    :param scm.SCM scm: SCM class representing the cloned git repo.
    :param dict optional_params: Dict with optional params for a build:
        - "local_build" (bool): The module is being built locally (the MBS is
          not running in infra, but on local developer's machine).
        - "default_streams" (dict): Dict with name:stream mapping defining the stream
          to choose for given module name if multiple streams are available to choose from.
        - Any optional ModuleBuild class field (str).
    :rtype: list with ModuleBuild
    :return: List with submitted module builds.
    """
    import koji  # Placed here to avoid py2/py3 conflicts...

    # For local builds, we want the user to choose the exact stream using the default_streams
    # in case there are multiple streams to choose from and raise an exception otherwise.
    if optional_params and "local_build" in optional_params:
        raise_if_stream_ambigous = True
        del optional_params["local_build"]
    else:
        raise_if_stream_ambigous = False

    # Get the default_streams if set.
    if optional_params and "default_streams" in optional_params:
        default_streams = optional_params["default_streams"]
        del optional_params["default_streams"]
    else:
        default_streams = {}

    validate_mmd(mmd)
    mmds = generate_expanded_mmds(db.session, mmd, raise_if_stream_ambigous, default_streams)
    modules = []

    for mmd in mmds:
        log.debug('Checking whether module build already exists: %s.',
                  ":".join([mmd.get_name(), mmd.get_stream(),
                           str(mmd.get_version()), mmd.get_context()]))
        module = models.ModuleBuild.get_build_from_nsvc(
            db.session, mmd.get_name(), mmd.get_stream(), str(mmd.get_version()),
            mmd.get_context())
        if module:
            if module.state != models.BUILD_STATES['failed']:
                err_msg = ('Module (state=%s) already exists. Only a new build or resubmission of '
                           'a failed build is allowed.' % module.state)
                log.error(err_msg)
                raise Conflict(err_msg)
            if optional_params:
                rebuild_strategy = optional_params.get('rebuild_strategy')
                if rebuild_strategy and module.rebuild_strategy != rebuild_strategy:
                    raise ValidationError(
                        'You cannot change the module\'s "rebuild_strategy" when '
                        'resuming a module build')
            log.debug('Resuming existing module build %r' % module)
            # Reset all component builds that didn't complete
            for component in module.component_builds:
                if component.state and component.state != koji.BUILD_STATES['COMPLETE']:
                    component.state = None
                    component.state_reason = None
                    db.session.add(component)
            module.username = username
            prev_state = module.previous_non_failed_state
            if prev_state == models.BUILD_STATES['init']:
                transition_to = models.BUILD_STATES['init']
            else:
                transition_to = models.BUILD_STATES['wait']
                module.batch = 0
            module.transition(conf, transition_to, "Resubmitted by %s" % username)
            log.info("Resumed existing module build in previous state %s" % module.state)
        else:
            log.debug('Creating new module build')
            module = models.ModuleBuild.create(
                db.session,
                conf,
                name=mmd.get_name(),
                stream=mmd.get_stream(),
                version=str(mmd.get_version()),
                modulemd=mmd.dumps(),
                scmurl=url,
                username=username,
                **(optional_params or {})
            )
            (module.ref_build_context, module.build_context, module.runtime_context,
             module.context) = module.contexts_from_mmd(module.modulemd)

        db.session.add(module)
        db.session.commit()
        modules.append(module)
        log.info("%s submitted build of %s, stream=%s, version=%s, context=%s", username,
                 mmd.get_name(), mmd.get_stream(), mmd.get_version(), mmd.get_context())
    return modules


def _fetch_mmd(url, branch=None, allow_local_url=False, whitelist_url=False):
    # Import it here, because SCM uses utils methods
    # and fails to import them because of dep-chain.
    import module_build_service.scm

    td = None
    scm = None
    try:
        log.debug('Verifying modulemd')
        td = tempfile.mkdtemp()
        if whitelist_url:
            scm = module_build_service.scm.SCM(url, branch, [url], allow_local_url)
        else:
            scm = module_build_service.scm.SCM(url, branch, conf.scmurls, allow_local_url)
        scm.checkout(td)
        scm.verify()
        cofn = scm.get_module_yaml()
        mmd = load_mmd(cofn, is_file=True)
    finally:
        try:
            if td is not None:
                shutil.rmtree(td)
        except Exception as e:
            log.warning(
                "Failed to remove temporary directory {!r}: {}".format(
                    td, str(e)))

    # If the name was set in the modulemd, make sure it matches what the scmurl
    # says it should be
    if mmd.get_name() and mmd.get_name() != scm.name:
        raise ValidationError('The name "{0}" that is stored in the modulemd '
                              'is not valid'.format(mmd.get_name()))
    else:
        mmd.set_name(scm.name)

    # If the stream was set in the modulemd, make sure it matches what the repo
    # branch is
    if mmd.get_stream() and mmd.get_stream() != scm.branch:
        raise ValidationError('The stream "{0}" that is stored in the modulemd '
                              'does not match the branch "{1}"'.format(
                                  mmd.get_stream(), scm.branch))
    else:
        mmd.set_stream(str(scm.branch))

    # If the version is in the modulemd, throw an exception since the version
    # since the version is generated by MBS
    if mmd.get_version():
        raise ValidationError('The version "{0}" is already defined in the '
                              'modulemd but it shouldn\'t be since the version '
                              'is generated based on the commit time'.format(
                                  mmd.get_version()))
    else:
        mmd.set_version(int(scm.version))

    return mmd, scm


def load_mmd(yaml, is_file=False):
    try:
        if is_file:
            mmd = Modulemd.Module().new_from_file(yaml)
        else:
            mmd = Modulemd.Module().new_from_string(yaml)
        # If the modulemd was v1, it will be upgraded to v2
        mmd.upgrade()
    except Exception:
        error = 'The following invalid modulemd was encountered: {0}'.format(yaml)
        log.exception(error)
        raise UnprocessableEntity(error)

    return mmd


def load_local_builds(local_build_nsvs, session=None):
    """
    Loads previously finished local module builds from conf.mock_resultsdir
    and imports them to database.

    :param local_build_nsvs: List of NSV separated by ':' defining the modules
        to load from the mock_resultsdir.
    """
    if not local_build_nsvs:
        return

    if not session:
        session = db.session

    if type(local_build_nsvs) != list:
        local_build_nsvs = [local_build_nsvs]

    # Get the list of all available local module builds.
    builds = []
    try:
        for d in os.listdir(conf.mock_resultsdir):
            m = re.match('^module-(.*)-([^-]*)-([0-9]+)$', d)
            if m:
                builds.append((m.group(1), m.group(2), int(m.group(3)), d))
    except OSError:
        pass

    # Sort with the biggest version first
    try:
        # py27
        builds.sort(lambda a, b: -cmp(a[2], b[2]))  # noqa: F821
    except TypeError:
        # py3
        builds.sort(key=lambda a: a[2], reverse=True)

    for nsv in local_build_nsvs:
        parts = nsv.split(':')
        if len(parts) < 1 or len(parts) > 3:
            raise RuntimeError(
                'The local build "{0}" couldn\'t be be parsed into '
                'NAME[:STREAM[:VERSION]]'.format(nsv))

        name = parts[0]
        stream = parts[1] if len(parts) > 1 else None
        version = int(parts[2]) if len(parts) > 2 else None

        found_build = None
        for build in builds:
            if name != build[0]:
                continue
            if stream is not None and stream != build[1]:
                continue
            if version is not None and version != build[2]:
                continue

            found_build = build
            break

        if not found_build:
            raise RuntimeError(
                'The local build "{0}" couldn\'t be found in "{1}"'.format(
                    nsv, conf.mock_resultsdir))

        # Load the modulemd metadata.
        path = os.path.join(conf.mock_resultsdir, found_build[3], 'results')
        mmd = load_mmd(os.path.join(path, 'modules.yaml'), is_file=True)

        # Create ModuleBuild in database.
        module = models.ModuleBuild.create(
            session,
            conf,
            name=mmd.get_name(),
            stream=mmd.get_stream(),
            version=str(mmd.get_version()),
            context=mmd.get_context(),
            modulemd=mmd.dumps(),
            scmurl="",
            username="mbs",
            publish_msg=False)
        module.koji_tag = path
        module.state = models.BUILD_STATES['ready']
        session.commit()

        if (found_build[0] != module.name or found_build[1] != module.stream or
                str(found_build[2]) != module.version):
            raise RuntimeError(
                'Parsed metadata results for "{0}" don\'t match the directory name'
                .format(found_build[3]))
        log.info("Loaded local module build %r", module)
