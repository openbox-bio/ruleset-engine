import sys
import pandas as pd
import re
from dateutil.parser import parse
from datetime import datetime
from pandas._libs.parsers import STR_NA_VALUES
from collections import defaultdict
from decimal import *

DATETIME_FORMATS = [
	"%Y",
	"%Y-%m-%d",
	"%m-%d-%Y",
	"%d-%m-%Y",
	"%Y/%m/%d",
	"%m/%d/%Y",
	"%d/%m/%Y",
	"%Y.%m.%d",
	"%m.%d.%Y",
	"%d.%m.%Y",
	"%Y%m%d",
	"%H:%M:%S",
	"%H:%M",
	"%I:%M:%S %p",
	"%I:%M %p",
	"%H%M%S",
	"%Y-%m-%d %H:%M:%S",
	"%Y-%m-%dT%H:%M:%S",
	"%Y-%m-%d %H:%M",
	"%Y-%m-%dT%H:%M",
	"%d/%m/%Y %H:%M:%S",
	"%m-%d-%Y %I:%M:%S %p",
	"%Y/%m/%d %H:%M:%S",
	"%Y-%m-%dT%H:%M:%S.%fZ",
	"%Y-%m-%dT%H:%M:%S%z",
]

def is_datetime(test_value, **kwargs):

	if pd.isna(test_value) or isinstance(test_value, bool):
		return False

	if not isinstance(test_value, str):
		return False

	for fmt in DATETIME_FORMATS:
		try:
			datetime.strptime(test_value, fmt)
			return True
		except ValueError:
			continue

	return False

def is_valid_format(test_value, input_format, **kwargs):
	'''
	Validates whether a given input string matches a specified format. Null strings return False.

	Args:
		test_value (str): The input string to validate.
		input_format (str): The expected format (e.g., 'YYYY-MM-DD', 'MM/DD/YYYY', etc.).

	Returns:
		bool: True if the input string matches the specified format, False otherwise.
	'''
	if not pd.isnull(test_value) and not isinstance(test_value, bool):
		format_regex_dict = {
		"YYYY": r"^\d{4}$",
		"YYYY-MM-DD": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$",
		"MM-DD-YYYY": r"^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])-\d{4}$",
		"DD-MM-YYYY": r"^(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])-\d{4}$",
		"YYYY/MM/DD": r"^\d{4}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])$",
		"MM/DD/YYYY": r"^(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])/\d{4}$",
		"DD/MM/YYYY": r"^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4}$",
		"YYYY.MM.DD": r"^\d{4}\.(0[1-9]|1[0-2])\.(0[1-9]|[1-2][0-9]|3[0-1])$",
		"MM.DD.YYYY": r"^(0[1-9]|1[0-2])\.(0[1-9]|[1-2][0-9]|3[0-1])\.\d{4}$",
		"DD.MM.YYYY": r"^(0[1-9]|[1-2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.\d{4}$",
		"YYYYMMDD": r"^\d{4}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])$",
		"HH:mm:ss": r"^([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
		"HH:mm": r"^([01][0-9]|2[0-3]):[0-5][0-9]$",
		"hh:mm:ss AM/PM": r"^(0[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$",
		"hh:mm AM/PM": r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$",
		"HHmmss": r"^([01][0-9]|2[0-3])[0-5][0-9][0-5][0-9]$",
		"YYYY-MM-DD HH:mm:ss": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
		"YYYY-MM-DDTHH:mm:ss": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
		"YYYY-MM-DD HH:mm": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([01][0-9]|2[0-3]):[0-5][0-9]$",
		"YYYY-MM-DDTHH:mm": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]$",
		"DD/MM/YYYY HH:mm:ss": r"^(0[1-9]|[1-2][0-9]|3[0-1])/(0[1-9]|1[0-2])/\d{4} ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
		"MM-DD-YYYY hh:mm:ss AM/PM": r"^(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])-\d{4} (0[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$",
		"YYYY/MM/DD HH:mm:ss": r"^\d{4}/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1]) ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$",
		"YYYY-MM-DDTHH:mm:ss.sssZ": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\.\d{3}Z$",
		"YYYY-MM-DDTHH:mm:ss+hh:mm": r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\+([01][0-9]|2[0-3]):[0-5][0-9]$"
		}

		clean_input_format = input_format.strip('"')
		try:
			return bool(re.match(format_regex_dict[clean_input_format], test_value))
		except KeyError:
			return False
	else:
		return False

