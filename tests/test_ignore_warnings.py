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

class TestIgnoreWarnings(unittest.TestCase):
	def test_ignore_warnings_set(self):
		'''
		Test that warning messages are ignored when the IgnoreWarningsRule is set.
		'''
		rules_infile = TESTS_DIR / "test_ignore_null_warnings_ruleset"
		data_infile = TESTS_DIR / "test_ignore_null_warnings.csv"
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

		warning_messages = []
		
		demo_df = pd.read_csv(data_infile, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					warning_messages.extend(return_val[1])
		
		self.assertEqual(warning_messages, [])

	def test_do_not_ignore_warnings_set(self):
			'''
			Test that warning messages are not ignored when the IgnoreWarningsRule is not set.
			'''
			rules_infile = TESTS_DIR / "test_do_not_ignore_null_warnings_ruleset"
			data_infile = TESTS_DIR / "test_ignore_null_warnings.csv"
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
	
			warning_messages = []
			
			demo_df = pd.read_csv(data_infile, dtype = object, skip_blank_lines = False, na_values = all_na_values)
			for column_name in column_value_rules_dict.keys():
				value_rules_list = column_value_rules_dict[column_name].valuerules
				for value_rule in value_rules_list:
					value_rule_name = type(value_rule).__name__
					if i.in_column_value_rule_checker_dict[value_rule_name]:
						return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
						warning_messages.extend(return_val[1])
			
			self.assertEqual(warning_messages, 
			                 ['Warning: column col1, row 3: value nan is null.',
			                  'Warning: column col2, row 3: value nan is null.',
							  'Warning: column col3, row 3: value nan is null.',
							  'Warning: column col4, row 3: value Mike is not numeric.',
							  'Warning: column col5, row 3: value Bike is not numeric.',
							  'Warning: column col6, row 3: value nan is null.',
							  'Warning: column col7, row 3: value nan is null.',
							  'Warning: column col8, row 3: value nan is null.']
							 )