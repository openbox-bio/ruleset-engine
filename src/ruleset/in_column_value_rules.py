import re
from collections import defaultdict
import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
from ruleset import helper as h

def check_has_value_type_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if the value type of column matches value type specified by HasValueTypeRule. If a separator is specified by the 
	ThousandsSeparatorRule then this is taken into account when evaluating columns of value type integer and floating point.
	Function returns a list of boolean values (True => valid value, False => invalid value) and a list of error messages.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasValueTypeRule) : the HasValueTypeRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#Ingest provided value type and value format for column in question.
	valid_value_type = input_rule.value_type_input

	#ingest the thousands separator, if provided
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""

	#initialize error_log_list.
	error_log_list = []
	
	# string check.
	if valid_value_type == "string":
		valid_value_mask = df[input_column_name].apply(h.is_string)
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not a string.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	
	# integer check.
	if valid_value_type == "integer":
		valid_value_mask = df[input_column_name].apply(lambda x: h.is_integer(x, separator = separator))
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not an integer.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
				
	# floating point check.
	if valid_value_type == "floating point":
		valid_value_mask = df[input_column_name].apply(lambda x: h.is_floating_point(x, separator = separator))
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not a floating point.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	# boolean check.
	if valid_value_type == "boolean":
		valid_value_mask = df[input_column_name].apply(h.is_boolean)
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not a boolean value.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	# scientific notation check.
	if valid_value_type == "scientific":
		valid_value_mask = df[input_column_name].apply(h.is_scientific_notation)
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not in scientific notation.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	# complex number check.
	if valid_value_type == "complex":
		valid_value_mask = df[input_column_name].apply(h.is_complex)
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not a complex number.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
	  
	# date-time check.
	if valid_value_type == "date-time":
		valid_value_mask = df[input_column_name].apply(h.is_datetime)
		invalid_value_indices = valid_value_mask[valid_value_mask == False].index.to_list()
		if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not a date-time value.')
				else:
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	return valid_value_mask.to_list(), error_log_list

def check_has_value_format_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if the value format of column matches value format specified by HasValueFormatRule. 
	Function returns a list of boolean values (True => valid value, False => invalid value) and a list of error messages.
	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasValueFormatRule) : the HasValueFormatRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#Ingest provided value format for column in question.
	value_format_input = input_rule.value_format_input

	#initialize error_log_list.
	error_log_list = []
	is_valid_format_mask = df[input_column_name].apply(lambda x: h.is_valid_format(x, value_format_input))
	invalid_value_indices = is_valid_format_mask[is_valid_format_mask == False].index.to_list()
	if invalid_value_indices:
		for index in invalid_value_indices:
			if not pd.isnull(df[input_column_name][index]):
				error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not in the correct format.')
			else:
				error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')

	valid_value_mask = is_valid_format_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_unique_rule(df, input_column_name, input_rule, **kwargs):
	'''
	If 'is unique' flag is set check_is_unique_rule function checks if there are any 
	duplicated values in the column in question.
	Function returns list of with a single boolean value type (True => all unique values, False => duplicate values identified) and a list of error messages.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsUniqueRule) : the IsUniqueRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, a list with a single boolean value type that represents if column meets condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	duplicate_values_dict = defaultdict(list)
	
	if not df[input_column_name].is_unique:
		is_duplicated = df[input_column_name].duplicated(keep = False)
		series_of_duplicates = df[input_column_name][is_duplicated]
		no_null_series_of_duplicates = series_of_duplicates.dropna()
		for duplicate_item in no_null_series_of_duplicates.items():
			row_num = duplicate_item[0] + 1
			row_value = duplicate_item[1]
			duplicate_values_dict[row_value].append(row_num)
			
	for row_value in duplicate_values_dict.keys():
		for row_num in duplicate_values_dict[row_value]:
			error_log_list.append(f'Error: column {input_column_name}, row {row_num}: found duplicate value {row_value}.')
	
	col_is_unique = df[input_column_name].is_unique		
	valid_value_mask.extend([col_is_unique] * len(df))
	return valid_value_mask, error_log_list

def check_is_required_rule(df, input_column_name, input_rule, **kwargs):
	'''
	If 'is required' flag is set then check_is_required function checks if any column values are null. 
	Column name and row numbers are reported for any identified null values. 
	Refer to set_null_values function for information on what are considered to be null values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsRequiredRule) : the IsRequiredRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	input_column = df[input_column_name]
	is_not_null_mask = input_column.notnull()
	invalid_value_indices = is_not_null_mask[is_not_null_mask == False].index.to_list()
	for index_value in invalid_value_indices:
			error_log_list.append(f'Error: column {input_column_name}, row {index_value + 1}: found null value.')
	valid_value_mask = is_not_null_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_null_rule(df, input_column_name, input_rule, **kwargs):
	'''
	If 'is null' flag is set then function checks if any column values are not null. 
	Column name and row numbers are reported for any identified non-null values. 
	Refer to set_null_values function for information on what are considered to be null values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsNullRule) : the IsNullRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	input_column = df[input_column_name]
	is_null_mask = input_column.isnull()
	invalid_value_indices = is_null_mask[is_null_mask == False].index.to_list()
	for index_value in invalid_value_indices:
			error_log_list.append(f'Error: column {input_column_name}, row {index_value + 1}: found non-null value.')
	valid_value_mask = is_null_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_not_null_rule(df, input_column_name, input_rule, **kwargs):
	'''
	If 'is not null' flag is set then function checks if any column values are null. 
	Column name and row numbers are reported for any identified null values. 
	Refer to set_null_values function for information on what are considered to be null values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsNotNullRule) : the IsNotNullRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	input_column = df[input_column_name]
	is_null_mask = input_column.notnull()
	invalid_value_indices = is_null_mask[is_null_mask == False].index.to_list()
	for index_value in invalid_value_indices:
			error_log_list.append(f'Error: column {input_column_name}, row {index_value + 1}: found null value.')
	valid_value_mask = is_null_mask.to_list()
	return valid_value_mask, error_log_list

