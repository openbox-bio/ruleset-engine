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

class TestIsLessThan(unittest.TestCase):
	def test_is_less_than_all_ok(self):
		'''
		Tests that "is less than" function returns All OK for column with values that are less than the specified value.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])
					
	def test_is_less_than_with_errors(self):
		'''
		Tests that "is less than" function returns errors for column with values not less than the specified value.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_with_errors.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, True, True])

	def test_is_less_than_float_comparand_mixed_operands_all_ok(self):
		'''
		Tests that "is less than" function returns All OK for column with values that are less than the specified value.
		Specified value is a float. Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_operands_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False,  na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_float_comparand_mixed_operands_with_errors(self):
		'''
		Tests that "is less than" function returns False for column values that are not less than the specified value.
		Specified value is a float. Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_operands_with_errors.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, True, True])

	def test_is_less_than_float_comparand_mixed_operands_with_default_tolerance_all_ok(self):
		'''
		Tests that "is less than" function returns All OK for column with values that are less than the specified value.
		Specified value is a float. Column values are a mixture of integers and floats. Default tolerance is 0.001.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_operands_default_tolerance_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_float_comparand_mixed_operands_with_user_specified_global_tolerance_all_ok(self):
		'''
		Tests that "is less than" function returns All OK for column with values that are less than the specified 
		value at the specified global level of tolerance. Specified value is a float. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_global_tolerance_level_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_global_tolerance_level_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_float_comparand_mixed_operands_with_user_specified_global_tolerance_with_error(self):
		'''
		Tests that "is less than" function returns an error message for column with values that are not less than the specified 
		value at the specified global level of tolerance. Specified value is a float. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_global_tolerance_level_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_global_tolerance_level_with_error.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False])

	def test_is_less_than_mixed_comparand_user_specified_separator_all_ok(self):
		'''
		Tests that "is less than" function returns an all OK message for column with values that are less than the specified value with the specified
		thousands separator. Specified value is an integer in one case and a float in another. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_user_specified_separator_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_user_specified_separator_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_mixed_comparand_user_specified_separator_with_error(self):
		'''
		Tests that "is less than" function returns an error message for column with values that are not less than the specified value with the specified 
		thousands separator. Specified value is an integer in one case and a float in another. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_user_specified_separator_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_user_specified_separator_with_error.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False])

	def test_is_less_than_mixed_comparand_user_specified_space_separator_all_OK(self):
		'''
		Tests that "is less than" function returns an all OK message for column with values that have a 
		thousands separator that matches the separator specified in the ruleset. The separator specified is a single space. Specified value is an integer in one case and a float in another. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_space_separator_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_space_separator_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_mixed_comparand_user_no_specified_separator_with_error(self):
		'''
		Tests that "is less than" function returns an error message for column with values that have a 
		thousands separator, but for which there is no spec in the ruleset. The thousands separator in the data file is a space. Specified value is an integer in one case and a float in another. 
		Column values are a mixture of integers and floats.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_no_specified_separator_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_mixed_comparand_space_separator_with_error.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False])

	def test_is_less_than_with_multiple_errors(self):
		'''
		Tests that "is less than" function returns an error message for null values, non-numeric values and values that are not less than the reference value.
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_with_multiple_errors_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_with_multiple_errors.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
						'Error: column value1, row 1: value 10 is not less than 10.',
						'Warning: column value1, row 2: value ABC is not numeric.',
						'Warning: column value1, row 3: value nan is null.',
						'Warning: column value1, row 4: value nan is null.',
						'Error: column value1, row 5: value 12.05 is not less than 10.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)

	def test_is_less_than_with_user_specified_local_tolerance_level_all_ok(self):
		'''
		Tests that "is less than" function returns All OK for column with values that are less than the specified 
		value at the specified local tolerance level. Specified value is a float. 
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_local_tolerance_level_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_user_specified_global_tolerance_level_all_ok.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			set_local_rules_list = column_value_rules_dict[column_name].setlocalrules
			local_rules_dict = {type(local_rule).__name__: local_rule for local_rule in set_local_rules_list}
			
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict, local_rules = local_rules_dict)
					self.assertEqual(return_val[0], [True, True, True])

	def test_is_less_than_with_user_specified_local_tolerance_level_with_errors(self):
		'''
		Tests that "is less than" function returns error message for column with values that are not less than the specified 
		value at the specified local tolerance level. Specified value is a float. 
		'''
		rules_infile = TESTS_DIR / "test_is_less_than_float_comparand_user_specified_local_tolerance_level_ruleset"
		data_infile = TESTS_DIR / "test_is_less_than_user_specified_local_tolerance_level_with_errors.csv"
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

		demo_df = pd.read_csv(data_infile, dtype = str, na_values = all_na_values)
		#print("CSV columns:", demo_df.columns.tolist())
		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			set_local_rules_list = column_value_rules_dict[column_name].setlocalrules
			local_rules_dict = {type(local_rule).__name__: local_rule for local_rule in set_local_rules_list}
			
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict, local_rules = local_rules_dict)
					self.assertEqual(return_val[0], [False, False, False])

if __name__ == '__main__':
	unittest.main()
