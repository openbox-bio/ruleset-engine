import sys
sys.path.insert(0, "/home/anjan_purkayastha/Documents/openboxbio/20211227_dsl-for-data-validation/code/ruleset_engine/")

import unittest
from textx import get_location, TextXSyntaxError
from textx.metamodel import metamodel_from_file
import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
from ruleset import in_column_value_rules as i
from ruleset import set_value_rules as s

class TestHasValueType(unittest.TestCase):
	def test_has_value_type_all_ok(self):
		'''
		Tests that has_value_type function returns All OK.
		'''
		rules_infile = "test_has_value_type_ruleset"
		data_infile = "test_has_value_type_all_ok.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
		    demo_rules = mm.model_from_file(rules_infile)
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

	def test_has_value_type_string_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_string_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_string_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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
		
		expected_error_list = [
    				  "Error: column value1, row 1: value True is not a string.",
					  "Warning: column value1, row 2: value nan is null.",
					  "Warning: column value1, row 3: value nan is null.",
					  "Error: column value1, row 4: value 2025-02-07 is not a string.",
					  "Error: column value1, row 5: value 1.60E-35 is not a string.",
					  "Error: column value1, row 6: value 2 is not a string.",
					  "Error: column value1, row 7: value 3+2j is not a string."
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)

	def test_has_value_type_integer_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_integer_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_integer_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		# demo_df = pd.read_excel(data_infile, dtype = object, na_values = all_na_values)
		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
					  'Error: column value1, row 1: value TRUE is not an integer.',
					  'Error: column value1, row 2: value FALSE is not an integer.',
					  'Warning: column value1, row 3: value nan is null.',
					  'Error: column value1, row 4: value 1.20E+11 is not an integer.',
					  'Error: column value1, row 5: value Audacious Alba is not an integer.',
					  'Error: column value1, row 6: value 3+2j is not an integer.',
					  'Warning: column value1, row 7: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)


	def test_has_value_type_floating_point_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_floating_point_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_floating_point_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		# demo_df = pd.read_excel(data_infile, dtype = object, na_values = all_na_values)
		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
					'Error: column value1, row 1: value TRUE is not a floating point.', 
					'Error: column value1, row 2: value 25 is not a floating point.', 
					'Warning: column value1, row 3: value nan is null.', 
					'Error: column value1, row 4: value 1.20E+07 is not a floating point.', 
					'Error: column value1, row 5: value Audacious Amit is not a floating point.', 
					'Error: column value1, row 6: value 3+2j is not a floating point.', 
					'Warning: column value1, row 7: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)


	def test_has_value_type_scientific_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_scientific_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_scientific_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		# demo_df = pd.read_excel(data_infile, dtype = object, na_values = all_na_values)
		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
					'Error: column value1, row 1: value TRUE is not in scientific notation.',
					'Error: column value1, row 2: value 25 is not in scientific notation.',
					'Warning: column value1, row 3: value nan is null.',
					'Error: column value1, row 4: value 2.035 is not in scientific notation.',
					'Error: column value1, row 5: value Audacious Amit is not in scientific notation.',
					'Error: column value1, row 6: value 3+2j is not in scientific notation.',
					'Warning: column value1, row 7: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)

	def test_has_value_type_boolean_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		This also tests if 'TRUE' and 'FALSE' are considered strings or booleans (they should be considered booleans).
		'''
		rules_infile = "test_has_value_type_boolean_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_boolean_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		# demo_df = pd.read_excel(data_infile, dtype = object, na_values = all_na_values)
		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
					'Error: column value1, row 2: value 12E+06 is not a boolean value.',
					'Error: column value1, row 4: value 25 is not a boolean value.',
					'Warning: column value1, row 5: value nan is null.',
					'Error: column value1, row 6: value 2.035 is not a boolean value.',
					'Error: column value1, row 7: value Audacious Amit is not a boolean value.',
					'Error: column value1, row 8: value 3+2j is not a boolean value.',
					'Warning: column value1, row 9: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [True, False, True, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)

	def test_has_value_type_complex_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_complex_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_complex_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
					'Error: column value1, row 1: value TRUE is not a complex number.',
					'Error: column value1, row 2: value 25 is not a complex number.',
					'Warning: column value1, row 3: value nan is null.',
					'Error: column value1, row 4: value 2.035 is not a complex number.',
					'Error: column value1, row 5: value Audacious Amit is not a complex number.',
					'Error: column value1, row 6: value false is not a complex number.',
					'Warning: column value1, row 7: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)

	def test_has_value_type_date_time_with_multiple_errors(self):
		'''
		Tests that has value type function returns a warning message for null values and error message for values with incorrect type.
		'''
		rules_infile = "test_has_value_type_date_time_with_multiple_errors_ruleset"
		data_infile = "test_has_value_type_date_time_with_multiple_errors.csv"
		'''
		Read the Ruleset metamodel from metamodel file.
		Read the rules file.
		'''
		metamodel_infile = "../ruleset/RuleSet.tx"
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
		try:
			demo_rules = mm.model_from_file(rules_infile)
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

		demo_df = pd.read_csv(data_infile, header = 0, dtype = object, skip_blank_lines = False, na_values = all_na_values)
		
		expected_error_list = [
				 'Error: column value1, row 1: value TRUE is not a date-time value.',
				 'Error: column value1, row 2: value 25 is not a date-time value.',
				 'Warning: column value1, row 3: value nan is null.',
				 'Error: column value1, row 4: value 2.035 is not a date-time value.',
				 'Error: column value1, row 5: value Audacious Amit is not a date-time value.',
				 'Error: column value1, row 6: value false is not a date-time value.',
				 'Warning: column value1, row 7: value nan is null.'
					]

		for column_name in column_value_rules_dict.keys():
			value_rules_list = column_value_rules_dict[column_name].valuerules
			for value_rule in value_rules_list:
				value_rule_name = type(value_rule).__name__
				if i.in_column_value_rule_checker_dict[value_rule_name]:
					return_val = i.in_column_value_rule_checker_dict[value_rule_name](df = demo_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
					self.assertEqual(return_val[0], [False, False, False, False, False, False, False])
					self.assertListEqual(return_val[1], expected_error_list)


if __name__ == '__main__':
    unittest.main()