def check_value_in_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if values in column belong to the list of allowed values specified by the ValueInRule.
	Prints an error message with column name and row number for value if it is not in the list of allowed values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (ValueInRule) : the ValueInRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
 
	allowed_values_list = input_rule.value_in_input
	allowed_values_str_list = [str(s) for s in allowed_values_list]

	value_in_mask = df[input_column_name].apply(lambda x: x in allowed_values_str_list)
	invalid_value_indices = value_in_mask[value_in_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not in allowed values list.')
	valid_value_mask = value_in_mask.to_list()
	return valid_value_mask, error_log_list

def check_value_not_in_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if values in column belong to the list of disallowed values specified by the ValueNotInRule.
	Prints an error message with column name and row number for value if it is in the list of disallowed values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (ValueNotInRule) : the ValueInRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	disallowed_values = input_rule.value_not_in_input
	disallowed_values_str_list = [str(s) for s in disallowed_values]
	value_not_in_mask = df[input_column_name].apply(lambda x: x not in disallowed_values_str_list)
	invalid_value_indices = value_not_in_mask[value_not_in_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is in not allowed values list.')
	valid_value_mask = value_not_in_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_value_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is the same as value specified by the HasValueRule.
	Prints an error message with column name and row number for value not the same as allowed value.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasValueRule) : the HasValueRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	reference_value = input_rule.reference_value_input
	has_value_mask = df[input_column_name].apply(lambda x: x == reference_value)
	invalid_value_indices = has_value_mask[has_value_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not allowed.')
	valid_value_mask = has_value_mask.to_list()
	return valid_value_mask, error_log_list

def check_not_has_value_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is the same as  value specified by the NotHasValueRule.
	Prints an error message with column name and row number for value that is same as disallowed value.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (NotHasValueRule) : the NotHasValueRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	reference_value = input_rule.reference_value_input
	not_has_value_mask = df[input_column_name].apply(lambda x: x != reference_value)
	invalid_value_indices = not_has_value_mask[not_has_value_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not allowed.')
	valid_value_mask = not_has_value_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_equal_to_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is equal to value specified by the IsEqualToRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is not equal to allowed value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsEqualToRule) : the IsEqualToRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""

	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
	
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_equal_to_mask = no_separator_column_values.apply(lambda x: h.is_equal_to(test_value = x, reference_value = reference_value, tolerance_input = str(tolerance_input)))
	invalid_value_indices = is_equal_to_mask[is_equal_to_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not equal to {reference_value}.')

	valid_value_mask = is_equal_to_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_not_equal_to_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is equal to value specified by the IsNotEqualToRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is equal to disallowed value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsNotEqualToRule) : the IsNotEqualToRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
	
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_equal_to_mask = no_separator_column_values.apply(lambda x: h.is_not_equal_to(x, reference_value = reference_value, tolerance_input = tolerance_input))
	invalid_value_indices = is_equal_to_mask[is_equal_to_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is equal to {reference_value}.')

	valid_value_mask = is_equal_to_mask.to_list()

	return valid_value_mask, error_log_list

def check_is_greater_than_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is greater than value specified by the IsGreaterThanRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is not greater than to reference value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsGreaterThanRule) : the IsGreaterThanRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
		
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_greater_than_mask = no_separator_column_values.apply(lambda x: h.is_greater_than(x, reference_value = reference_value, tolerance_input = tolerance_input))
	invalid_value_indices = is_greater_than_mask[is_greater_than_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not greater than {reference_value}.')
				
	valid_value_mask = is_greater_than_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_greater_than_or_equal_to_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is greater than or equal to than value specified by the IsGreaterThanOrEqualToRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is not greater than or equal to reference value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsGreaterThanOrEqualToRule) : the IsGreaterThanOrEqualToRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
		
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_greater_than_or_equal_to_mask = no_separator_column_values.apply(lambda x: h.is_greater_than_or_equal_to(x, reference_value = reference_value, tolerance_input = tolerance_input))
	invalid_value_indices = is_greater_than_or_equal_to_mask[is_greater_than_or_equal_to_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not greater than or equal to {reference_value}.')
			
	valid_value_mask = is_greater_than_or_equal_to_mask.to_list()
	return valid_value_mask, error_log_list


def check_is_less_than_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is less than value specified by the IsLessThanRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is not less than the reference value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsLessThanRule) : the IsLessThanRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
		
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_less_than_mask = no_separator_column_values.apply(lambda x: h.is_less_than(x, reference_value = reference_value, tolerance_input = tolerance_input))
	invalid_value_indices = is_less_than_mask[is_less_than_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not less than {reference_value}.')
			
	valid_value_mask = is_less_than_mask.to_list()
	return valid_value_mask, error_log_list

def check_is_less_than_or_equal_to_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is less than or equal to than value specified by the IsLessThanOrEqualToRule.
	If a thousands separator has been set, then it is removed from the test value.
	If level of tolerance has been set, then tolerance is set to user's input, otherwise a default of 0.001 (3 decimal places) is used.
	Prints an error message with column name and row number for value that is not less than or equal to reference value.
	This rule is used to compare numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IsLessThanOrEqualToRule) : the IsLessThanOrEqualToRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	#Ingest provided value type and value format for column in question.
	reference_value = input_rule.reference_value_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	#ingest tolerance input, if provided, else set it to "0.001".
	tolerance_input = (
    getattr(kwargs.get('local_rules', {}).get('SetLocalToleranceRule'), 'local_tolerance_input', None)
    or getattr(kwargs.get('input_set_value_rules', {}).get('SetGlobalToleranceRule'), 'global_tolerance_input', None)
    or "0.001"
	)
		
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	is_less_than_or_equal_to_mask = no_separator_column_values.apply(lambda x: h.is_less_than_or_equal_to(x, reference_value = reference_value, tolerance_input = tolerance_input))
	invalid_value_indices = is_less_than_or_equal_to_mask[is_less_than_or_equal_to_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is null.')
					continue
				elif not h.is_numeric(no_separator_column_values[index]): # if separator removed value is not numeric, raise warning.
					error_log_list.append(f'Warning: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not numeric.')
					continue
				else:
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} is not less than or equal to {reference_value}.')

	valid_value_mask = is_less_than_or_equal_to_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_length_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column has length as specified by the HasLengthRule.
	Prints an error message with column name and row number for value not equal to specified length.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasLengthRule) : the HasLengthRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	length = input_rule.has_length_input
	has_length_mask = df[input_column_name].apply(lambda x: isinstance(x, str) and len(x) == length)
	invalid_value_indices = has_length_mask[has_length_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}:length of value {df[input_column_name][index]} is more than {length}.')
	valid_value_mask = has_length_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_min_length_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column has length greater than or equal to the minimum length specified by the HasMinLengthRule.
	Prints an error message with column name and row number for value not meeting length specification.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasMinLengthRule) : the HasMinLengthRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	length = input_rule.has_min_length_input
	has_min_length_mask = df[input_column_name].apply(lambda x: isinstance(x, str) and len(x) >= length)
	invalid_value_indices = has_min_length_mask[has_min_length_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}:length of value {df[input_column_name][index]} is more than {length}.')
	valid_value_mask = has_min_length_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_max_length_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column has length less than or equal to the maximum length specified by the HasMaxLengthRule.
	Prints an error message with column name and row number for value not meeting length specification.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasMaxLengthRule) : the HasMaxLengthRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	length = input_rule.has_max_length_input
	has_max_length_mask = df[input_column_name].apply(lambda x: isinstance(x, str) and len(x) <= length)
	invalid_value_indices = has_max_length_mask[has_max_length_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}:length of value {df[input_column_name][index]} is more than {length}.')
	valid_value_mask = has_max_length_mask.to_list()
	return valid_value_mask, error_log_list

