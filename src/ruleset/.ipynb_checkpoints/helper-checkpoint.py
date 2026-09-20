import sys
import pandas as pd
import re
from dateutil.parser import parse
from pandas._libs.parsers import STR_NA_VALUES
from collections import defaultdict

def summarize_infile(df, file_name, **kwargs):
    '''
    Provides a summary of input file: number of rows, columns and number of missing/null values.
    Args:
        df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
        file_name (str): name of file being validated.

    Returns:
        dict: a dictionary with summary data.

    '''
    rows, columns = df.shape
    summary = {
        "File Name": file_name,
        "Rows": rows, 
        "Columns": columns,
        "Missing Values": df.isnull().sum().to_dict(),
    }
    return summary

def is_datetime(test_value, **kwargs):
    '''
    Checks if given input string represents a date-time value. Null strings are ignored.

    Args:
        test_value (str): The input to check.

    Returns:
        bool: True if the input represents a date-time value, False otherwise.
    '''
    if not pd.isnull(test_value):
        try:
            parse(test_value, fuzzy=False)
            return True
        except ValueError:
            return False

def is_valid_format(test_value, input_format, **kwargs):
    '''
    Validates whether a given input string matches a specified format. Null strings are ignored.

    Args:
        test_value (str): The input string to validate.
        input_format (str): The expected format (e.g., 'YYYY-MM-DD', 'MM/DD/YYYY', etc.).

    Returns:
        bool: True if the input string matches the specified format, False otherwise.
    '''
    if not pd.isnull(test_value):
        format_regex_dict = {
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

        return bool(re.match(format_regex_dict[input_format], test_value))

def is_floating_point(test_value, **kwargs):
    '''
    Checks if given input string represents a floating-point number. Null strings are ignored.
    Thousands separator is taken in to account if it is passed as a 'separator' parameter.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a floating-point number, False otherwise.
    '''
    if not pd.isnull(test_value):
        if 'separator' in kwargs:
            test_value = test_value.replace(kwargs['separator'], "")
        float_pattern = r'^[-+]?\d*\.\d+$'
        return bool(re.match(float_pattern, test_value))

def is_integer(test_value, **kwargs):
    '''
    Checks if given input string represents an integer. Null strings are ignored.
    Thousands separator is taken in to account if it is passed as a 'separator' parameter.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents an integer, False otherwise.
    '''
    if not pd.isnull(test_value):
        if 'separator' in kwargs:
            test_value = test_value.replace(kwargs['separator'], "")
        integer_pattern = r'^[-+]?\d+$'
        return bool(re.match(integer_pattern, test_value))

def is_numeric(test_value, **kwargs):
    '''
    Checks if given input string represents a number. Null strings are ignored.
    Thousands separator is taken in to account if it is passed as a 'separator' parameter.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a number, False otherwise.
    '''
    if not pd.isnull(test_value):
        try:
            float(test_value)
            return True
        except (ValueError, TypeError):
            return False
    else:
        return False

def is_equal_to(test_value, reference_value, **kwargs):
    '''
    Compares two values to check if they are equal after converting them to integers. Null values are ignored
    If the conversion fails or either value is null, the function returns `False`.
    Note: this function can be applied across to dataframe columns to check for row-wise equality of column values.

    Args:
        test_value (str or numeric): The first value to compare.
        reference_value (str or numeric): The second value to compare.

    Returns:
        bool: True if both values are equal after conversion to integers, False otherwise.
    '''
    if not pd.isnull(test_value) and not pd.isnull(reference_value):
        try:
            return bool(float(test_value) == float(reference_value))
        except:
            return False

def is_greater_than(test_value, reference_value, **kwargs):
    '''
    Compares two values to check if test value is greater than reference value after converting both to integers. Null values are ignored
    If the conversion fails or either value is null, the function returns `False`.
    Note: this function can be applied across to dataframe columns to check for row-wise equality of column values.

    Args:
        test_value (str or numeric): The first value to compare.
        reference_value (str or numeric): The second value to compare.

    Returns:
        bool: True if inequality condition after conversion to integers, False otherwise.
    '''
    if not pd.isnull(test_value) and not pd.isnull(reference_value):
        try:
            return bool(float(test_value) > float(reference_value))
        except:
            return False

def is_greater_than_or_equal_to(test_value, reference_value, **kwargs):
    '''
    Compares two values to check if test value is greater than or equal to reference value after converting both to integers. Null values are ignored
    If the conversion fails or either value is null, the function returns `False`.
    Note: this function can be applied across to dataframe columns to check for row-wise equality of column values.

    Args:
        test_value (str or numeric): The first value to compare.
        reference_value (str or numeric): The second value to compare.

    Returns:
        bool: True if inequality condition holds after conversion to integers, False otherwise.
    '''
    if not pd.isnull(test_value) and not pd.isnull(reference_value):
        try:
            return bool(float(test_value) >= float(reference_value))
        except:
            return False

def is_less_than(test_value, reference_value, **kwargs):
    '''
    Compares two values to check if test value is less than reference value after converting both to integers. Null values are ignored
    If the conversion fails or either value is null, the function returns `False`.
    Note: this function can be applied across to dataframe columns to check for row-wise equality of column values.

    Args:
        test_value (str or numeric): The first value to compare.
        reference_value (str or numeric): The second value to compare.

    Returns:
        bool: True if inequality condition holds after conversion to integers, False otherwise.
    '''
    if not pd.isnull(test_value) and not pd.isnull(reference_value):
        try:
            return bool(float(test_value) < float(reference_value))
        except:
            return False

def is_less_than_or_equal_to(test_value, reference_value, **kwargs):
    '''
    Compares two values to check if test value is less than or equal to reference value after converting both to integers. Null values are ignored
    If the conversion fails or either value is null, the function returns `False`.
    Note: this function can be applied across to dataframe columns to check for row-wise equality of column values.

    Args:
        test_value (str or numeric): The first value to compare.
        reference_value (str or numeric): The second value to compare.

    Returns:
        bool: True if inequality condition holds after conversion to integers, False otherwise.
    '''
    if not pd.isnull(test_value) and not pd.isnull(reference_value):
        try:
            return bool(float(test_value) <= float(reference_value))
        except:
            return False

def is_scientific_notation(test_value, **kwargs):
    '''
    Checks if given input string represents a number in scientific notation. Null strings are ignored.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a number in scientific notation, False otherwise.
    '''
    if not pd.isnull(test_value):
        scientific_notation_pattern = r'^[+-]?\d+(\.\d+)?[eE][+-]?\d+$'
        return bool(re.match(scientific_notation_pattern, test_value))

def is_complex(test_value, **kwargs):
    '''
    Checks if given input string represents a complex number. Null strings are ignored.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a complex number, False otherwise.
    '''
    
    if not pd.isnull(test_value):
        complex_number_pattern = r'^[+-]?(\d+(\.\d+)?|(\.\d+))[+-](\d+(\.\d+)?|(\.\d+))j$'
        return bool(re.match(complex_number_pattern, test_value))

def is_string(test_value, **kwargs):
    '''
    Checks if given input string represents a non-numerical, non-boolean, non-date-time string. Null strings are ignored.
    
    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a non-numerical, non-boolean, non-date-time string, False otherwise.
    '''
    if not pd.isnull(test_value):
        if is_integer(test_value) or is_floating_point(test_value) or is_datetime(test_value) or is_scientific_notation(test_value) or is_complex(test_value) or is_boolean(test_value):
            return False
        else:
            return True

def is_boolean(test_value, **kwargs):
    '''
    Checks if given input string represents a boolean value. Check is performed only on strings with non-null values.

    Args:
        test_value (str): The input to check. Can be a string or any value.

    Returns:
        bool: True if the input represents a boolean value, False otherwise.
    '''
    if not pd.isnull(test_value):
        return test_value in ['True', 'False', 'true', 'false', 'TRUE', 'FALSE']

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
        str_num = "{:.16g}".format(float(test_value))  # Avoid floating-point issues
        str_num = str_num.lstrip("0").rstrip("0").replace(".", "")
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
        return len(str_num.split('.')[1].rstrip('0'))
    return 0

