# coding: utf-8

"""
Copyright 2015 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from pprint import pformat
from six import iteritems


class BuildConfigurationRest(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuildConfigurationRest - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'name': 'str',
            'description': 'str',
            'build_script': 'str',
            'repository_configuration': 'RepositoryConfigurationRest',
            'scm_revision': 'str',
            'creation_time': 'datetime',
            'last_modification_time': 'datetime',
            'archived': 'bool',
            'project': 'ProjectRest',
            'environment': 'BuildEnvironmentRest',
            'dependency_ids': 'list[int]',
            'product_version_id': 'int',
            'build_configuration_set_ids': 'list[int]',
            'generic_parameters': 'dict(str, str)'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'build_script': 'buildScript',
            'repository_configuration': 'repositoryConfiguration',
            'scm_revision': 'scmRevision',
            'creation_time': 'creationTime',
            'last_modification_time': 'lastModificationTime',
            'archived': 'archived',
            'project': 'project',
            'environment': 'environment',
            'dependency_ids': 'dependencyIds',
            'product_version_id': 'productVersionId',
            'build_configuration_set_ids': 'buildConfigurationSetIds',
            'generic_parameters': 'genericParameters'
        }

        self._id = None
        self._name = None
        self._description = None
        self._build_script = None
        self._repository_configuration = None
        self._scm_revision = None
        self._creation_time = None
        self._last_modification_time = None
        self._archived = None
        self._project = None
        self._environment = None
        self._dependency_ids = None
        self._product_version_id = None
        self._build_configuration_set_ids = None
        self._generic_parameters = None

    @property
    def id(self):
        """
        Gets the id of this BuildConfigurationRest.


        :return: The id of this BuildConfigurationRest.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BuildConfigurationRest.


        :param id: The id of this BuildConfigurationRest.
        :type: int
        """
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this BuildConfigurationRest.


        :return: The name of this BuildConfigurationRest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this BuildConfigurationRest.


        :param name: The name of this BuildConfigurationRest.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this BuildConfigurationRest.


        :return: The description of this BuildConfigurationRest.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BuildConfigurationRest.


        :param description: The description of this BuildConfigurationRest.
        :type: str
        """
        self._description = description

    @property
    def build_script(self):
        """
        Gets the build_script of this BuildConfigurationRest.


        :return: The build_script of this BuildConfigurationRest.
        :rtype: str
        """
        return self._build_script

    @build_script.setter
    def build_script(self, build_script):
        """
        Sets the build_script of this BuildConfigurationRest.


        :param build_script: The build_script of this BuildConfigurationRest.
        :type: str
        """
        self._build_script = build_script

    @property
    def repository_configuration(self):
        """
        Gets the repository_configuration of this BuildConfigurationRest.


        :return: The repository_configuration of this BuildConfigurationRest.
        :rtype: RepositoryConfigurationRest
        """
        return self._repository_configuration

    @repository_configuration.setter
    def repository_configuration(self, repository_configuration):
        """
        Sets the repository_configuration of this BuildConfigurationRest.


        :param repository_configuration: The repository_configuration of this BuildConfigurationRest.
        :type: RepositoryConfigurationRest
        """
        self._repository_configuration = repository_configuration

    @property
    def scm_revision(self):
        """
        Gets the scm_revision of this BuildConfigurationRest.


        :return: The scm_revision of this BuildConfigurationRest.
        :rtype: str
        """
        return self._scm_revision

    @scm_revision.setter
    def scm_revision(self, scm_revision):
        """
        Sets the scm_revision of this BuildConfigurationRest.


        :param scm_revision: The scm_revision of this BuildConfigurationRest.
        :type: str
        """
        self._scm_revision = scm_revision

    @property
    def creation_time(self):
        """
        Gets the creation_time of this BuildConfigurationRest.


        :return: The creation_time of this BuildConfigurationRest.
        :rtype: datetime
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """
        Sets the creation_time of this BuildConfigurationRest.


        :param creation_time: The creation_time of this BuildConfigurationRest.
        :type: datetime
        """
        self._creation_time = creation_time

    @property
    def last_modification_time(self):
        """
        Gets the last_modification_time of this BuildConfigurationRest.


        :return: The last_modification_time of this BuildConfigurationRest.
        :rtype: datetime
        """
        return self._last_modification_time

    @last_modification_time.setter
    def last_modification_time(self, last_modification_time):
        """
        Sets the last_modification_time of this BuildConfigurationRest.


        :param last_modification_time: The last_modification_time of this BuildConfigurationRest.
        :type: datetime
        """
        self._last_modification_time = last_modification_time

    @property
    def archived(self):
        """
        Gets the archived of this BuildConfigurationRest.


        :return: The archived of this BuildConfigurationRest.
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """
        Sets the archived of this BuildConfigurationRest.


        :param archived: The archived of this BuildConfigurationRest.
        :type: bool
        """
        self._archived = archived

    @property
    def project(self):
        """
        Gets the project of this BuildConfigurationRest.


        :return: The project of this BuildConfigurationRest.
        :rtype: ProjectRest
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Sets the project of this BuildConfigurationRest.


        :param project: The project of this BuildConfigurationRest.
        :type: ProjectRest
        """
        self._project = project

    @property
    def environment(self):
        """
        Gets the environment of this BuildConfigurationRest.


        :return: The environment of this BuildConfigurationRest.
        :rtype: BuildEnvironmentRest
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """
        Sets the environment of this BuildConfigurationRest.


        :param environment: The environment of this BuildConfigurationRest.
        :type: BuildEnvironmentRest
        """
        self._environment = environment

    @property
    def dependency_ids(self):
        """
        Gets the dependency_ids of this BuildConfigurationRest.


        :return: The dependency_ids of this BuildConfigurationRest.
        :rtype: list[int]
        """
        return self._dependency_ids

    @dependency_ids.setter
    def dependency_ids(self, dependency_ids):
        """
        Sets the dependency_ids of this BuildConfigurationRest.


        :param dependency_ids: The dependency_ids of this BuildConfigurationRest.
        :type: list[int]
        """
        self._dependency_ids = dependency_ids

    @property
    def product_version_id(self):
        """
        Gets the product_version_id of this BuildConfigurationRest.


        :return: The product_version_id of this BuildConfigurationRest.
        :rtype: int
        """
        return self._product_version_id

    @product_version_id.setter
    def product_version_id(self, product_version_id):
        """
        Sets the product_version_id of this BuildConfigurationRest.


        :param product_version_id: The product_version_id of this BuildConfigurationRest.
        :type: int
        """
        self._product_version_id = product_version_id

    @property
    def build_configuration_set_ids(self):
        """
        Gets the build_configuration_set_ids of this BuildConfigurationRest.


        :return: The build_configuration_set_ids of this BuildConfigurationRest.
        :rtype: list[int]
        """
        return self._build_configuration_set_ids

    @build_configuration_set_ids.setter
    def build_configuration_set_ids(self, build_configuration_set_ids):
        """
        Sets the build_configuration_set_ids of this BuildConfigurationRest.


        :param build_configuration_set_ids: The build_configuration_set_ids of this BuildConfigurationRest.
        :type: list[int]
        """
        self._build_configuration_set_ids = build_configuration_set_ids

    @property
    def generic_parameters(self):
        """
        Gets the generic_parameters of this BuildConfigurationRest.


        :return: The generic_parameters of this BuildConfigurationRest.
        :rtype: dict(str, str)
        """
        return self._generic_parameters

    @generic_parameters.setter
    def generic_parameters(self, generic_parameters):
        """
        Sets the generic_parameters of this BuildConfigurationRest.


        :param generic_parameters: The generic_parameters of this BuildConfigurationRest.
        :type: dict(str, str)
        """
        self._generic_parameters = generic_parameters

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
	    elif isinstance(value, datetime):
		result[attr] = str(value.date())
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()