def check_starts_with_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column starts with string specified by the StartsWithRule.
	Prints an error message with column name and row number for value not starting with specified value.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (StartsWithRule) : the StartsWithRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	#convert input value to string, in case a digit was the specified input value.
	error_log_list = []
	valid_value_mask = []
	starts_with_value = str(input_rule.starts_with_input)
	
	starts_with_mask = df[input_column_name].apply(lambda x: x.startswith(starts_with_value) if pd.notna(x) else False)
	invalid_value_indices = starts_with_mask[starts_with_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} does not start with {starts_with_value}.')
	valid_value_mask = starts_with_mask.to_list()
	return valid_value_mask, error_log_list

def check_ends_with_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column ends with string specified by the EndsWithRule.
	Prints an error message with column name and row number for value not ending with specified value.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (EndssWithRule) : the EndsWithRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	#convert input value to string, in case a digit was the specified input value.
	error_log_list = []
	valid_value_mask = []
	ends_with_value = str(input_rule.ends_with_input)
	
	ends_with_mask = df[input_column_name].apply(lambda x: x.endswith(ends_with_value) if pd.notna(x) else False)
	invalid_value_indices = ends_with_mask[ends_with_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} does not end with {ends_with_value}.')
	valid_value_mask = ends_with_mask.to_list()
	return valid_value_mask, error_log_list

