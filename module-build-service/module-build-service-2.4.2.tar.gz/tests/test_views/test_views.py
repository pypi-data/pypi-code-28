# Copyright (c) 2016  Red Hat, Inc.
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
# Written by Matt Prahl <mprahl@redhat.com>

import json

import module_build_service.scm

from mock import patch, PropertyMock, Mock
from shutil import copyfile
from os import path, mkdir
from os.path import dirname
from requests.utils import quote
import hashlib
import pytest

from tests import app, init_data, clean_database, reuse_component_init_data
from module_build_service.errors import UnprocessableEntity
from module_build_service.models import ModuleBuild
from module_build_service import db, version, Modulemd
import module_build_service.config as mbs_config
import module_build_service.scheduler.handlers.modules


user = ('Homer J. Simpson', set(['packager']))
other_user = ('some_other_user', set(['packager']))
anonymous_user = ('anonymous', set(['packager']))
base_dir = dirname(dirname(__file__))


class FakeSCM(object):
    def __init__(self, mocked_scm, name, mmd_filenames, commit=None, checkout_raise=False,
                 get_latest_raise=False):
        """
        Adds default testing checkout, get_latest and name methods
        to mocked_scm SCM class.

        :param mmd_filenames: List of ModuleMetadata yaml files which
        will be checkouted by the SCM class in the same order as they
        are stored in the list.
        """
        self.mocked_scm = mocked_scm
        self.name = name
        self.commit = commit
        if not isinstance(mmd_filenames, list):
            mmd_filenames = [mmd_filenames]
        self.mmd_filenames = mmd_filenames
        self.checkout_id = 0
        self.sourcedir = None

        if checkout_raise:
            self.mocked_scm.return_value.checkout.side_effect = \
                UnprocessableEntity(
                    "checkout: The requested commit hash was not found within "
                    "the repository. Perhaps you forgot to push. The original "
                    "message was: ")
        else:
            self.mocked_scm.return_value.checkout = self.checkout

        self.mocked_scm.return_value.name = self.name
        self.mocked_scm.return_value.commit = self.commit
        if get_latest_raise:
            self.mocked_scm.return_value.get_latest.side_effect = \
                UnprocessableEntity("Failed to get_latest commit")
        else:
            self.mocked_scm.return_value.get_latest = self.get_latest
        self.mocked_scm.return_value.repository_root = "git://pkgs.stg.fedoraproject.org/modules/"
        self.mocked_scm.return_value.branch = 'master'
        self.mocked_scm.return_value.sourcedir = self.sourcedir
        self.mocked_scm.return_value.get_module_yaml = self.get_module_yaml

    def checkout(self, temp_dir):
        try:
            mmd_filename = self.mmd_filenames[self.checkout_id]
        except Exception:
            mmd_filename = self.mmd_filenames[0]

        self.sourcedir = path.join(temp_dir, self.name)
        mkdir(self.sourcedir)
        base_dir = path.abspath(path.dirname(__file__))
        copyfile(path.join(base_dir, '..', 'staged_data', mmd_filename),
                 self.get_module_yaml())

        self.checkout_id += 1

        return self.sourcedir

    def get_latest(self, ref='master'):
        return hashlib.sha1(ref.encode('utf-8')).hexdigest()[:10]

    def get_module_yaml(self):
        return path.join(self.sourcedir, self.name + ".yaml")


