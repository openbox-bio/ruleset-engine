from pathlib import Path

import unittest
from textx import TextXSyntaxError
from textx.metamodel import metamodel_from_file
import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
from ruleset import in_column_value_rules as i
from ruleset import set_value_rules as s
from ruleset.cli import get_grammar_path

TESTS_DIR = Path(__file__).parent

class TestStartsWith(unittest.TestCase):
	def test_starts_with_all_ok(self):
		'''
		Tests that starts_with function returns All OK.
		'''
		rules_infile = TESTS_DIR / "test_starts_with_ruleset"
		data_infile = TESTS_DIR / "test_starts_with_all_ok.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = get_grammar_path()
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(str(rules_infile))
		except TextXSyntaxError as err:
			print(f'Syntax Error found in {err.filename} in line {err.line}, column {err.col}')
			print(f'Error: {err.message}')
		'''
		Create a dictionary of column rules and of column value rules from the parsed rules file.
		Key = rule name; Value = rule object. 
		'''
		set_value_rules_dict = {}
		column_rules_dict = {}
		column_value_rules_dict = {}
		# add a list of cross-column conditional rules.

		for rule in demo_rules.set_value_rules:
			set_value_rules_dict[type(rule).__name__] = rule

		for rule in demo_rules.column_rules:
			column_rules_dict[type(rule).__name__] = rule

		for rule in demo_rules.column_value_rules:
			column_value_rules_dict[rule.column_name.name] = rule

		'''
		Set null values, if specified in rules file.
		'''
		try:
			input_rule = set_value_rules_dict['SetNullValuesRule']
			input_rule_name = type(input_rule).__name__
			all_na_values = s.set_values_dict[input_rule_name](input_rule)
		except:
			all_na_values = STR_NA_VALUES

		demo_df = pd.read_csv(data_infile, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_starts_with_with_errors(self):
			'''
			Tests that starts_with function returns errors for values not matching length specifications.
			'''
			rules_infile = TESTS_DIR / "test_starts_with_ruleset"
			data_infile = TESTS_DIR / "test_starts_with_errors.csv"
			'''
			Read the Ruleset metamodel from metamodel file.
			Read the rules file.
			'''
			metamodel_infile = get_grammar_path()
			mm = metamodel_from_file(metamodel_infile, autokwd=True)
			try:
				demo_rules = mm.model_from_file(str(rules_infile))
			except TextXSyntaxError as err:
				print(f'Syntax Error found in {err.filename} in line {err.line}, column {err.col}')
				print(f'Error: {err.message}')
			'''
			Create a dictionary of column rules and of column value rules from the parsed rules file.
			Key = rule name; Value = rule object. 
			'''
			set_value_rules_dict = {}
			column_rules_dict = {}
			column_value_rules_dict = {}
			# add a list of cross-column conditional rules.

			for rule in demo_rules.set_value_rules:
				set_value_rules_dict[type(rule).__name__] = rule

			for rule in demo_rules.column_rules:
				column_rules_dict[type(rule).__name__] = rule

			for rule in demo_rules.column_value_rules:
				column_value_rules_dict[rule.column_name.name] = rule

			'''
			Set null values, if specified in rules file.
			'''
			try:
				input_rule = set_value_rules_dict['SetNullValuesRule']
				input_rule_name = type(input_rule).__name__
				all_na_values = s.set_values_dict[input_rule_name](input_rule)
			except:
				all_na_values = STR_NA_VALUES

			demo_df = pd.read_csv(data_infile, dtype = object, skip_blank_lines = False, na_values = all_na_values)
			for column_name in column_value_rules_dict.keys():
				value_rules_list = column_value_rules_dict[column_name].valuerules
				for value_rule in value_rules_list:
					value_rule_name = type(value_rule).__name__
					if i.in_column_value_rule_checker_dict[value_rule_name]:
						return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
						self.assertEqual(return_val[0], [False, False, False])