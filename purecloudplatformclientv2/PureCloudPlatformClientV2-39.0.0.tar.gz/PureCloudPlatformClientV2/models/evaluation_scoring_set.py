# coding: utf-8

"""
Copyright 2016 SmartBear Software

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

from pprint import pformat
from six import iteritems
import re


class EvaluationScoringSet(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        EvaluationScoringSet - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'total_score': 'float',
            'total_critical_score': 'float',
            'question_group_scores': 'list[EvaluationQuestionGroupScore]',
            'any_failed_kill_questions': 'bool',
            'comments': 'str',
            'agent_comments': 'str'
        }

        self.attribute_map = {
            'total_score': 'totalScore',
            'total_critical_score': 'totalCriticalScore',
            'question_group_scores': 'questionGroupScores',
            'any_failed_kill_questions': 'anyFailedKillQuestions',
            'comments': 'comments',
            'agent_comments': 'agentComments'
        }

        self._total_score = None
        self._total_critical_score = None
        self._question_group_scores = None
        self._any_failed_kill_questions = None
        self._comments = None
        self._agent_comments = None

    @property
    def total_score(self):
        """
        Gets the total_score of this EvaluationScoringSet.


        :return: The total_score of this EvaluationScoringSet.
        :rtype: float
        """
        return self._total_score

    @total_score.setter
    def total_score(self, total_score):
        """
        Sets the total_score of this EvaluationScoringSet.


        :param total_score: The total_score of this EvaluationScoringSet.
        :type: float
        """
        
        self._total_score = total_score

    @property
    def total_critical_score(self):
        """
        Gets the total_critical_score of this EvaluationScoringSet.


        :return: The total_critical_score of this EvaluationScoringSet.
        :rtype: float
        """
        return self._total_critical_score

    @total_critical_score.setter
    def total_critical_score(self, total_critical_score):
        """
        Sets the total_critical_score of this EvaluationScoringSet.


        :param total_critical_score: The total_critical_score of this EvaluationScoringSet.
        :type: float
        """
        
        self._total_critical_score = total_critical_score

    @property
    def question_group_scores(self):
        """
        Gets the question_group_scores of this EvaluationScoringSet.


        :return: The question_group_scores of this EvaluationScoringSet.
        :rtype: list[EvaluationQuestionGroupScore]
        """
        return self._question_group_scores

    @question_group_scores.setter
    def question_group_scores(self, question_group_scores):
        """
        Sets the question_group_scores of this EvaluationScoringSet.


        :param question_group_scores: The question_group_scores of this EvaluationScoringSet.
        :type: list[EvaluationQuestionGroupScore]
        """
        
        self._question_group_scores = question_group_scores

    @property
    def any_failed_kill_questions(self):
        """
        Gets the any_failed_kill_questions of this EvaluationScoringSet.


        :return: The any_failed_kill_questions of this EvaluationScoringSet.
        :rtype: bool
        """
        return self._any_failed_kill_questions

    @any_failed_kill_questions.setter
    def any_failed_kill_questions(self, any_failed_kill_questions):
        """
        Sets the any_failed_kill_questions of this EvaluationScoringSet.


        :param any_failed_kill_questions: The any_failed_kill_questions of this EvaluationScoringSet.
        :type: bool
        """
        
        self._any_failed_kill_questions = any_failed_kill_questions

    @property
    def comments(self):
        """
        Gets the comments of this EvaluationScoringSet.


        :return: The comments of this EvaluationScoringSet.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this EvaluationScoringSet.


        :param comments: The comments of this EvaluationScoringSet.
        :type: str
        """
        
        self._comments = comments

    @property
    def agent_comments(self):
        """
        Gets the agent_comments of this EvaluationScoringSet.


        :return: The agent_comments of this EvaluationScoringSet.
        :rtype: str
        """
        return self._agent_comments

    @agent_comments.setter
    def agent_comments(self, agent_comments):
        """
        Sets the agent_comments of this EvaluationScoringSet.


        :param agent_comments: The agent_comments of this EvaluationScoringSet.
        :type: str
        """
        
        self._agent_comments = agent_comments

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
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

