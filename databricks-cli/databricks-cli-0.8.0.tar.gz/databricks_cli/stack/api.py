# Databricks CLI
# Copyright 2018 Databricks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"), except
# that the use of services to which certain application programming
# interfaces (each, an "API") connect requires that the user first obtain
# a license for the use of the APIs from Databricks, Inc. ("Databricks"),
# by creating an account at www.databricks.com and agreeing to either (a)
# the Community Edition Terms of Service, (b) the Databricks Terms of
# Service, or (c) another written agreement between Licensee and Databricks
# for the use of the APIs.
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from datetime import datetime
import time
import copy

import click

from databricks_cli.jobs.api import JobsApi
from databricks_cli.workspace.api import WorkspaceApi, DIRECTORY, NOTEBOOK
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.workspace.types import WorkspaceLanguage
from databricks_cli.version import version as CLI_VERSION
from databricks_cli.stack.exceptions import StackError

MS_SEC = 1000

# Resource Services
JOBS_SERVICE = 'jobs'
WORKSPACE_SERVICE = 'workspace'
DBFS_SERVICE = 'dbfs'

# Config Outer Fields
STACK_NAME = 'name'
STACK_RESOURCES = 'resources'
STACK_DEPLOYED = 'deployed'

# Resource Fields
RESOURCE_ID = 'id'
RESOURCE_SERVICE = 'service'
RESOURCE_PROPERTIES = 'properties'

# Deployed Resource Fields
RESOURCE_PHYSICAL_ID = 'physical_id'
RESOURCE_DEPLOY_OUTPUT = 'deploy_output'
RESOURCE_DEPLOY_TIMESTAMP = 'timestamp'
CLI_VERSION_KEY = 'cli_version'

# Job Service Properties
JOBS_RESOURCE_NAME = 'name'
JOBS_RESOURCE_JOB_ID = 'job_id'

# Workspace Service Properties
WORKSPACE_RESOURCE_SOURCE_PATH = 'source_path'
WORKSPACE_RESOURCE_PATH = 'path'
WORKSPACE_RESOURCE_OBJECT_TYPE = 'object_type'

# DBFS Service Properties
DBFS_RESOURCE_SOURCE_PATH = 'source_path'
DBFS_RESOURCE_PATH = 'path'
DBFS_RESOURCE_IS_DIR = 'is_dir'