def check_includes_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column contains string specified by the IncludesRule.
	Prints an error message with column name and row number for value that does not have the specified string as a substring.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (IncludesRule) : the IncludesRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	#convert input value to string, in case a digit was the specified input value.
	error_log_list = []
	valid_value_mask = []
	includes_value = str(input_rule.includes_input)
	
	includes_mask = df[input_column_name].apply(lambda x: includes_value in x if pd.notna(x) else False)
	invalid_value_indices = includes_mask[includes_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} does not include {includes_value}.')
	valid_value_mask = includes_mask.to_list()
	return valid_value_mask, error_log_list

def check_does_not_include_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column does not include string specified by the DoesNotIncludeRule.
	Prints an error message with column name and row number for value that has the specified string as a substring.
	This rule is used to compare non-numerical values.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (DoesNotIncludeRule) : the DoesNotIncludeRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	#convert input value to string, in case a digit was the specified input value.
	error_log_list = []
	valid_value_mask = []
	does_not_include_value = str(input_rule.does_not_include_input)
	
	does_not_include_mask = df[input_column_name].apply(lambda x: does_not_include_value not in x if pd.notna(x) else False)
	invalid_value_indices = does_not_include_mask[does_not_include_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: value {df[input_column_name][index]} includes {does_not_include_value}.')
	valid_value_mask = does_not_include_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_significant_digits_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column is a number with the number of significant digits specified by HasSignificantDigitsRule.
	Prints an error message with column name and row number for values with incorrect number of significant digits.
	Prints a warning message for values that are non-numeric.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasSignificantDigitsRule) : the HasSignificantDigitsRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	#Ingest number of significant digits for column in question.
	significant_digits_input = input_rule.significant_digits_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	significant_digit_mask = no_separator_column_values.apply(lambda x: h.count_significant_digits(x) == significant_digits_input if h.is_numeric(x) else False )
	invalid_value_indices = significant_digit_mask[significant_digit_mask == False].index.to_list()

	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: for value {df[input_column_name][index]} significant digits not equal to {significant_digits_input}.')
	
	valid_value_mask = significant_digit_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_decimal_places_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column has the number of decimal places specified by HasDecimalPlacesRule.
	Prints an error message with column name and row number for values with incorrect number of significant digits.
	Prints a warning message for values that are non-numeric.

	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasDecimalPlacesRule.) : the HasDecimalPlacesRule. object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	#Ingest number of decimal places for column in question.
	decimal_places_input = input_rule.decimal_places_input

	#ingest the thousands separator, if provided, else set it to "".
	try:
		separator = kwargs['input_set_value_rules']['ThousandsSeparatorRule'].separator_input
	except:
		separator = ""
	
	no_separator_column_values = df[input_column_name].apply(lambda x: str(x).replace(separator,"") if not pd.isnull(x) else x)
	decimal_places_mask = no_separator_column_values.apply(lambda x: h.count_decimal_places(x) == decimal_places_input if h.is_numeric(x) else False )
	invalid_value_indices = decimal_places_mask[decimal_places_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}: for value {df[input_column_name][index]} number of decimal places not equal to {decimal_places_input}.')

	valid_value_mask = decimal_places_mask.to_list()
	return valid_value_mask, error_log_list

