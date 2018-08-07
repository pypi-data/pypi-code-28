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


class BuildConfigurationAudited(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        BuildConfigurationAudited - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'int',
            'rev': 'int',
            'id_rev': 'IdRev',
            'name': 'str',
            'build_script': 'str',
            'repository_configuration': 'RepositoryConfiguration',
            'scm_revision': 'str',
            'description': 'str',
            'project': 'Project',
            'build_environment': 'BuildEnvironment',
            'build_records': 'list[BuildRecord]',
            'build_configuration': 'BuildConfiguration',
            'generic_parameters': 'dict(str, str)',
            'field_handler': 'FieldHandler'
        }

        self.attribute_map = {
            'id': 'id',
            'rev': 'rev',
            'id_rev': 'idRev',
            'name': 'name',
            'build_script': 'buildScript',
            'repository_configuration': 'repositoryConfiguration',
            'scm_revision': 'scmRevision',
            'description': 'description',
            'project': 'project',
            'build_environment': 'buildEnvironment',
            'build_records': 'buildRecords',
            'build_configuration': 'buildConfiguration',
            'generic_parameters': 'genericParameters',
            'field_handler': 'fieldHandler'
        }

        self._id = None
        self._rev = None
        self._id_rev = None
        self._name = None
        self._build_script = None
        self._repository_configuration = None
        self._scm_revision = None
        self._description = None
        self._project = None
        self._build_environment = None
        self._build_records = None
        self._build_configuration = None
        self._generic_parameters = None
        self._field_handler = None

    @property
    def id(self):
        """
        Gets the id of this BuildConfigurationAudited.


        :return: The id of this BuildConfigurationAudited.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BuildConfigurationAudited.


        :param id: The id of this BuildConfigurationAudited.
        :type: int
        """
        self._id = id

    @property
    def rev(self):
        """
        Gets the rev of this BuildConfigurationAudited.


        :return: The rev of this BuildConfigurationAudited.
        :rtype: int
        """
        return self._rev

    @rev.setter
    def rev(self, rev):
        """
        Sets the rev of this BuildConfigurationAudited.


        :param rev: The rev of this BuildConfigurationAudited.
        :type: int
        """
        self._rev = rev

    @property
    def id_rev(self):
        """
        Gets the id_rev of this BuildConfigurationAudited.


        :return: The id_rev of this BuildConfigurationAudited.
        :rtype: IdRev
        """
        return self._id_rev

    @id_rev.setter
    def id_rev(self, id_rev):
        """
        Sets the id_rev of this BuildConfigurationAudited.


        :param id_rev: The id_rev of this BuildConfigurationAudited.
        :type: IdRev
        """
        self._id_rev = id_rev

    @property
    def name(self):
        """
        Gets the name of this BuildConfigurationAudited.


        :return: The name of this BuildConfigurationAudited.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this BuildConfigurationAudited.


        :param name: The name of this BuildConfigurationAudited.
        :type: str
        """
        self._name = name

    @property
    def build_script(self):
        """
        Gets the build_script of this BuildConfigurationAudited.


        :return: The build_script of this BuildConfigurationAudited.
        :rtype: str
        """
        return self._build_script

    @build_script.setter
    def build_script(self, build_script):
        """
        Sets the build_script of this BuildConfigurationAudited.


        :param build_script: The build_script of this BuildConfigurationAudited.
        :type: str
        """
        self._build_script = build_script

    @property
    def repository_configuration(self):
        """
        Gets the repository_configuration of this BuildConfigurationAudited.


        :return: The repository_configuration of this BuildConfigurationAudited.
        :rtype: RepositoryConfiguration
        """
        return self._repository_configuration

    @repository_configuration.setter
    def repository_configuration(self, repository_configuration):
        """
        Sets the repository_configuration of this BuildConfigurationAudited.


        :param repository_configuration: The repository_configuration of this BuildConfigurationAudited.
        :type: RepositoryConfiguration
        """
        self._repository_configuration = repository_configuration

    @property
    def scm_revision(self):
        """
        Gets the scm_revision of this BuildConfigurationAudited.


        :return: The scm_revision of this BuildConfigurationAudited.
        :rtype: str
        """
        return self._scm_revision

    @scm_revision.setter
    def scm_revision(self, scm_revision):
        """
        Sets the scm_revision of this BuildConfigurationAudited.


        :param scm_revision: The scm_revision of this BuildConfigurationAudited.
        :type: str
        """
        self._scm_revision = scm_revision

    @property
    def description(self):
        """
        Gets the description of this BuildConfigurationAudited.


        :return: The description of this BuildConfigurationAudited.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BuildConfigurationAudited.


        :param description: The description of this BuildConfigurationAudited.
        :type: str
        """
        self._description = description

    @property
    def project(self):
        """
        Gets the project of this BuildConfigurationAudited.


        :return: The project of this BuildConfigurationAudited.
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Sets the project of this BuildConfigurationAudited.


        :param project: The project of this BuildConfigurationAudited.
        :type: Project
        """
        self._project = project

    @property
    def build_environment(self):
        """
        Gets the build_environment of this BuildConfigurationAudited.


        :return: The build_environment of this BuildConfigurationAudited.
        :rtype: BuildEnvironment
        """
        return self._build_environment

    @build_environment.setter
    def build_environment(self, build_environment):
        """
        Sets the build_environment of this BuildConfigurationAudited.


        :param build_environment: The build_environment of this BuildConfigurationAudited.
        :type: BuildEnvironment
        """
        self._build_environment = build_environment

    @property
    def build_records(self):
        """
        Gets the build_records of this BuildConfigurationAudited.


        :return: The build_records of this BuildConfigurationAudited.
        :rtype: list[BuildRecord]
        """
        return self._build_records

    @build_records.setter
    def build_records(self, build_records):
        """
        Sets the build_records of this BuildConfigurationAudited.


        :param build_records: The build_records of this BuildConfigurationAudited.
        :type: list[BuildRecord]
        """
        self._build_records = build_records

    @property
    def build_configuration(self):
        """
        Gets the build_configuration of this BuildConfigurationAudited.


        :return: The build_configuration of this BuildConfigurationAudited.
        :rtype: BuildConfiguration
        """
        return self._build_configuration

    @build_configuration.setter
    def build_configuration(self, build_configuration):
        """
        Sets the build_configuration of this BuildConfigurationAudited.


        :param build_configuration: The build_configuration of this BuildConfigurationAudited.
        :type: BuildConfiguration
        """
        self._build_configuration = build_configuration

    @property
    def generic_parameters(self):
        """
        Gets the generic_parameters of this BuildConfigurationAudited.


        :return: The generic_parameters of this BuildConfigurationAudited.
        :rtype: dict(str, str)
        """
        return self._generic_parameters

    @generic_parameters.setter
    def generic_parameters(self, generic_parameters):
        """
        Sets the generic_parameters of this BuildConfigurationAudited.


        :param generic_parameters: The generic_parameters of this BuildConfigurationAudited.
        :type: dict(str, str)
        """
        self._generic_parameters = generic_parameters

    @property
    def field_handler(self):
        """
        Gets the field_handler of this BuildConfigurationAudited.


        :return: The field_handler of this BuildConfigurationAudited.
        :rtype: FieldHandler
        """
        return self._field_handler

    @field_handler.setter
    def field_handler(self, field_handler):
        """
        Sets the field_handler of this BuildConfigurationAudited.


        :param field_handler: The field_handler of this BuildConfigurationAudited.
        :type: FieldHandler
        """
        self._field_handler = field_handler

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
