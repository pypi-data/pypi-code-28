#!/usr/bin/env python

# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0

# pylint: disable=missing-docstring

import logging
import os
import unittest

import mock

from xtesting.ci import tier_builder


class TierBuilderTesting(unittest.TestCase):

    def setUp(self):
        self.dependency = {
            'installer': 'test_installer', 'scenario': 'test_scenario'}
        self.testcase = {
            'dependencies': self.dependency, 'enabled': True,
            'case_name': 'test_name', 'criteria': 'test_criteria',
            'blocking': 'test_blocking', 'description': 'test_desc',
            'project_name': 'project_name'}
        self.testcase_disabled = {
            'dependencies': self.dependency, 'enabled': False,
            'case_name': 'test_name_disabled', 'criteria': 'test_criteria',
            'blocking': 'test_blocking', 'description': 'test_desc',
            'project_name': 'project_name'}
        self.dic_tier = {
            'name': 'test_tier', 'order': 'test_order',
            'ci_loop': 'test_ci_loop', 'description': 'test_desc',
            'testcases': [self.testcase, self.testcase_disabled]}
        self.mock_yaml = mock.Mock()
        attrs = {'get.return_value': [self.dic_tier]}
        self.mock_yaml.configure_mock(**attrs)

        with mock.patch('xtesting.ci.tier_builder.yaml.safe_load',
                        return_value=self.mock_yaml), \
                mock.patch('six.moves.builtins.open', mock.mock_open()):
            os.environ["INSTALLER_TYPE"] = 'test_installer'
            os.environ["DEPLOY_SCENARIO"] = 'test_scenario'
            self.tierbuilder = tier_builder.TierBuilder('testcases_file')
        self.tier_obj = self.tierbuilder.tier_objects[0]

    def test_get_tiers(self):
        self.assertEqual(self.tierbuilder.get_tiers(),
                         [self.tier_obj])

    def test_get_tier_names(self):
        self.assertEqual(self.tierbuilder.get_tier_names(),
                         ['test_tier'])

    def test_get_tier_present_tier(self):
        self.assertEqual(self.tierbuilder.get_tier('test_tier'),
                         self.tier_obj)

    def test_get_tier_missing_tier(self):
        self.assertEqual(self.tierbuilder.get_tier('test_tier2'),
                         None)

    def test_get_test_present_test(self):
        self.assertEqual(self.tierbuilder.get_test('test_name'),
                         self.tier_obj.get_test('test_name'))

    def test_get_test_disabled(self):
        self.assertEqual(
            self.tierbuilder.get_test('test_name_disabled'),
            self.tier_obj.get_test('test_name_disabled'))
        self.assertEqual(
            self.tier_obj.get_skipped_test()[0].name, 'test_name_disabled')

    def test_get_test_missing_test(self):
        self.assertEqual(self.tierbuilder.get_test('test_name2'),
                         None)

    def test_get_tests_present_tier(self):
        self.assertEqual(self.tierbuilder.get_tests('test_tier'),
                         self.tier_obj.tests_array)

    def test_get_tests_missing_tier(self):
        self.assertEqual(self.tierbuilder.get_tests('test_tier2'),
                         None)

    def test_get_tier_name_ok(self):
        self.assertEqual(self.tierbuilder.get_tier_name('test_name'),
                         'test_tier')

    def test_get_tier_name_ko(self):
        self.assertEqual(self.tierbuilder.get_tier_name('test_name2'), None)

    def test_str(self):
        message = str(self.tierbuilder)
        self.assertTrue('test_tier' in message)
        self.assertTrue('test_order' in message)
        self.assertTrue('test_ci_loop' in message)
        self.assertTrue('test_desc' in message)
        self.assertTrue('test_name' in message)


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)