def is_floating_point(test_value, **kwargs):
	'''
	Checks if given input string represents a floating-point number. Null strings and Booleans return False.
	Thousands separator is taken in to account if it is passed as a 'separator' parameter.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a floating-point number, False otherwise.
	'''
	if pd.isnull(test_value) or isinstance(test_value, bool) or isinstance(test_value, datetime):
		return False
	else:
		test_value_string = str(test_value)
		if 'separator' in kwargs:
			test_value_string = test_value_string.replace(kwargs['separator'], "")
		integer_pattern = r'^[-+]?\d*\.\d+$'
		return bool(re.match(integer_pattern, test_value_string))

def is_integer(test_value, **kwargs):
	'''
	Checks if given input string represents an integer. Null strings, Booleans, Date-time objects return False.
	Thousands separator is taken in to account if it is passed as a 'separator' parameter.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents an integer, False otherwise.
	'''
	if pd.isnull(test_value) or isinstance(test_value, bool) or isinstance(test_value, datetime):
		return False
	else:
		test_value_string = str(test_value)
		if 'separator' in kwargs:
			test_value_string = test_value_string.replace(kwargs['separator'], "")
		integer_pattern = r'^[-+]?\d+$'
		return bool(re.match(integer_pattern, test_value_string))

def is_numeric(test_value, **kwargs):
	'''
	Checks if given input string represents a number. Null strings, Booleans, Date-time objects return False.
	Thousands separator is taken in to account if it is passed as a 'separator' parameter.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a number, False otherwise.
	'''
	if pd.isnull(test_value) or isinstance(test_value, bool) or isinstance(test_value, datetime):
		return False
	else:
		try:
			float(test_value)
			return True
		except (ValueError, TypeError):
			return False

def is_equal_to(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if they are equal after converting both to Decimal objects. Null values return False.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str ): The first value to compare.
		reference_value (str): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two numbers, default = 0.001.

	Returns:
		bool: True if both values are equal after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			return abs(test_value_decimal - reference_value_decimal) <= tolerance
		except:
			return False
	else:
		return False

def is_not_equal_to(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if they are equal after converting both to Decimal objects. Null values return False.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str ): The first value to compare.
		reference_value (str): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two number, default = 0.001.

	Returns:
		bool: True if test value is not equal to reference value after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			
			return abs(test_value_decimal - reference_value_decimal) > tolerance
		except:
			return False
	else:
		return False

def is_greater_than(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if test value is greater than reference value after converting both to Decimal objects. Null values return `False`.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str): The first value to compare.
		reference_value (str): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two number, default = 0.001.

	Returns:
		bool: True if inequality condition holds after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			return (test_value_decimal - reference_value_decimal) > tolerance
		except:
			return False
	else:
		return False

def is_greater_than_or_equal_to(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if test value is greater than or equal to reference value after converting both to Decimal objects. Null values return `False`.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str): The first value to compare.
		reference_value (str): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two number, default = 0.001.

	Returns:
		bool: True if inequality condition holds after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			return (test_value_decimal >=  reference_value_decimal - tolerance)
		except:
			return False
	else:
		return False

def is_less_than(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if test value is less than reference value after converting both to Decimal objects. Null values are ignored.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str): The first value to compare.
		reference_value (str): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two number, default = 0.001.

	Returns:
		bool: True if inequality condition holds after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			return (test_value_decimal < reference_value_decimal - tolerance)
		except:
			return False
	else:
		return False