class StackApi(object):
    def __init__(self, api_client):
        self.jobs_client = JobsApi(api_client)
        self.workspace_client = WorkspaceApi(api_client)
        self.dbfs_client = DbfsApi(api_client)

    def deploy(self, config_path, **kwargs):
        """
        Deploys a stack given stack JSON configuration template at path config_path.

        Loads the JSON template as well as status JSON if stack has been deployed before.

        The working directory is changed to that where the JSON template is contained
        so that paths within the stack configuration are relative to the directory of the
        JSON template instead of the directory where this function is called.

        :param config_path: Path to stack JSON configuration template. Must have the fields of
        'name', the name of the stack and 'resources', a list of stack resources.
        :return: None.
        """
        stack_config = self._load_json(config_path)
        status_path = self._generate_stack_status_path(config_path)
        stack_status = self._load_json(status_path)
        config_dir = os.path.dirname(os.path.abspath(config_path))
        cli_dir = os.getcwd()
        os.chdir(config_dir)  # Switch current working directory to where json config is stored
        new_stack_status = self.deploy_config(stack_config, stack_status, **kwargs)
        os.chdir(cli_dir)
        click.echo("Saving stack status to {}".format(status_path))
        self._save_json(status_path, new_stack_status)

    def download(self, config_path, **kwargs):
        """
        Downloads a stack given stack JSON configuration template at path config_path.

        The working directory is changed to that where the JSON template is contained
        so that paths within the stack configuration are relative to the directory of the
        JSON template instead of the directory where this function is called.

        :param config_path: Path to stack JSON configuration template. Must have the fields of
        'name', the name of the stack and 'resources', a list of stack resources.
        :return: None.
        """
        stack_config = self._load_json(config_path)
        config_dir = os.path.dirname(os.path.abspath(config_path))
        cli_dir = os.getcwd()
        os.chdir(config_dir)  # Switch current working directory to where json config is stored
        self.download_from_config(stack_config, **kwargs)
        os.chdir(cli_dir)

    def deploy_config(self, stack_config, stack_status=None, **kwargs):
        """
        Deploys a stack given stack JSON configuration template at path config_path.

        After going through each of the resources and deploying them, stores status JSON
        of deployment with deploy status of each resource deployment.
        For each resource deployment, stack_status is used to get the associated resource status
        of a resource from the last deployment.

        :param stack_config: Must have the fields of
        'name', the name of the stack and 'resources', a list of stack resources.
        :param stack_status: Must have the fields of
        :return:
        """
        click.echo('#' * 80)
        self._validate_config(stack_config)
        if stack_status:
            click.echo('#' * 80)
            self._validate_status(stack_status)
            resource_id_to_status = self._get_resource_to_status_map(stack_status)
        else:
            resource_id_to_status = {}

        stack_name = stack_config.get(STACK_NAME)
        click.echo('#' * 80)
        click.echo('Deploying stack {}'.format(stack_name))

        # List of statuses, One for each resource in stack_config[STACK_RESOURCES]
        resource_statuses = []
        click.echo('#' * 80)
        for resource_config in stack_config.get(STACK_RESOURCES):
            # Retrieve resource deployment info from the last deployment.
            resource_map_key = (resource_config.get(RESOURCE_ID),
                                resource_config.get(RESOURCE_SERVICE))
            resource_status = resource_id_to_status.get(resource_map_key) \
                if resource_map_key in resource_id_to_status else None
            # Deploy resource, get resource_status
            new_resource_status = self._deploy_resource(resource_config, resource_status, **kwargs)
            resource_statuses.append(new_resource_status)
            click.echo('#' * 80)
        # stack deploy status is original config with deployed resource statuses added
        new_stack_status = copy.deepcopy(stack_config)
        new_stack_status.update({STACK_DEPLOYED: resource_statuses})
        new_stack_status.update({CLI_VERSION_KEY: CLI_VERSION})

        # Validate that the status has been created correctly
        self._validate_status(new_stack_status)
        click.echo('#' * 80)

        return new_stack_status

    def download_from_config(self, stack_config, **kwargs):
        """
        Downloads a stack given a dict of the stack configuration.
        :param stack_config: dict of stack configuration. Must contain 'name' and 'resources' field.
        :return: None.
        """
        self._validate_config(stack_config)
        stack_name = stack_config.get(STACK_NAME)
        click.echo('Downloading stack {}'.format(stack_name))

        click.echo('#' * 80)
        for resource_config in stack_config.get(STACK_RESOURCES):
            # Deploy resource, get resource_status
            self._download_resource(resource_config, **kwargs)
            click.echo('#' * 80)

    def _deploy_resource(self, resource_config, resource_status=None, **kwargs):
        """
        Deploys a resource given a resource information extracted from the stack JSON configuration
        template.

        :param resource_config: A dict of the resource with fields of 'id', 'service'
        and 'properties'.
        ex. {'id': 'example-resource', 'service': 'jobs', 'properties': {...}}
        :param resource_status: A dict of the resource's deployment info from the last
        deployment. Will be None if this is the first deployment.
        ex. {'id': 'example-resource', 'service': 'jobs', 'physical_id': {...}}
        :return: dict resource_status- A dictionary of deployment information of the
        resource to be stored at deploy time. It includes the resource id of the resource along
        with the physical id and deploy output of the resource.
        ex. {'id': 'example-resource', 'service': 'jobs', 'physical_id': {'job_id': 123},
        'timestamp': 123456789, 'deploy_output': {..}}
        """
        resource_id = resource_config.get(RESOURCE_ID)
        resource_service = resource_config.get(RESOURCE_SERVICE)
        resource_properties = resource_config.get(RESOURCE_PROPERTIES)
        physical_id = resource_status.get(RESOURCE_PHYSICAL_ID) if resource_status else None

        if resource_service == JOBS_SERVICE:
            click.echo("Deploying job '{}' with properties: \n{}".format(resource_id, json.dumps(
                resource_properties, indent=2, separators=(',', ': '))))
            new_physical_id, deploy_output = self._deploy_job(resource_properties,
                                                              physical_id)
        elif resource_service == WORKSPACE_SERVICE:
            click.echo(
                "Deploying workspace asset '{}' with properties \n{}"
                .format(
                    resource_id, json.dumps(resource_properties, indent=2, separators=(',', ': '))
                )
            )
            overwrite = kwargs.get('overwrite', False)
            new_physical_id, deploy_output = self._deploy_workspace(resource_properties,
                                                                    physical_id,
                                                                    overwrite)
        elif resource_service == DBFS_SERVICE:
            click.echo(
                "Deploying DBFS asset '{}' with properties \n{}".format(
                    resource_id, json.dumps(resource_properties, indent=2, separators=(',', ': '))
                )
            )
            overwrite = kwargs.get('overwrite', False)
            new_physical_id, deploy_output = self._deploy_dbfs(resource_properties,
                                                               physical_id,
                                                               overwrite)
        else:
            raise StackError("Resource service '{}' not supported".format(resource_service))

        new_resource_status = {RESOURCE_ID: resource_id,
                               RESOURCE_SERVICE: resource_service,
                               RESOURCE_DEPLOY_TIMESTAMP:
                                   # Milliseconds since epoch.
                                   int(time.mktime(datetime.now().timetuple()) * MS_SEC),
                               RESOURCE_PHYSICAL_ID: new_physical_id,
                               RESOURCE_DEPLOY_OUTPUT: deploy_output}
        return new_resource_status

    def _download_resource(self, resource_config, **kwargs):
        """
        Downloads a resource given a resource information extracted from the stack JSON
        configuration template.

        :param resource_config: A dict of the resource with fields of 'id', 'service' and
        'properties'.
        ex. {'id': 'example-resource', 'service': 'jobs', 'properties': {...}}
        """
        resource_id = resource_config.get(RESOURCE_ID)
        resource_service = resource_config.get(RESOURCE_SERVICE)
        resource_properties = resource_config.get(RESOURCE_PROPERTIES)

        if resource_service == WORKSPACE_SERVICE:
            click.echo(
                "Downloading workspace asset '{}' with properties \n{}"
                .format(
                    resource_id, json.dumps(resource_properties, indent=2, separators=(',', ': '))
                )
            )
            overwrite = kwargs.get('overwrite', False)
            self._download_workspace(resource_properties, overwrite)
        else:
            click.echo("Resource service '{}' not supported for download. "
                       "skipping.".format(resource_service))

    def _deploy_job(self, resource_properties, physical_id=None):
        """
        Deploys a job resource by either creating a job if the job isn't kept track of through
        the physical_id of the job or updating an existing job. The job is created or updated using
        the the settings specified in the inputted job_settings.

        :param resource_properties: A dict of the Databricks JobSettings data structure
        :param physical_id: A dict object containing 'job_id' field of job identifier in Databricks
        server

        :return: tuple of (physical_id, deploy_output), where physical_id contains a 'job_id' field
        of the physical job_id of the job on databricks. deploy_output is the output of the job
        from databricks when a GET request is called for it.
        """
        job_settings = resource_properties  # resource_properties of jobs are solely job settings.

        if physical_id:
            job_id = physical_id.get(JOBS_RESOURCE_JOB_ID)
            self._update_job(job_settings, job_id)
        else:
            job_id = self._put_job(job_settings)
        click.echo("Job deployed on Databricks with Job ID {}".format(job_id))
        physical_id = {JOBS_RESOURCE_JOB_ID: job_id}
        deploy_output = self.jobs_client.get_job(job_id)
        return physical_id, deploy_output

    def _put_job(self, job_settings):
        """
        Given settings of the job in job_settings, create a new job. For purposes of idempotency
        and to reduce leaked resources in alpha versions of stack deployment, if a job exists
        with the same name, that job will be updated. If multiple jobs are found with the same name,
        the deployment will abort.

        :param job_settings:
        :return: job_id, Physical ID of job on Databricks server.
        """
        job_name = job_settings.get(JOBS_RESOURCE_NAME)
        jobs_same_name = self.jobs_client._list_jobs_by_name(job_name)
        if len(jobs_same_name) > 1:
            raise StackError("Multiple jobs with the same name '{}' already exist, aborting"
                             " stack deployment".format(job_name))
        elif len(jobs_same_name) == 1:
            existing_job = jobs_same_name[0]
            creator_name = existing_job.get('creator_user_name')
            timestamp = existing_job.get('created_time') / MS_SEC  # Convert to readable date.
            date_created = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("Warning: Job exists with same name '{}' created by {} on {}. Job will "
                       "be overwritten".format(job_name, creator_name, date_created))
            # Calling jobs_client.reset_job directly so as to not call same level function.
            self.jobs_client.reset_job({'job_id': existing_job.get('job_id'),
                                        'new_settings': job_settings})
            return existing_job.get('job_id')
        else:
            job_id = self.jobs_client.create_job(job_settings).get('job_id')
            return job_id

    def _update_job(self, job_settings, job_id):
        """
        Given job settings and an existing job_id of a job, update the job settings on databricks.

        :param job_settings: job settings to update the job with.
        :param job_id: physical job_id of job in databricks server.
        """

        self.jobs_client.reset_job({'job_id': job_id, 'new_settings': job_settings})

    def _deploy_workspace(self, resource_properties, physical_id, overwrite):
        """
        Deploy workspace asset.

        :param resource_properties: dict of properties for the workspace asset. Must contain the
        'source_path', 'path' and 'object_type' fields.
        :param physical_id: dict containing physical identifier of workspace asset on databricks.
        Should contain the field 'path'.
        :param overwrite: Whether or not to overwrite the contents of workspace notebooks.
        :return: (dict, dict) of (physical_id, deploy_output). physical_id is the physical ID for
        the stack status that contains the workspace path of the notebook or directory on datbricks.
        deploy_output is the initial information about the asset on databricks at deploy time
        returned by the REST API.
        """
        local_path = resource_properties.get(WORKSPACE_RESOURCE_SOURCE_PATH)
        workspace_path = resource_properties.get(WORKSPACE_RESOURCE_PATH)
        object_type = resource_properties.get(WORKSPACE_RESOURCE_OBJECT_TYPE)

        actual_object_type = DIRECTORY if os.path.isdir(local_path) else NOTEBOOK
        if object_type != actual_object_type:
            raise StackError("Field '{}' ({}) not consistent"
                             "with actual object type ({})".format(WORKSPACE_RESOURCE_OBJECT_TYPE,
                                                                   object_type,
                                                                   actual_object_type))

        click.echo('Uploading {} from {} to Databricks workspace at {}'.format(object_type,
                                                                               local_path,
                                                                               workspace_path))
        if object_type == NOTEBOOK:
            # Inference of notebook language and format
            language_fmt = WorkspaceLanguage.to_language_and_format(local_path)
            if language_fmt is None:
                raise StackError("Workspace notebook language and format cannot be inferred"
                                 "Please check file extension of notebook file.")
            language, fmt = language_fmt
            # Create needed directories in workspace.
            self.workspace_client.mkdirs(os.path.dirname(workspace_path))
            self.workspace_client.import_workspace(local_path, workspace_path, language, fmt,
                                                   overwrite)
        elif object_type == DIRECTORY:
            self.workspace_client.import_workspace_dir(local_path, workspace_path, overwrite,
                                                       exclude_hidden_files=True)
        else:
            # Shouldn't reach here because of verification of object_type above.
            assert False

        if physical_id and physical_id[WORKSPACE_RESOURCE_PATH] != workspace_path:
            # physical_id['path'] is the workspace path from the last deployment. Alert when changed
            click.echo("Workspace asset had path changed from {} to {}"
                       .format(physical_id[WORKSPACE_RESOURCE_PATH], workspace_path))
        new_physical_id = {WORKSPACE_RESOURCE_PATH: workspace_path}
        deploy_output = self.workspace_client.client.get_status(workspace_path)

        return new_physical_id, deploy_output

    def _download_workspace(self, resource_properties, overwrite):
        """
        Download workspace asset.

        :param resource_properties: dict of properties for the workspace asset. Must contain the
        'source_path', 'path' and 'object_type' fields.
        :param overwrite: Whether or not to overwrite the contents of workspace notebooks.
        """
        local_path = resource_properties.get(WORKSPACE_RESOURCE_SOURCE_PATH)
        workspace_path = resource_properties.get(WORKSPACE_RESOURCE_PATH)
        object_type = resource_properties.get(WORKSPACE_RESOURCE_OBJECT_TYPE)
        click.echo('Downloading {} from Databricks path {} to {}'.format(object_type,
                                                                         workspace_path,
                                                                         local_path))
        if object_type == NOTEBOOK:
            # Inference of notebook language and format. A tuple of (language, fmt) or Nonetype.
            language_fmt = WorkspaceLanguage.to_language_and_format(local_path)
            if language_fmt is None:
                raise StackError("Workspace Notebook language and format cannot be inferred."
                                 "Please check file extension of notebook 'source_path'.")
            (_, fmt) = language_fmt
            local_dir = os.path.dirname(os.path.abspath(local_path))
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            self.workspace_client.export_workspace(workspace_path, local_path, fmt, overwrite)
        elif object_type == DIRECTORY:
            self.workspace_client.export_workspace_dir(workspace_path, local_path, overwrite)
        else:
            raise StackError("Invalid value for '{}' field: {}"
                             .format(WORKSPACE_RESOURCE_OBJECT_TYPE, object_type))

    def _deploy_dbfs(self, resource_properties, physical_id, overwrite):
        """
        Deploy dbfs asset.

        :param resource_properties: dict of properties for the dbfs asset. Must contain the
        'source_path', 'path' and 'is_dir' fields.
        :param physical_id: dict containing physical identifier of dbfs asset on Databricks.
        Should contain the field 'path'.
        :param overwrite: Whether or not to overwrite the contents of dbfs files.
        :return: (dict, dict) of (physical_id, deploy_output). physical_id is a dict that
        contains the dbfs path of the file on Databricks.
        ex.{"path":"dbfs:/path/in/dbfs"}
        deploy_output is the initial information about the dbfs asset at deploy time
        returned by the REST API.
        """

        local_path = resource_properties.get(DBFS_RESOURCE_SOURCE_PATH)
        dbfs_path = resource_properties.get(DBFS_RESOURCE_PATH)
        is_dir = resource_properties.get(DBFS_RESOURCE_IS_DIR)

        if is_dir != os.path.isdir(local_path):
            dir_or_file = 'directory' if os.path.isdir(local_path) else 'file'
            raise StackError("local source_path '{}' is found to be a {}, but is not specified"
                             " as one with is_dir: {}."
                             .format(local_path, dir_or_file, str(is_dir).lower()))
        if is_dir:
            click.echo('Uploading directory from {} to DBFS at {}'.format(local_path, dbfs_path))
            self.dbfs_client.cp(recursive=True, overwrite=overwrite, src=local_path, dst=dbfs_path)
        else:
            click.echo('Uploading file from {} to DBFS at {}'.format(local_path, dbfs_path))
            self.dbfs_client.cp(recursive=False, overwrite=overwrite, src=local_path, dst=dbfs_path)

        if physical_id and physical_id[DBFS_RESOURCE_PATH] != dbfs_path:
            # physical_id['path'] is the dbfs path from the last deployment. Alert when changed
            click.echo("Dbfs asset had path changed from {} to {}"
                       .format(physical_id[DBFS_RESOURCE_PATH], dbfs_path))
        new_physical_id = {DBFS_RESOURCE_PATH: dbfs_path}
        deploy_output = self.dbfs_client.client.get_status(dbfs_path)

        return new_physical_id, deploy_output

    def _validate_config(self, stack_config):
        """
        Validate fields within a stack configuration. This ensures that an inputted configuration
        has the necessary fields for stack deployment to function well.

        :param stack_config: dict- stack config that is inputted by the user.
        :return: None. Raises errors to stop deployment if there is a problem.
        """
        click.echo('Validating fields in stack configuration...')
        self._assert_fields_in_dict([STACK_NAME, STACK_RESOURCES], stack_config)

        seen_resource_ids = set()  # Store seen resources to restrict duplicates.
        for resource in stack_config.get(STACK_RESOURCES):
            # Get validate resource ID exists, then get it.
            self._assert_fields_in_dict([RESOURCE_ID], resource)
            resource_id = resource.get(RESOURCE_ID)

            click.echo('Validating fields in resource with ID "{}"'.format(resource_id))
            self._assert_fields_in_dict([RESOURCE_SERVICE, RESOURCE_PROPERTIES], resource)

            resource_service = resource.get(RESOURCE_SERVICE)
            resource_properties = resource.get(RESOURCE_PROPERTIES)

            # Error on duplicate resource ID's
            if resource_id in seen_resource_ids:
                raise StackError('Duplicate resource ID "{}" found, please resolve.'.format(
                    resource_id))
            seen_resource_ids.add(resource_id)

            # Resource service-specific validations
            click.echo('Validating fields in "{}" of {} resource.'
                       .format(RESOURCE_PROPERTIES, resource_service))
            if resource_service == JOBS_SERVICE:
                self._assert_fields_in_dict([JOBS_RESOURCE_NAME], resource_properties)
            elif resource_service == WORKSPACE_SERVICE:
                self._assert_fields_in_dict(
                    [WORKSPACE_RESOURCE_PATH, WORKSPACE_RESOURCE_SOURCE_PATH,
                     WORKSPACE_RESOURCE_OBJECT_TYPE], resource_properties)
            elif resource_service == DBFS_SERVICE:
                self._assert_fields_in_dict(
                    [DBFS_RESOURCE_PATH, DBFS_RESOURCE_SOURCE_PATH,
                     DBFS_RESOURCE_IS_DIR], resource_properties)
            else:
                raise StackError("Resource service '{}' not supported".format(resource_service))

    def _validate_status(self, stack_status):
        """
        Validate fields within a stack status. This ensures that a stack status has the
        necessary fields for stack deployment to function well.

        If there is an error here, then it is either an implementation error that must be fixed by
        a developer or the User edited the stack status file created by the program.

        :param stack_status: dict- stack status that is created by the program.
        :return: None. Raises errors to stop deployment if there is a problem.
        """
        click.echo('Validating fields in stack status...')
        self._assert_fields_in_dict([STACK_NAME, STACK_RESOURCES, STACK_DEPLOYED], stack_status)

        for resource_status in stack_status.get(STACK_DEPLOYED):
            self._assert_fields_in_dict([RESOURCE_ID], resource_status)
            resource_id = resource_status.get(RESOURCE_ID)
            click.echo('Validating fields in resource status of resource with ID "{}"'
                       .format(resource_id))
            self._assert_fields_in_dict([RESOURCE_SERVICE, RESOURCE_PHYSICAL_ID,
                                         RESOURCE_DEPLOY_OUTPUT], resource_status)

            resource_service = resource_status.get(RESOURCE_SERVICE)
            resource_physical_id = resource_status.get(RESOURCE_PHYSICAL_ID)

            click.echo('Validating fields in "{}" of {} resource status'
                       .format(RESOURCE_PHYSICAL_ID, resource_service))
            if resource_service == JOBS_SERVICE:
                self._assert_fields_in_dict([JOBS_RESOURCE_JOB_ID], resource_physical_id)
            elif resource_service == WORKSPACE_SERVICE:
                self._assert_fields_in_dict([WORKSPACE_RESOURCE_PATH], resource_physical_id)
            elif resource_service == DBFS_SERVICE:
                self._assert_fields_in_dict([DBFS_RESOURCE_PATH], resource_physical_id)
            else:
                raise StackError("{} not a valid resource status service".format(resource_service))

    def _assert_fields_in_dict(self, fields, dictionary):
        for field in fields:
            if field not in dictionary:
                raise StackError('Required field "{}" not found'.format(field))

    def _get_resource_to_status_map(self, stack_status):
        """
        Returns a dictionary that maps a resource's (id, service) to the resource's status
        from the last deployment

        The key for this dictionary is the resource's (id, service) so that we don't load
        persisted resources with the wrong resource service.
        """
        return {
            (resource_status.get(RESOURCE_ID), resource_status.get(RESOURCE_SERVICE)):
                resource_status
            for resource_status in stack_status.get(STACK_DEPLOYED)
        }

    def _generate_stack_status_path(self, stack_path):
        """
        Given a path to the stack configuration template JSON file, generates a path to where the
        deployment status JSON will be stored after successful deployment of the stack.

        :param stack_path: Path to the stack config template JSON file
        :return: The path to the stack status file.

        >>> self._generate_stack_status_path('./stack.json')
        './stack.deployed.json'
        """
        stack_status_insert = 'deployed'
        stack_path_split = stack_path.split('.')
        stack_path_split.insert(-1, stack_status_insert)
        return '.'.join(stack_path_split)

    def _load_json(self, path):
        """
        Parse a json file to a readable dict format.
        Returns an empty dictionary if the path doesn't exist.

        :param path: File path of the JSON stack configuration template.
        :return: dict of parsed JSON stack config template.
        """
        stack_conf = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                stack_conf = json.load(f)
        return stack_conf

    def _save_json(self, path, data):
        """
        Writes data to a JSON file.

        :param path: Path of JSON file.
        :param data: dict- data that wants to by written to JSON file
        :return: None
        """
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, sort_keys=True)
