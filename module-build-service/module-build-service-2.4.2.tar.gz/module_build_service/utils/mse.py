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
from module_build_service import log, models, Modulemd, conf, db
from module_build_service.errors import StreamAmbigous
from module_build_service.mmd_resolver import MMDResolver
from module_build_service import glib
import module_build_service.resolver


def _expand_mse_streams(session, name, streams, default_streams, raise_if_stream_ambigous):
    """
    Helper method for `expand_mse_stream()` expanding single name:[streams].
    Returns list of expanded streams.

    :param session: SQLAlchemy DB session.
    :param str name: Name of the module which will be expanded.
    :param list streams: List of streams to expand.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    """
    default_streams = default_streams or {}
    # Stream can be prefixed with '-' sign to define that this stream should
    # not appear in a resulting list of streams. There can be two situations:
    # a) all streams have '-' prefix. In this case, we treat list of streams
    #    as blacklist and we find all the valid streams and just remove those with
    #    '-' prefix.
    # b) there is at least one stream without '-' prefix. In this case, we can
    #    ignore all the streams with '-' prefix and just add those without
    #    '-' prefix to the list of valid streams.
    streams_is_blacklist = all(stream.startswith("-") for stream in streams.get())
    if streams_is_blacklist or len(streams.get()) == 0:
        if name in default_streams:
            expanded_streams = [default_streams[name]]
        elif raise_if_stream_ambigous:
            raise StreamAmbigous(
                "There are multiple streams to choose from for module %s." % name)
        else:
            builds = models.ModuleBuild.get_last_build_in_all_streams(
                session, name)
            expanded_streams = [build.stream for build in builds]
    else:
        expanded_streams = []
    for stream in streams.get():
        if stream.startswith("-"):
            if streams_is_blacklist and stream[1:] in expanded_streams:
                expanded_streams.remove(stream[1:])
        else:
            expanded_streams.append(stream)

    if len(expanded_streams) > 1:
        if name in default_streams:
            expanded_streams = [default_streams[name]]
        elif raise_if_stream_ambigous:
            raise StreamAmbigous("There are multiple streams %r to choose from for module %s."
                                 % (expanded_streams, name))

    return expanded_streams


def expand_mse_streams(session, mmd, default_streams=None, raise_if_stream_ambigous=False):
    """
    Expands streams in both buildrequires/requires sections of MMD.

    :param session: SQLAlchemy DB session.
    :param Modulemd.Module mmd: Modulemd metadata with original unexpanded module.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    """
    for deps in mmd.get_dependencies():
        expanded = {}
        for name, streams in deps.get_requires().items():
            streams_set = Modulemd.SimpleSet()
            streams_set.set(_expand_mse_streams(
                session, name, streams, default_streams, raise_if_stream_ambigous))
            expanded[name] = streams_set
        deps.set_requires(expanded)

        expanded = {}
        for name, streams in deps.get_buildrequires().items():
            streams_set = Modulemd.SimpleSet()
            streams_set.set(_expand_mse_streams(
                session, name, streams, default_streams, raise_if_stream_ambigous))
            expanded[name] = streams_set
        deps.set_buildrequires(expanded)


def _get_mmds_from_requires(session, requires, mmds, recursive=False,
                            default_streams=None, raise_if_stream_ambigous=False):
    """
    Helper method for get_mmds_required_by_module_recursively returning
    the list of module metadata objects defined by `requires` dict.

    :param session: SQLAlchemy DB session.
    :param requires: Modulemetadata requires or buildrequires.
    :param mmds: Dictionary with already handled name:streams as a keys and lists
        of resulting mmds as values.
    :param recursive: If True, the requires are checked recursively.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :return: Dict with name:stream as a key and list with mmds as value.
    """
    default_streams = default_streams or {}
    # To be able to call itself recursively, we need to store list of mmds
    # we have added to global mmds list in this particular call.
    added_mmds = {}
    resolver = module_build_service.resolver.GenericResolver.create(conf)

    for name, streams in requires.items():
        streams_to_try = streams.get()
        if name in default_streams:
            streams_to_try = [default_streams[name]]
        elif len(streams_to_try) > 1 and raise_if_stream_ambigous:
            raise StreamAmbigous("There are multiple streams %r to choose from for module %s."
                                 % (streams_to_try, name))

        # For each valid stream, find the last build in a stream and also all
        # its contexts and add mmds of these builds to `mmds` and `added_mmds`.
        # Of course only do that if we have not done that already in some
        # previous call of this method.
        for stream in streams.get():
            ns = "%s:%s" % (name, stream)
            if ns in mmds:
                continue

            mmds[ns] = resolver.get_module_modulemds(name, stream, strict=True)
            added_mmds[ns] = mmds[ns]

    # Get the requires recursively.
    if recursive:
        for mmd_list in added_mmds.values():
            for mmd in mmd_list:
                for deps in mmd.get_dependencies():
                    mmds = _get_mmds_from_requires(session, deps.get_requires(), mmds, True)

    return mmds