def is_less_than_or_equal_to(test_value, reference_value, tolerance_input, **kwargs):
	'''
	Compares two values to check if test value is less than or equal to reference value after converting both to Decimal objects. Null values are ignored.
	If conversion fails function returns `False`.
	Note: this function can be applied across two dataframe columns to check for row-wise equality of column values.

	Args:
		test_value (str or numeric): The first value to compare.
		reference_value (str or numeric): The second value to compare.
		tolerance_input (str): The level of tolerance at which to compare the two number, default = 0.001.

	Returns:
		bool: True if inequality condition holds after conversion to decimal objects, False otherwise.
	'''
	if not pd.isnull(test_value) and not pd.isnull(reference_value):
		try:
			test_value_decimal = Decimal(test_value)
			reference_value_decimal = Decimal(reference_value)
			tolerance = Decimal(tolerance_input)
			return (test_value_decimal <= reference_value_decimal + tolerance)
		except:
			return False
	else:
		return False

def is_scientific_notation(test_value, **kwargs):
	'''
	Checks if given input string represents a number in scientific notation. Null strings, Booleans and date-time objects return False.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a number in scientific notation, False otherwise.
	'''
	if not pd.isnull(test_value) or not isinstance(test_value, bool) or not isinstance(test_value, datetime):
		test_value_string = str(test_value)
		scientific_notation_pattern = r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$'
		return bool(re.match(scientific_notation_pattern, test_value_string))
	else:
		return False

def is_complex(test_value, **kwargs):
	'''
	Checks if given input string represents a complex number. Null strings, Booleans and date-time objects return False.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a complex number, False otherwise.
	'''
	
	if not pd.isnull(test_value) or not isinstance(test_value, bool) or not isinstance(test_value, datetime):
		test_value_string = str(test_value)
		complex_number_pattern = r'^[+-]?(\d+(\.\d+)?|(\.\d+))[+-](\d+(\.\d+)?|(\.\d+))j$'
		return bool(re.match(complex_number_pattern, test_value_string))
	else:
		return False

def is_string(test_value, **kwargs):
	'''
	Checks if given input string represents a non-numerical, non-boolean, non-date-time string. Null strings return False.
	
	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a non-numerical, non-boolean, non-date-time string, False otherwise.
	'''
	if not pd.isnull(test_value):
		if is_integer(test_value):
			return False
		elif is_floating_point(test_value):
			return False
		elif is_datetime(str(test_value)):
			return False
		elif is_scientific_notation(test_value):
			return False
		elif is_complex(test_value):
			return False
		elif is_boolean(test_value):
			return False
		elif isinstance(test_value, str):
			return True
	else:
		return False

def is_boolean(test_value, **kwargs):
	'''
	Checks if given input string represents a boolean value. Check is performed only on strings with non-null values. Null strings return False.

	Args:
		test_value (str): The input to check. Can be a string or any value.

	Returns:
		bool: True if the input represents a boolean value, False otherwise.
	'''
	if not pd.isnull(test_value):
		return test_value in ['True', 'False', 'true', 'false', 'TRUE', 'FALSE']
	else:
		return False

def count_significant_digits(test_value):
	'''
	Returns the number of significant digits for a numeric value. 

	Args:
		test_value (str): The input to check, a numeric value.

	Returns:
		int: The number of significant digits in the input numeric value.
	'''
	if float(test_value) == 0.0:
		return 0
	
	# Convert to string and remove leading/trailing zeros and decimal point
	try:
		str_num = test_value.strip().lower()

		#remove signficand from exponent
		if 'e' in str_num:
			str_num = str_num.split('e')[0]

		#remove sign
		str_num = str_num.lstrip('+-')

		#For decimal number do..
		if '.' in str_num:
			str_num = str_num.replace('.', '')
			str_num = str_num.lstrip('0')
			return len(str_num)
		#For integer do...
		else:
			#remove leading zeros
			str_num = str_num.lstrip('0')

			#remove trailing zeros (not significant without decimal point)
			str_num = str_num.rstrip('0')
			return len(str_num)

	except (ValueError, TypeError):
		return 0

def count_decimal_places(test_value):
	'''
	Returns the number of decimal places for a numeric value. 

	Args:
		test_value (float, int): The input to check, a numeric value.

	Returns:
		int: The number of decimal places in the input numeric value.
	'''
	str_num = str(test_value)
	if '.' in str_num:
		return len(str_num.split('.')[1])
	return 0