class TestViews:
    def setup_method(self, test_method):
        self.client = app.test_client()
        init_data(2)

    def test_query_build(self):
        rv = self.client.get('/module-build-service/1/module-builds/2')
        data = json.loads(rv.data)
        assert data['id'] == 2
        assert data['context'] == '00000000'
        assert data['name'] == 'nginx'
        assert data['owner'] == 'Moe Szyslak'
        assert data['stream'] == '1'
        assert data['siblings'] == []
        assert data['state'] == 5
        assert data['state_reason'] is None
        assert data['tasks'] == {
            'rpms': {
                'module-build-macros': {
                    'task_id': 12312321,
                    'state': 1,
                    'state_reason': None,
                    'nvr': 'module-build-macros-01-1.module+2+b8661ee4',
                },
                'nginx': {
                    'task_id': 12312345,
                    'state': 1,
                    'state_reason': None,
                    'nvr': 'nginx-1.10.1-2.module+2+b8661ee4',
                },
            },
        }
        assert data['time_completed'] == '2016-09-03T11:25:32Z'
        assert data['time_modified'] == '2016-09-03T11:25:32Z'
        assert data['time_submitted'] == '2016-09-03T11:23:20Z'
        assert data['rebuild_strategy'] == 'changed-and-after'
        assert data['version'] == '2'

    @pytest.mark.parametrize('api_version', [0, 99])
    def test_query_builds_invalid_api_version(self, api_version):
        rv = self.client.get('/module-build-service/{0}/module-builds/'.format(api_version))
        data = json.loads(rv.data)
        assert data['error'] == 'Not Found'
        assert data['message'] == 'The requested API version is not available'
        assert data['status'] == 404

    def test_query_build_short(self):
        rv = self.client.get('/module-build-service/1/module-builds/2?short=True')
        data = json.loads(rv.data)
        assert data['id'] == 2
        assert data['context'] == '00000000'
        assert data['name'] == 'nginx'
        assert data['state'] == 5
        assert data['state_name'] == 'ready'
        assert data['stream'] == '1'
        assert data['version'] == '2'

    def test_query_build_with_verbose_mode(self):
        rv = self.client.get('/module-build-service/1/module-builds/2?verbose=true')
        data = json.loads(rv.data)
        assert data['component_builds'] == [1, 2]
        assert data['context'] == '00000000'
        # There is no xmd information on this module, so these values should be None
        assert data['build_context'] is None
        assert data['runtime_context'] is None
        assert data['id'] == 2
        with open(path.join(base_dir, "staged_data", "nginx_mmd.yaml")) as mmd:
            assert data['modulemd'] == mmd.read()
        assert data['name'] == 'nginx'
        assert data['owner'] == 'Moe Szyslak'
        assert data['scmurl'] == ('git://pkgs.domain.local/modules/nginx'
                                  '?#ba95886c7a443b36a9ce31abda1f9bef22f2f8c9')
        assert data['siblings'] == []
        assert data['state'] == 5
        assert data['state_name'] == 'ready'
        assert data['state_reason'] is None
        # State trace is empty because we directly created these builds and didn't have them
        # transition, which creates these entries
        assert data['state_trace'] == []
        assert data['state_url'] == '/module-build-service/1/module-builds/2'
        assert data['stream'] == '1'
        assert data['tasks'] == {
            'rpms': {
                'module-build-macros': {
                    'task_id': 12312321,
                    'state': 1,
                    'state_reason': None,
                    'nvr': 'module-build-macros-01-1.module+2+b8661ee4',
                },
                'nginx': {
                    'task_id': 12312345,
                    'state': 1,
                    'state_reason': None,
                    'nvr': 'nginx-1.10.1-2.module+2+b8661ee4',
                },
            },
        }
        assert data['time_completed'] == u'2016-09-03T11:25:32Z'
        assert data['time_modified'] == u'2016-09-03T11:25:32Z'
        assert data['time_submitted'] == u'2016-09-03T11:23:20Z'
        assert data['version'] == '2'
        assert data['rebuild_strategy'] == 'changed-and-after'
        assert data['siblings'] == []

    def test_pagination_metadata(self):
        rv = self.client.get('/module-build-service/1/module-builds/?per_page=2&page=2')
        meta_data = json.loads(rv.data)['meta']
        assert meta_data['prev'].split('?', 1)[1] in ['per_page=2&page=1', 'page=1&per_page=2']
        assert meta_data['next'].split('?', 1)[1] in ['per_page=2&page=3', 'page=3&per_page=2']
        assert meta_data['last'].split('?', 1)[1] in ['per_page=2&page=4', 'page=4&per_page=2']
        assert meta_data['first'].split('?', 1)[1] in ['per_page=2&page=1', 'page=1&per_page=2']
        assert meta_data['total'] == 7
        assert meta_data['per_page'] == 2
        assert meta_data['pages'] == 4
        assert meta_data['page'] == 2

    def test_pagination_metadata_with_args(self):
        rv = self.client.get('/module-build-service/1/module-builds/?per_page=2&page=2&order_by=id')
        meta_data = json.loads(rv.data)['meta']
        for link in [meta_data['prev'], meta_data['next'], meta_data['last'], meta_data['first']]:
            assert 'order_by=id' in link
            assert 'per_page=2' in link
        assert meta_data['total'] == 7
        assert meta_data['per_page'] == 2
        assert meta_data['pages'] == 4
        assert meta_data['page'] == 2

    def test_query_builds(self):
        rv = self.client.get('/module-build-service/1/module-builds/?per_page=2')
        items = json.loads(rv.data)['items']
        expected = [
            {
                "component_builds": [11, 12],
                "context": "00000000",
                "id": 7,
                "koji_tag": None,
                "name": "testmodule",
                "owner": "some_other_user",
                "rebuild_strategy": "changed-and-after",
                "scmurl": ("git://pkgs.domain.local/modules/testmodule"
                           "?#ca95886c7a443b36a9ce31abda1f9bef22f2f8c9"),
                "siblings": [],
                "state": 1,
                "state_name": "wait",
                "state_reason": None,
                "stream": "4.3.43",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+7+f95651e2",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383994
                        },
                        "rubygem-rails": {
                            "nvr": "postgresql-9.5.3-4.module+7+f95651e2",
                            "state": 3,
                            "state_reason": None,
                            "task_id": 2433434
                        }
                    }
                },
                "time_completed": None,
                "time_modified": "2016-09-03T12:38:40Z",
                "time_submitted": "2016-09-03T12:38:33Z",
                "version": "7"
            },
            {
                "component_builds": [9, 10],
                "context": "00000000",
                "id": 6,
                "koji_tag": "module-postgressql-1.2",
                "name": "postgressql",
                "owner": "some_user",
                "rebuild_strategy": "changed-and-after",
                "scmurl": ("git://pkgs.domain.local/modules/postgressql"
                           "?#aa95886c7a443b36a9ce31abda1f9bef22f2f8c9"),
                "siblings": [],
                "state": 3,
                "state_name": "done",
                "state_reason": None,
                "stream": "1",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+6+fa947d31",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383994
                        },
                        "postgresql": {
                            "nvr": "postgresql-9.5.3-4.module+6+fa947d31",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 2433434
                        }
                    }
                },
                "time_completed": "2016-09-03T11:37:19Z",
                "time_modified": "2016-09-03T12:37:19Z",
                "time_submitted": "2016-09-03T12:35:33Z",
                "version": "3"
            }
        ]

        assert items == expected

    def test_query_builds_with_context(self):
        clean_database()
        init_data(2, contexts=True)
        rv = self.client.get('/module-build-service/1/module-builds/?context=3a4057d2')
        items = json.loads(rv.data)['items']
        expected = [
            {
                "component_builds": [3, 4],
                "context": "3a4057d2",
                "id": 3,
                "koji_tag": "module-nginx-1.2",
                "name": "nginx",
                "owner": "Moe Szyslak",
                "rebuild_strategy": "changed-and-after",
                "scmurl": ("git://pkgs.domain.local/modules/nginx"
                           "?#ba95886c7a443b36a9ce31abda1f9bef22f2f8c9"),
                "siblings": [2],
                "state": 5,
                "state_name": "ready",
                "state_reason": None,
                "stream": "0",
                "tasks": {
                    "rpms": {
                        "module-build-macros": {
                            "nvr": "module-build-macros-01-1.module+4+0557c87d",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 47383993
                        },
                        "postgresql": {
                            "nvr": "postgresql-9.5.3-4.module+4+0557c87d",
                            "state": 1,
                            "state_reason": None,
                            "task_id": 2433433
                        }
                    }
                },
                "time_completed": "2016-09-03T11:25:32Z",
                "time_modified": "2016-09-03T11:25:32Z",
                "time_submitted": "2016-09-03T11:23:20Z",
                "version": "2"
            }
        ]
        assert items == expected

    def test_query_builds_with_id_error(self):
        rv = self.client.get('/module-build-service/1/module-builds/?id=1')
        actual = json.loads(rv.data)
        msg = ('The "id" query option is invalid. Did you mean to go to '
               '"/module-build-service/1/module-builds/1"?')
        expected = {
            'error': 'Bad Request',
            'message': msg,
            "status": 400
        }
        assert actual == expected

    def test_query_builds_with_nsvc(self):
        nsvcs = ["testmodule:4.3.43:7:00000000",
                 "testmodule:4.3.43:7",
                 "testmodule:4.3.43",
                 "testmodule"]

        results = []
        for nsvc in nsvcs:
            rv = self.client.get('/module-build-service/1/module-builds/?nsvc=%s&per_page=2' % nsvc)
            results.append(json.loads(rv.data)['items'])

        nsvc_keys = ["name", "stream", "version", "context"]

        for items, nsvc in zip(results, nsvcs):
            nsvc_parts = nsvc.split(":")
            for item in items:
                for key, part in zip(nsvc_keys, nsvc_parts):
                    assert item[key] == part

    @patch("module_build_service.builder.KojiModuleBuilder.KojiModuleBuilder.get_session")
    def test_query_builds_with_binary_rpm(self, mock_get_session):
        """
        Test for querying MBS with the binary rpm filename. MBS should return all the modules,
        which contain the rpm.
        """
        # update database with builds which contain koji tags.
        reuse_component_init_data()
        mock_rpm_md = {"build_id": 1065871}
        mock_tags = [{"name": "module-testmodule-master-20170219191323-c40c156c"},
                     {"name": "module-testmodule-master-20170219191323-c40c156c-build"},
                     {"name": "non-module-tag"},
                     {"name": "module-testmodule-master-20170109091357-78e4a6fd"}]

        mock_session = Mock()
        mock_session.getRPM.return_value = mock_rpm_md
        mock_session.listTags.return_value = mock_tags
        mock_get_session.return_value = mock_session

        rpm = quote('module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm')
        rv = self.client.get('/module-build-service/1/module-builds/?rpm=%s' % rpm)
        results = json.loads(rv.data)['items']

        assert len(results) == 2
        assert results[0]["koji_tag"] == "module-testmodule-master-20170219191323-c40c156c"
        assert results[1]["koji_tag"] == "module-testmodule-master-20170109091357-78e4a6fd"

        mock_session.getRPM.assert_called_once_with(
            "module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm")
        mock_session.listTags.assert_called_once_with(mock_rpm_md["build_id"])

    @patch('module_build_service.config.Config.system',
           new_callable=PropertyMock, return_value="invalid_builder")
    def test_query_builds_with_binary_rpm_not_koji(self, mock_builder):
        rpm = quote('module-build-macros-0.1-1.testmodule_master_20170303190726.src.rpm')
        rv = self.client.get('/module-build-service/1/module-builds/?rpm=%s' % rpm)
        results = json.loads(rv.data)
        expected_error = {
            'error': 'Bad Request',
            'message': 'Configured builder does not allow to search by rpm binary name!',
            'status': 400
        }
        assert rv.status_code == 400
        assert results == expected_error

    def test_query_component_build(self):
        rv = self.client.get('/module-build-service/1/component-builds/1')
        data = json.loads(rv.data)
        assert data['id'] == 1
        assert data['format'] == 'rpms'
        assert data['module_build'] == 2
        assert data['nvr'] == 'nginx-1.10.1-2.module+2+b8661ee4'
        assert data['package'] == 'nginx'
        assert data['state'] == 1
        assert data['state_name'] == 'COMPLETE'
        assert data['state_reason'] is None
        assert data['task_id'] == 12312345

    def test_query_component_build_short(self):
        rv = self.client.get('/module-build-service/1/component-builds/1?short=True')
        data = json.loads(rv.data)
        assert data['id'] == 1
        assert data['format'] == 'rpms'
        assert data['module_build'] == 2
        assert data['nvr'] == 'nginx-1.10.1-2.module+2+b8661ee4'
        assert data['package'] == 'nginx'
        assert data['state'] == 1
        assert data['state_name'] == 'COMPLETE'
        assert data['state_reason'] is None
        assert data['task_id'] == 12312345

    def test_query_component_build_verbose(self):
        rv = self.client.get('/module-build-service/1/component-builds/3?verbose=true')
        data = json.loads(rv.data)
        assert data['id'] == 3
        assert data['format'] == 'rpms'
        assert data['module_build'] == 3
        assert data['nvr'] == 'postgresql-9.5.3-4.module+3+0557c87d'
        assert data['package'] == 'postgresql'
        assert data['state'] == 1
        assert data['state_name'] == 'COMPLETE'
        assert data['state_reason'] is None
        assert data['task_id'] == 2433433
        assert data['state_trace'][0]['reason'] is None
        assert data['state_trace'][0]['time'] is not None
        assert data['state_trace'][0]['state'] == 1
        assert data['state_trace'][0]['state_name'] == 'wait'
        assert data['state_url'], '/module-build-service/1/component-builds/3'

    def test_query_component_builds_filter_format(self):
        rv = self.client.get('/module-build-service/1/component-builds/'
                             '?format=rpms')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 12

    def test_query_component_builds_filter_ref(self):
        rv = self.client.get('/module-build-service/1/component-builds/'
                             '?ref=this-filter-query-should-return-zero-items')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 0

    def test_query_component_builds_filter_tagged(self):
        rv = self.client.get('/module-build-service/1/component-builds/?tagged=true')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 8

    def test_query_component_builds_filter_nvr(self):
        rv = self.client.get('/module-build-service/1/component-builds/?nvr=nginx-1.10.1-2.'
                             'module%2B2%2Bb8661ee4')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 1

    def test_query_component_builds_filter_task_id(self):
        rv = self.client.get('/module-build-service/1/component-builds/?task_id=12312346')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 1

    def test_query_component_builds_filter_state(self):
        rv = self.client.get('/module-build-service/1/component-builds/?state=3')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_component_builds_filter_multiple_states(self):
        rv = self.client.get('/module-build-service/1/component-builds/?state=3&state=1')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 12

    def test_query_builds_filter_name(self):
        rv = self.client.get('/module-build-service/1/module-builds/?name=nginx')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_koji_tag(self):
        rv = self.client.get('/module-build-service/1/module-builds/?koji_tag=module-nginx-1.2')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_completed_before(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?completed_before=2016-09-03T11:30:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_completed_after(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?completed_after=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 3

    def test_query_builds_filter_submitted_before(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?submitted_before=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_submitted_after(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?submitted_after=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 5

    def test_query_builds_filter_modified_before(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?modified_before=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 1

    def test_query_builds_filter_modified_after(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?modified_after=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 6

    def test_query_builds_filter_owner(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?owner=Moe%20Szyslak')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_state(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?state=3')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 2

    def test_query_builds_filter_multiple_states(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?state=3&state=1')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 4

    def test_query_builds_two_filters(self):
        rv = self.client.get('/module-build-service/1/module-builds/?owner=Moe%20Szyslak'
                             '&modified_after=2016-09-03T11:35:00Z')
        data = json.loads(rv.data)
        assert data['meta']['total'] == 1

    def test_query_builds_filter_nsv(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?name=postgressql&stream=1&version=2')
        data = json.loads(rv.data)
        for item in data['items']:
            assert item['name'] == 'postgressql'
            assert item['stream'] == '1'
            assert item['version'] == '2'
        assert data['meta']['total'] == 1

    def test_query_builds_filter_invalid_date(self):
        rv = self.client.get(
            '/module-build-service/1/module-builds/?modified_after=2016-09-03T12:25:00-05:00')
        data = json.loads(rv.data)
        assert data['error'] == 'Bad Request'
        assert data['message'] == ('An invalid Zulu ISO 8601 timestamp was '
                                   'provided for the \"modified_after\" parameter')
        assert data['status'] == 400

    def test_query_builds_order_by(self):
        build = db.session.query(module_build_service.models.ModuleBuild).filter_by(id=2).one()
        build.name = 'candy'
        db.session.add(build)
        db.session.commit()
        rv = self.client.get('/module-build-service/1/module-builds/?'
                             'per_page=10&order_by=name')
        items = json.loads(rv.data)['items']
        assert items[0]['name'] == 'candy'
        assert items[1]['name'] == 'nginx'

    def test_query_builds_order_desc_by(self):
        rv = self.client.get('/module-build-service/1/module-builds/?'
                             'per_page=10&order_desc_by=id')
        items = json.loads(rv.data)['items']
        # Check that the id is items[0]["id"], items[0]["id"] - 1, ...
        for idx, item in enumerate(items):
            assert item["id"] == items[0]["id"] - idx

    def test_query_builds_order_desc_by_context(self):
        clean_database()
        init_data(2, contexts=True)

        rv = self.client.get('/module-build-service/1/module-builds/?'
                             'per_page=10&name=nginx&order_desc_by=context')
        sorted_items = json.loads(rv.data)['items']
        sorted_contexts = [m['context'] for m in sorted_items]

        expected_contexts = ['d5a6c0fa', '795e97c1', '3a4057d2', '10e50d06']
        assert sorted_contexts == expected_contexts

    def test_query_builds_order_by_order_desc_by(self):
        """
        Test that when both order_by and order_desc_by is set,
        we prefer order_desc_by.
        """
        rv = self.client.get('/module-build-service/1/module-builds/?'
                             'per_page=10&order_desc_by=id&order_by=name')
        items = json.loads(rv.data)['items']
        # Check that the id is items[0]["id"], items[0]["id"] - 1, ...
        for idx, item in enumerate(items):
            assert item["id"] == items[0]["id"] - idx

    def test_query_builds_order_by_wrong_key(self):
        rv = self.client.get('/module-build-service/1/module-builds/?'
                             'per_page=10&order_by=unknown')
        data = json.loads(rv.data)
        assert data['status'] == 400
        assert data['error'] == 'Bad Request'
        assert data['message'] == 'An invalid order_by or order_desc_by key was supplied'

    @pytest.mark.parametrize('api_version', [1, 2])
    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build(self, mocked_scm, mocked_get_user, api_version):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        post_url = '/module-build-service/{0}/module-builds/'.format(api_version)
        rv = self.client.post(post_url, data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)

        if api_version >= 2:
            assert isinstance(data, list)
            assert len(data) == 1
            data = data[0]

        assert 'component_builds' in data, data
        assert data['component_builds'] == []
        assert data['name'] == 'testmodule'
        assert data['scmurl'] == ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git'
                                  '?#68931c90de214d9d13feefbd35246a81b6cb8d49')
        assert data['version'] == '1'
        assert data['time_submitted'] is not None
        assert data['time_modified'] is not None
        assert data['time_completed'] is None
        assert data['stream'] == 'master'
        assert data['owner'] == 'Homer J. Simpson'
        assert data['id'] == 8
        assert data['rebuild_strategy'] == 'changed-and-after'
        assert data['state_name'] == 'init'
        assert data['state_url'] == '/module-build-service/{0}/module-builds/8'.format(api_version)
        assert len(data['state_trace']) == 1
        assert data['state_trace'][0]['state'] == 0
        assert data['tasks'] == {}
        assert data['siblings'] == []
        mmd = Modulemd.Module().new_from_string(data['modulemd'])
        mmd.upgrade()

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    @patch('module_build_service.config.Config.rebuild_strategy_allow_override',
           new_callable=PropertyMock, return_value=True)
    def test_submit_build_rebuild_strategy(self, mocked_rmao, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'rebuild_strategy': 'only-changed',
             'scmurl': ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git?'
                        '#68931c90de214d9d13feefbd35246a81b6cb8d49')}))
        data = json.loads(rv.data)
        assert data['rebuild_strategy'] == 'only-changed'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    @patch('module_build_service.config.Config.rebuild_strategies_allowed',
           new_callable=PropertyMock, return_value=['all'])
    @patch('module_build_service.config.Config.rebuild_strategy_allow_override',
           new_callable=PropertyMock, return_value=True)
    def test_submit_build_rebuild_strategy_not_allowed(self, mock_rsao, mock_rsa, mocked_scm,
                                                       mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'rebuild_strategy': 'only-changed',
             'scmurl': ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git?'
                        '#68931c90de214d9d13feefbd35246a81b6cb8d49')}))
        data = json.loads(rv.data)
        assert rv.status_code == 400
        expected_error = {
            'error': 'Bad Request',
            'message': ('The rebuild method of "only-changed" is not allowed. Choose from: all.'),
            'status': 400
        }
        assert data == expected_error

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_dep_not_present(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule-no-deps.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master',
             'scmurl': ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git?'
                        '#68931c90de214d9d13feefbd35246a81b6cb8d49')}))
        data = json.loads(rv.data)
        assert rv.status_code == 422
        expected_error = {
            'error': 'Unprocessable Entity',
            'message': 'Cannot find any module builds for chineese_food:good',
            'status': 422
        }
        assert data == expected_error

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_rebuild_strategy_override_not_allowed(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'rebuild_strategy': 'only-changed',
             'scmurl': ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git?'
                        '#68931c90de214d9d13feefbd35246a81b6cb8d49')}))
        data = json.loads(rv.data)
        assert rv.status_code == 400
        expected_error = {
            'error': 'Bad Request',
            'message': ('The request contains the "rebuild_strategy" parameter but overriding '
                        'the default isn\'t allowed'),
            'status': 400
        }
        assert data == expected_error

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_componentless_build(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'fakemodule', 'fakemodule.yaml',
                '3da541559918a808c2402bba5012f6c60b27661c')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)

        assert data['component_builds'] == []
        assert data['name'] == 'fakemodule'
        assert data['scmurl'] == ('git://pkgs.stg.fedoraproject.org/modules/testmodule.git'
                                  '?#68931c90de214d9d13feefbd35246a81b6cb8d49')
        assert data['version'] == '1'
        assert data['time_submitted'] is not None
        assert data['time_modified'] is not None
        assert data['time_completed'] is None
        assert data['stream'] == 'master'
        assert data['owner'] == 'Homer J. Simpson'
        assert data['id'] == 8
        assert data['state_name'] == 'init'
        assert data['rebuild_strategy'] == 'changed-and-after'

    def test_submit_build_auth_error(self):
        base_dir = path.abspath(path.dirname(__file__))
        client_secrets = path.join(base_dir, "client_secrets.json")
        with patch.dict('module_build_service.app.config', {'OIDC_CLIENT_SECRETS': client_secrets}):
            rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
                {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                    'testmodule.git?#48931b90de214d9d13feefbd35246a81b6cb8d49'}))
            data = json.loads(rv.data)
            assert data['message'] == "No 'authorization' header found."
            assert data['status'] == 401
            assert data['error'] == 'Unauthorized'

    @patch('module_build_service.auth.get_user', return_value=user)
    def test_submit_build_scm_url_error(self, mocked_get_user):
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://badurl.com'}))
        data = json.loads(rv.data)
        assert data['message'] == 'The submitted scmurl git://badurl.com is not allowed'
        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=user)
    def test_submit_build_scm_url_without_hash(self, mocked_get_user):
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git'}))
        data = json.loads(rv.data)
        assert data['message'] == ('The submitted scmurl git://pkgs.stg.fedoraproject.org'
                                   '/modules/testmodule.git is not valid')
        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_bad_modulemd(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, "bad", "bad.yaml")

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)
        assert data['message'].startswith('The following invalid modulemd was encountered') is True
        assert data['status'] == 422
        assert data['error'] == 'Unprocessable Entity'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_includedmodule_custom_repo_not_allowed(self,
                                                                 mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, "includedmodules", ["includedmodules.yaml",
                                                "testmodule.yaml"])
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)

        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=other_user)
    def test_cancel_build(self, mocked_get_user):
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'state': 'failed'}))
        data = json.loads(rv.data)

        assert data['state'] == 4
        assert data['state_reason'] == 'Canceled by some_other_user.'

    @patch('module_build_service.auth.get_user', return_value=other_user)
    def test_cancel_build_already_failed(self, mocked_get_user):
        module = ModuleBuild.query.filter_by(id=7).one()
        module.state = 4
        db.session.add(module)
        db.session.commit()
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'state': 'failed'}))
        data = json.loads(rv.data)

        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=('sammy', set()))
    def test_cancel_build_unauthorized_no_groups(self, mocked_get_user):
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'state': 'failed'}))
        data = json.loads(rv.data)

        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=('sammy', set(["packager"])))
    def test_cancel_build_unauthorized_not_owner(self, mocked_get_user):
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'state': 'failed'}))
        data = json.loads(rv.data)

        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user',
           return_value=('sammy', set(["packager", "mbs-admin"])))
    def test_cancel_build_admin(self, mocked_get_user):
        with patch("module_build_service.config.Config.admin_groups",
                   new_callable=PropertyMock, return_value=set(["mbs-admin"])):
            rv = self.client.patch('/module-build-service/1/module-builds/7',
                                   data=json.dumps({'state': 'failed'}))
            data = json.loads(rv.data)

            assert data['state'] == 4
            assert data['state_reason'] == 'Canceled by sammy.'

    @patch('module_build_service.auth.get_user',
           return_value=('sammy', set(["packager"])))
    def test_cancel_build_no_admin(self, mocked_get_user):
        with patch("module_build_service.config.Config.admin_groups",
                   new_callable=PropertyMock, return_value=set(["mbs-admin"])):
            rv = self.client.patch('/module-build-service/1/module-builds/7',
                                   data=json.dumps({'state': 'failed'}))
            data = json.loads(rv.data)

            assert data['status'] == 403
            assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=other_user)
    def test_cancel_build_wrong_param(self, mocked_get_user):
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'some_param': 'value'}))
        data = json.loads(rv.data)

        assert data['status'] == 400
        assert data['error'] == 'Bad Request'
        assert data['message'] == 'Invalid JSON submitted'

    @patch('module_build_service.auth.get_user', return_value=other_user)
    def test_cancel_build_wrong_state(self, mocked_get_user):
        rv = self.client.patch('/module-build-service/1/module-builds/7',
                               data=json.dumps({'state': 'some_state'}))
        data = json.loads(rv.data)

        assert data['status'] == 400
        assert data['error'] == 'Bad Request'
        assert data['message'] == 'The provided state change is not supported'

    @patch('module_build_service.auth.get_user', return_value=user)
    def test_submit_build_unsupported_scm_scheme(self, mocked_get_user):
        scmurl = 'unsupported://example.com/modules/'
        'testmodule.git?#0000000000000000000000000000000000000000'
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': scmurl}))
        data = json.loads(rv.data)
        assert data['message'] in ("The submitted scmurl {} is not allowed".format(scmurl),
                                   "The submitted scmurl {} is not valid".format(scmurl))
        assert data['status'] == 403
        assert data['error'] == 'Forbidden'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_version_set_error(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule-version-set.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)
        assert data['status'] == 400
        assert data['message'] == ('The version "123456789" is already defined in the modulemd '
                                   'but it shouldn\'t be since the version is generated based on '
                                   'the commit time')
        assert data['error'] == 'Bad Request'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_wrong_stream(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule-wrong-stream.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49'}))
        data = json.loads(rv.data)
        assert data['status'] == 400
        assert data['message'] == ('The stream "wrong_stream" that is stored in the modulemd '
                                   'does not match the branch "master"')
        assert data['error'] == 'Bad Request'

    @patch('module_build_service.auth.get_user', return_value=user)
    def test_submit_build_set_owner(self, mocked_get_user):
        data = {
            'branch': 'master',
            'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                      'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49',
            'owner': 'foo',
        }
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(data))
        result = json.loads(rv.data)
        assert result['status'] == 400
        assert "The request contains 'owner' parameter" in result['message']

    @patch('module_build_service.auth.get_user', return_value=anonymous_user)
    @patch('module_build_service.scm.SCM')
    @patch("module_build_service.config.Config.no_auth", new_callable=PropertyMock,
           return_value=True)
    def test_submit_build_no_auth_set_owner(self, mocked_conf, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        data = {
            'branch': 'master',
            'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                      'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49',
            'owner': 'foo',
        }
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(data))
        result = json.loads(rv.data)

        build = ModuleBuild.query.filter(ModuleBuild.id == result['id']).one()
        assert (build.owner == result['owner'] == 'foo') is True

    @patch('module_build_service.auth.get_user', return_value=anonymous_user)
    @patch('module_build_service.scm.SCM')
    @patch("module_build_service.config.Config.no_auth", new_callable=PropertyMock)
    def test_patch_set_different_owner(self, mocked_no_auth, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        mocked_no_auth.return_value = True
        data = {
            'branch': 'master',
            'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                      'testmodule.git?#68931c90de214d9d13feefbd35246a81b6cb8d49',
            'owner': 'foo',
        }
        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(data))
        r1 = json.loads(rv.data)

        url = '/module-build-service/1/module-builds/' + str(r1['id'])
        r2 = self.client.patch(url, data=json.dumps({'state': 'failed'}))
        assert r2.status_code == 403

        r3 = self.client.patch(url, data=json.dumps({'state': 'failed', 'owner': 'foo'}))
        assert r3.status_code == 200

        mocked_no_auth.return_value = False
        r3 = self.client.patch(url, data=json.dumps({'state': 'failed', 'owner': 'foo'}))
        assert r3.status_code == 400
        assert "The request contains 'owner' parameter" in json.loads(r3.data)['message']

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    def test_submit_build_commit_hash_not_found(self, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '7035bd33614972ac66559ac1fdd019ff6027ad22', checkout_raise=True)

        rv = self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
            {'branch': 'master', 'scmurl': 'git://pkgs.stg.fedoraproject.org/modules/'
                'testmodule.git?#7035bd33614972ac66559ac1fdd019ff6027ad22'}))
        data = json.loads(rv.data)
        assert "The requested commit hash was not found within the repository." in data['message']
        assert "Perhaps you forgot to push. The original message was: " in data['message']
        assert data['status'] == 422
        assert data['error'] == 'Unprocessable Entity'

    @patch('module_build_service.auth.get_user', return_value=user)
    @patch('module_build_service.scm.SCM')
    @patch("module_build_service.config.Config.allow_custom_scmurls", new_callable=PropertyMock)
    def test_submit_custom_scmurl(self, allow_custom_scmurls, mocked_scm, mocked_get_user):
        FakeSCM(mocked_scm, 'testmodule', 'testmodule.yaml',
                '620ec77321b2ea7b0d67d82992dda3e1d67055b4')

        def submit(scmurl):
            return self.client.post('/module-build-service/1/module-builds/', data=json.dumps(
                                    {'branch': 'master', 'scmurl': scmurl}))

        allow_custom_scmurls.return_value = False
        res1 = submit('git://some.custom.url.org/modules/testmodule.git?#68931c9')
        data = json.loads(res1.data)
        assert data['status'] == 403
        assert data['message'].startswith('The submitted scmurl') is True
        assert data['message'].endswith('is not allowed') is True

        allow_custom_scmurls.return_value = True
        res2 = submit('git://some.custom.url.org/modules/testmodule.git?#68931c9')
        assert res2.status_code == 201

    def test_about(self):
        with patch.object(mbs_config.Config, 'auth_method', new_callable=PropertyMock) as auth:
            auth.return_value = 'kerberos'
            rv = self.client.get('/module-build-service/1/about/')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert data == {'auth_method': 'kerberos', 'api_version': 2, 'version': version}

    def test_rebuild_strategy_api(self):
        rv = self.client.get('/module-build-service/1/rebuild-strategies/')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            'items': [
                {
                    'allowed': False,
                    'default': False,
                    'description': 'All components will be rebuilt',
                    'name': 'all'
                },
                {
                    'allowed': True,
                    'default': True,
                    'description': ('All components that have changed and those in subsequent '
                                    'batches will be rebuilt'),
                    'name': 'changed-and-after'
                },
                {
                    'allowed': False,
                    'default': False,
                    'description': 'All changed components will be rebuilt',
                    'name': 'only-changed'
                }
            ]
        }
        assert data == expected

    def test_rebuild_strategy_api_only_changed_default(self):
        with patch.object(mbs_config.Config, 'rebuild_strategy', new_callable=PropertyMock) as r_s:
            r_s.return_value = 'only-changed'
            rv = self.client.get('/module-build-service/1/rebuild-strategies/')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            'items': [
                {
                    'allowed': False,
                    'default': False,
                    'description': 'All components will be rebuilt',
                    'name': 'all'
                },
                {
                    'allowed': False,
                    'default': False,
                    'description': ('All components that have changed and those in subsequent '
                                    'batches will be rebuilt'),
                    'name': 'changed-and-after'
                },
                {
                    'allowed': True,
                    'default': True,
                    'description': 'All changed components will be rebuilt',
                    'name': 'only-changed'
                }
            ]
        }
        assert data == expected

    def test_rebuild_strategy_api_override_allowed(self):
        with patch.object(mbs_config.Config, 'rebuild_strategy_allow_override',
                          new_callable=PropertyMock) as rsao:
            rsao.return_value = True
            rv = self.client.get('/module-build-service/1/rebuild-strategies/')
        data = json.loads(rv.data)
        assert rv.status_code == 200
        expected = {
            'items': [
                {
                    'allowed': True,
                    'default': False,
                    'description': 'All components will be rebuilt',
                    'name': 'all'
                },
                {
                    'allowed': True,
                    'default': True,
                    'description': ('All components that have changed and those in subsequent '
                                    'batches will be rebuilt'),
                    'name': 'changed-and-after'
                },
                {
                    'allowed': True,
                    'default': False,
                    'description': 'All changed components will be rebuilt',
                    'name': 'only-changed'
                }
            ]
        }
        assert data == expected

    def test_cors_header_decorator(self):
        rv = self.client.get('/module-build-service/1/module-builds/')
        assert rv.headers['Access-Control-Allow-Origin'] == '*'