def get_mmds_required_by_module_recursively(
        session, mmd, default_streams=None, raise_if_stream_ambigous=False):
    """
    Returns the list of Module metadata objects of all modules required while
    building the module defined by `mmd` module metadata. This presumes the
    module metadata streams are expanded using `expand_mse_streams(...)`
    method.

    This method finds out latest versions of all the build-requires of
    the `mmd` module and then also all contexts of these latest versions.

    For each build-required name:stream:version:context module, it checks
    recursively all the "requires" and finds the latest version of each
    required module and also all contexts of these latest versions.

    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :rtype: list of Modulemd metadata
    :return: List of all modulemd metadata of all modules required to build
        the module `mmd`.
    """
    # We use dict with name:stream as a key and list with mmds as value.
    # That way, we can ensure we won't have any duplicate mmds in a resulting
    # list and we also don't waste resources on getting the modules we already
    # handled from DB.
    mmds = {}

    # At first get all the buildrequires of the module of interest.
    for deps in mmd.get_dependencies():
        mmds = _get_mmds_from_requires(
            session, deps.get_buildrequires(), mmds, False, default_streams,
            raise_if_stream_ambigous)

    # Now get the requires of buildrequires recursively.
    for mmd_key in list(mmds.keys()):
        for mmd in mmds[mmd_key]:
            for deps in mmd.get_dependencies():
                mmds = _get_mmds_from_requires(
                    session, deps.get_requires(), mmds, True, default_streams,
                    raise_if_stream_ambigous)

    # Make single list from dict of lists.
    res = []
    for mmds_list in mmds.values():
        res += mmds_list
    return res