def check_has_pattern_rule(df, input_column_name, input_rule, **kwargs):
	'''
	Checks if each value in column matches the pattern specified by the HasPatternRule.
	Prints an error message with column name and row number for value not matching specified pattern.
	
	Args:
		df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
		input_rule (HasPatternRule) : the HasPatternRule object.
		input_column_name (str) : the name of the column for which data is being validated.
		
	Returns:
		list: valid_values_mask, list of boolean values that represent if column values meet condition.
		list: error_log_list, the list of error messages.
	'''
	#initialize error_log_list and valid_value_mask.
	error_log_list = []
	valid_value_mask = []
	
	pattern = input_rule.regex_input
	clean_pattern = pattern.strip('/')
	regex_pattern = re.compile(clean_pattern)
	
	has_pattern_mask = df[input_column_name].apply(lambda x: bool(regex_pattern.fullmatch(x)) if pd.notnull(x) else False)
	invalid_value_indices = has_pattern_mask[has_pattern_mask == False].index.to_list()
	
	if invalid_value_indices:
			for index in invalid_value_indices:
				if not pd.isnull(df[input_column_name][index]):
					error_log_list.append(f'Error: column {input_column_name}, row {index +1}:Value {df[input_column_name][index]} does not match {pattern}.')
	valid_value_mask = has_pattern_mask.to_list()
	return valid_value_mask, error_log_list

'''
Initialize function dictionary for checking each type of InColumnValueRule.
There is a setter or checker function for each rule in RuleSet (only the ThousandsSeparatorRule does not have a setter function; its separator value
is used by other functions).
If a new rule is added to RuleSet, a new setting/checking function should be written. The new function should be added to the appropriate
function dictionary - set_value_rule_dict; column_rule_checker_dict; in_column_value_rule_checker_dict.
Code that imports this module can use the in_column_value_rule_checker_dict to call the appropriate rule checker function.
'''

in_column_value_rule_checker_dict = {}

in_column_value_rule_checker_dict["HasValueTypeRule"] = check_has_value_type_rule

in_column_value_rule_checker_dict["HasValueFormatRule"] = check_has_value_format_rule

in_column_value_rule_checker_dict["IsUniqueRule"] = check_is_unique_rule

in_column_value_rule_checker_dict["IsRequiredRule"] = check_is_required_rule

in_column_value_rule_checker_dict["IsNullRule"] = check_is_null_rule

in_column_value_rule_checker_dict["IsNotNullRule"] = check_is_not_null_rule

in_column_value_rule_checker_dict["HasPatternRule"] = check_has_pattern_rule

in_column_value_rule_checker_dict["ValueInRule"] = check_value_in_rule

in_column_value_rule_checker_dict["ValueNotInRule"] = check_value_not_in_rule

in_column_value_rule_checker_dict["HasValueRule"] = check_has_value_rule

in_column_value_rule_checker_dict["NotHasValueRule"] = check_not_has_value_rule

in_column_value_rule_checker_dict["IsEqualToRule"] = check_is_equal_to_rule

in_column_value_rule_checker_dict["IsNotEqualToRule"] = check_is_not_equal_to_rule

in_column_value_rule_checker_dict["IsGreaterThanRule"] = check_is_greater_than_rule

in_column_value_rule_checker_dict["IsLessThanRule"] = check_is_less_than_rule

in_column_value_rule_checker_dict["IsGreaterThanOrEqualToRule"] = check_is_greater_than_or_equal_to_rule

in_column_value_rule_checker_dict["IsLessThanOrEqualToRule"] = check_is_less_than_or_equal_to_rule

in_column_value_rule_checker_dict["HasLengthRule"] = check_has_length_rule

in_column_value_rule_checker_dict["HasMinLengthRule"] = check_has_min_length_rule

in_column_value_rule_checker_dict["HasMaxLengthRule"] = check_has_max_length_rule

in_column_value_rule_checker_dict["StartsWithRule"] = check_starts_with_rule

in_column_value_rule_checker_dict["EndsWithRule"] = check_ends_with_rule

in_column_value_rule_checker_dict["IncludesRule"] = check_includes_rule

in_column_value_rule_checker_dict["DoesNotIncludeRule"] = check_does_not_include_rule

in_column_value_rule_checker_dict["HasSignificantDigitsRule"] = check_has_significant_digits_rule

in_column_value_rule_checker_dict["HasDecimalPlacesRule"] = check_has_decimal_places_rule