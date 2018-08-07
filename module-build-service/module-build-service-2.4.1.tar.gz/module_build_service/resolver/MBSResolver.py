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
# Written by Martin Curlej <mcurlej@redhat.com>

"""MBS handler functions."""

import logging
import kobo.rpmlib
import requests

from module_build_service import db
from module_build_service import models
from module_build_service.errors import UnprocessableEntity
from module_build_service.resolver.base import GenericResolver

log = logging.getLogger()


class MBSResolver(GenericResolver):

    backend = "mbs"

    def __init__(self, config):
        self.mbs_prod_url = config.mbs_url
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount(self.mbs_prod_url, adapter)

    def _query_from_nsvc(self, name, stream, version=None, context=None, state="ready"):
        """
        Generates dict with MBS params query.

        :param str name: Name of the module to query.
        :param str stream: Stream of the module to query.
        :param str version/int: Version of the module to query.
        :param str context: Context of the module to query.
        """
        query = {
            "name": name,
            "stream": stream,
            "state": state,
            "verbose": True,
            "order_desc_by": "version"
        }
        if version is not None:
            query["version"] = str(version)
        if context is not None:
            query["context"] = context
        return query

    def _get_modules(self, name, stream, version=None, context=None, state="ready", strict=False):
        """
        :param module_info: str, mmd or module dict
        :param strict: Normally this function returns None if no module can be
               found.  If strict=True, then an UnprocessableEntity is raised.

        :return final list of module_info which pass repoclosure
        """
        query = self._query_from_nsvc(name, stream, version, context, state)
        query["page"] = 1
        query["per_page"] = 10
        modules = []

        while True:
            res = self.session.get(self.mbs_prod_url, params=query)
            if not res.ok:
                raise RuntimeError("Failed to query MBS with query %r returned HTTP status %s" %
                                   (query, res.status_code))
                break

            data = res.json()
            modules_per_page = data["items"]
            modules += modules_per_page

            if not data["meta"]["next"]:
                break

            query["page"] += 1

        # Error handling
        if not modules:
            if strict:
                raise UnprocessableEntity("Failed to find module in MBS %r" % query)
            else:
                return None

        return modules

    def _get_module(self, name, stream, version, context, state="ready", strict=False):
        return self._get_modules(name, stream, version, context, state, strict)[0]

    def get_module_modulemds(self, name, stream, version=None, context=None, strict=False):
        """
        Gets the module modulemds from the resolver.
        :param name: a string of the module's name
        :param stream: a string of the module's stream
        :param version: a string or int of the module's version. When None, latest version will
            be returned.
        :param context: a string of the module's context. When None, all contexts will
            be returned.
        :kwarg strict: Normally this function returns [] if no module can be
            found.  If strict=True, then a UnprocessableEntity is raised.
        :return: List of Modulemd metadata instances matching the query
        """
        yaml = None

        local_modules = models.ModuleBuild.local_modules(db.session, name, stream)
        if local_modules:
            return [m.mmd() for m in local_modules]

        modules = self._get_modules(name, stream, version, context, strict=strict)
        if not modules:
            return []

        mmds = []
        for module in modules:
            if module:
                yaml = module['modulemd']

            if not yaml:
                if strict:
                    raise UnprocessableEntity(
                        "Failed to find modulemd entry in MBS for %r" % module)
                else:
                    return None

            mmds.append(self.extract_modulemd(yaml, strict=strict))
        return mmds

    def resolve_profiles(self, mmd, keys):
        """
        :param mmd: ModuleMetadata instance of module
        :param keys: list of modulemd installation profiles to include in
                     the result.
        :return: Dictionary with keys set according to `keys` param and values
                 set to union of all components defined in all installation
                 profiles matching the key using the buildrequires.

        If there are some modules loaded by utils.load_local_builds(...), these
        local modules will be considered when returning the profiles.

        https://pagure.io/fm-orchestrator/issue/181
        """

        results = {}
        for key in keys:
            results[key] = set()
        for module_name, module_info in mmd.get_xmd()['mbs']['buildrequires'].items():
            local_modules = models.ModuleBuild.local_modules(
                db.session, module_name, module_info['stream'])
            if local_modules:
                local_module = local_modules[0]
                log.info("Using local module %r to resolve profiles.",
                         local_module)
                dep_mmd = local_module.mmd()
                for key in keys:
                    if key in dep_mmd.get_profiles().keys():
                        results[key] |= set(dep_mmd.get_profiles()[key].get_rpms().get())
                continue

            # Find the dep in the built modules in MBS
            modules = self._get_modules(
                module_name, module_info['stream'], module_info['version'],
                module_info['context'], strict=True)

            for module in modules:
                yaml = module['modulemd']
                dep_mmd = self.extract_modulemd(yaml)
                # Take note of what rpms are in this dep's profile.
                for key in keys:
                    if key in dep_mmd.get_profiles().keys():
                        results[key] |= set(dep_mmd.get_profiles()[key].get_rpms().get())

        # Return the union of all rpms in all profiles of the given keys.
        return results

    def get_module_build_dependencies(self, name=None, stream=None, version=None, context=None,
                                      mmd=None, strict=False):
        """
        :param name: a module's name (required if mmd is not set)
        :param stream: a module's stream (required if mmd is not set)
        :param version: a module's version (required if mmd is not set)
        :param context: a module's context (required if mmd is not set)
        :param mmd: uses the mmd instead of the name, stream, version
        :param strict: Normally this function returns None if no module can be
            found.  If strict=True, then an UnprocessableEntity is raised.
        :return dict with koji_tag as a key and ModuleMetadata object as value.
        """

        if mmd:
            log.debug("get_module_build_dependencies(mmd=%r strict=%r)" % (mmd, strict))
        elif any(x is None for x in [name, stream, version, context]):
            raise RuntimeError('The name, stream, version, and/or context weren\'t specified')
        else:
            version = str(version)
            log.debug("get_module_build_dependencies(%s, strict=%r)"
                      % (', '.join([name, stream, str(version), context]), strict))

        # This is the set we're going to build up and return.
        module_tags = {}

        if mmd:
            queried_mmd = mmd
        else:
            queried_module = self._get_module(
                name, stream, version, context, strict=strict)
            yaml = queried_module['modulemd']
            queried_mmd = self.extract_modulemd(yaml, strict=strict)

        if (not queried_mmd or not queried_mmd.get_xmd().get('mbs') or
                'buildrequires' not in queried_mmd.get_xmd()['mbs'].keys()):
            raise RuntimeError(
                'The module "{0!r}" did not contain its modulemd or did not have '
                'its xmd attribute filled out in MBS'.format(queried_mmd))

        buildrequires = queried_mmd.get_xmd()['mbs']['buildrequires']
        # Queue up the next tier of deps that we should look at..
        for name, details in buildrequires.items():
            local_modules = models.ModuleBuild.local_modules(
                db.session, name, details['stream'])
            if local_modules:
                for m in local_modules:
                    module_tags[m.koji_tag] = m.mmd()
                continue

            if "context" not in details:
                details["context"] = "00000000"
            modules = self._get_modules(
                name, details['stream'], details['version'],
                details['context'], strict=True)
            for m in modules:
                if m["koji_tag"] in module_tags:
                    continue
                module_tags[m["koji_tag"]] = self.extract_modulemd(m["modulemd"])

        return module_tags

    def resolve_requires(self, requires):
        """
        Takes `requires` dict with module_name as key and module_stream as value.
        Resolves the stream to particular latest version of a module and returns
        new dict in following format:

        {
            "module_name": {
                "ref": module_commit_hash,
                "stream": original_module_stream,
                "version": module_version,
                "filtered_rpms": ["nvr", ...]
            },
            ...
        }

        If there are some modules loaded by utils.load_local_builds(...), these
        local modules will be considered when resolving the requires.

        Raises RuntimeError on MBS lookup error.
        """
        new_requires = {}
        for nsvc in requires:
            nsvc_splitted = nsvc.split(":")
            if len(nsvc_splitted) == 2:
                module_name, module_stream = nsvc_splitted
                module_version = None
                module_context = None
            elif len(nsvc_splitted) == 4:
                module_name, module_stream, module_version, module_context = nsvc_splitted
            else:
                raise ValueError(
                    "Only N:S or N:S:V:C is accepted by resolve_requires, got %s" % nsvc)
            # Try to find out module dependency in the local module builds
            # added by utils.load_local_builds(...).
            local_modules = models.ModuleBuild.local_modules(
                db.session, module_name, module_stream)
            if local_modules:
                local_build = local_modules[0]
                new_requires[module_name] = {
                    # The commit ID isn't currently saved in modules.yaml
                    'ref': None,
                    'stream': local_build.stream,
                    'version': local_build.version,
                    'context': local_build.context,
                    # No need to set filtered_rpms for local builds, because MBS
                    # filters the RPMs automatically when the module build is
                    # done.
                    'filtered_rpms': []
                }
                continue

            commit_hash = None
            version = None
            filtered_rpms = []
            module = self._get_module(
                module_name, module_stream, module_version,
                module_context, strict=True)
            if module.get('modulemd'):
                mmd = self.extract_modulemd(module['modulemd'])
                if mmd.get_xmd().get('mbs') and 'commit' in mmd.get_xmd()['mbs'].keys():
                    commit_hash = mmd.get_xmd()['mbs']['commit']

                # Find out the particular NVR of filtered packages
                if "rpms" in module and mmd.get_rpm_filter().get():
                    for rpm in module["rpms"]:
                        nvr = kobo.rpmlib.parse_nvra(rpm)
                        # If the package is not filtered, continue
                        if not nvr["name"] in mmd.get_rpm_filter().get():
                            continue

                        # If the nvr is already in filtered_rpms, continue
                        nvr = kobo.rpmlib.make_nvr(nvr, force_epoch=True)
                        if nvr in filtered_rpms:
                            continue
                        filtered_rpms.append(nvr)

            if module.get('version'):
                version = module['version']

            if version and commit_hash:
                new_requires[module_name] = {
                    'ref': commit_hash,
                    'stream': module_stream,
                    'version': str(version),
                    'context': module["context"],
                    'filtered_rpms': filtered_rpms,
                }
            else:
                raise RuntimeError(
                    'The module "{0}" didn\'t contain either a commit hash or a'
                    ' version in MBS'.format(module_name))

        return new_requires
