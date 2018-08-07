# -*- coding: utf-8 -*-

''' xml_to_yaml_country_template.py : Parse XML parameter files for Country-Template and convert them to YAML files. Comments are NOT transformed.

Usage :
  `python xml_to_yaml_country_template.py output_dir`
or just (output is written in a directory called `yaml_parameters`):
  `python xml_to_yaml_country_template.py`
'''
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import os

from openfisca_country_template import CountryTaxBenefitSystem, COUNTRY_DIR
from . import xml_to_yaml

tax_benefit_system = CountryTaxBenefitSystem()

if len(sys.argv) > 1:
    target_path = sys.argv[1]
else:
    target_path = 'yaml_parameters'

param_dir = os.path.join(COUNTRY_DIR, 'parameters')
param_files = [
    'benefits.xml',
    'general.xml',
    'taxes.xml',
    ]
legislation_xml_info_list = [
    (os.path.join(param_dir, param_file), [])
    for param_file in param_files
    ]

xml_to_yaml.write_parameters(legislation_xml_info_list, target_path)