def generate_expanded_mmds(session, mmd, raise_if_stream_ambigous=False, default_streams=None):
    """
    Returns list with MMDs with buildrequires and requires set according
    to module stream expansion rules. These module metadata can be directly
    built using MBS.

    :param session: SQLAlchemy DB session.
    :param Modulemd.Module mmd: Modulemd metadata with original unexpanded module.
    :param bool raise_if_stream_ambigous: When True, raises a StreamAmbigous exception in case
        there are multiple streams for some dependency of module and the module name is not
        defined in `default_streams`, so it is not clear which stream should be used.
    :param dict default_streams: Dict in {module_name: module_stream, ...} format defining
        the default stream to choose for module in case when there are multiple streams to
        choose from.
    """
    if not session:
        session = db.session

    if not default_streams:
        default_streams = {}

    # Create local copy of mmd, because we will expand its dependencies,
    # which would change the module.
    # TODO: Use copy method once its in released libmodulemd:
    # https://github.com/fedora-modularity/libmodulemd/pull/20
    current_mmd = Modulemd.Module.new_from_string(mmd.dumps())

    # MMDResolver expects the input MMD to have no context.
    current_mmd.set_context(None)

    # Expands the MSE streams. This mainly handles '-' prefix in MSE streams.
    expand_mse_streams(session, current_mmd, default_streams, raise_if_stream_ambigous)

    # Get the list of all MMDs which this module can be possibly built against
    # and add them to MMDResolver.
    mmd_resolver = MMDResolver()
    mmds_for_resolving = get_mmds_required_by_module_recursively(
        session, current_mmd, default_streams, raise_if_stream_ambigous)
    for m in mmds_for_resolving:
        mmd_resolver.add_modules(m)

    # Show log.info message with the NSVCs we have added to mmd_resolver.
    nsvcs_to_solve = [
        ":".join([m.get_name(), m.get_stream(), str(m.get_version()), str(m.get_context())])
        for m in mmds_for_resolving]
    log.info("Starting resolving with following input modules: %r", nsvcs_to_solve)

    # Resolve the dependencies between modules and get the list of all valid
    # combinations in which we can build this module.
    requires_combinations = mmd_resolver.solve(current_mmd)
    log.info("Resolving done, possible requires: %r", requires_combinations)

    # This is where we are going to store the generated MMDs.
    mmds = []
    for requires in requires_combinations:
        # Each generated MMD must be new Module object...
        # TODO: Use copy method once its in released libmodulemd:
        # https://github.com/fedora-modularity/libmodulemd/pull/20
        mmd_copy = Modulemd.Module.new_from_string(mmd.dumps())
        xmd = glib.from_variant_dict(mmd_copy.get_xmd())

        # Requires contain the NSVC representing the input mmd.
        # The 'context' of this NSVC defines the id of buildrequires/requires
        # pair in the mmd.get_dependencies().
        dependencies_id = None

        # We don't want to depend on ourselves, so store the NSVC of the current_mmd
        # to be able to ignore it later.
        self_nsvca = None

        # Dict to store name:stream pairs from nsvca, so we are able to access it
        # easily later.
        req_name_stream = {}

        # Get the values for dependencies_id, self_nsvca and req_name_stream variables.
        for nsvca in requires:
            req_name, req_stream, _, req_context, req_arch = nsvca.split(":")
            if req_arch == 'src':
                assert req_name == current_mmd.get_name()
                assert req_stream == current_mmd.get_stream()
                assert dependencies_id is None
                assert self_nsvca is None
                dependencies_id = int(req_context)
                self_nsvca = nsvca
                continue
            req_name_stream[req_name] = req_stream
        if dependencies_id is None or self_nsvca is None:
            raise RuntimeError(
                "%s:%s not found in requires %r" % (
                    current_mmd.get_name(), current_mmd.get_stream(), requires))

        # The name:[streams, ...] pairs do not have to be the same in both
        # buildrequires/requires. In case they are the same, we replace the streams
        # in requires section with a single stream against which we will build this MMD.
        # In case they are not the same, we have to keep the streams as they are in requires
        # section.  We always replace stream(s) for build-requirement with the one we
        # will build this MMD against.
        new_dep = Modulemd.Dependencies()
        dep = mmd_copy.get_dependencies()[dependencies_id]
        dep_requires = dep.get_requires()
        dep_buildrequires = dep.get_buildrequires()
        for req_name, req_streams in dep_requires.items():
            if req_name not in dep_buildrequires:
                # This require is not a buildrequire so just copy this runtime requirement to
                # new_dep and don't touch buildrequires
                new_dep.add_requires(req_name, req_streams.get())
            elif set(req_streams.get()) != set(dep_buildrequires[req_name].get()):
                # Streams in runtime section are not the same as in buildtime section,
                # so just copy this runtime requirement to new_dep.
                new_dep.add_requires(req_name, req_streams.get())
                new_dep.add_buildrequires(req_name, [req_name_stream[req_name]])
            else:
                # This runtime requirement has the same streams in both runtime/buildtime
                # requires sections, so replace streams in both sections by the one we
                # really used in this resolved variant.
                new_dep.add_requires(req_name, [req_name_stream[req_name]])
                new_dep.add_buildrequires(req_name, [req_name_stream[req_name]])
        mmd_copy.set_dependencies((new_dep, ))

        # The Modulemd.Dependencies() stores only streams, but to really build this
        # module, we need NSVC of buildrequires, so we have to store this data in XMD.
        # We also need additional data like for example list of filtered_rpms. We will
        # get them using module_build_service.resolver.GenericResolver.resolve_requires,
        # so prepare list with NSVCs of buildrequires as an input for this method.
        br_list = []
        for nsvca in requires:
            if nsvca == self_nsvca:
                continue
            # Remove the arch from nsvca
            nsvc = ":".join(nsvca.split(":")[:-1])
            br_list.append(nsvc)

        # Resolve the buildrequires and store the result in XMD.
        if 'mbs' not in xmd:
            xmd['mbs'] = {}
        resolver = module_build_service.resolver.GenericResolver.create(conf)
        xmd['mbs']['buildrequires'] = resolver.resolve_requires(br_list)
        xmd['mbs']['mse'] = True

        mmd_copy.set_xmd(glib.dict_values(xmd))

        # Now we have all the info to actually compute context of this module.
        ref_build_context, build_context, runtime_context, context = \
            models.ModuleBuild.contexts_from_mmd(mmd_copy.dumps())
        mmd_copy.set_context(context)

        mmds.append(mmd_copy)

    return mmds
