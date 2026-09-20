import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
from collections import defaultdict

def set_custom_null_values(input_rule, **kwargs):
    '''
    Update the default pandas null values list with any null values supplied in the rules file.
    
    Args:
        input_rule (NullValuesRule): a NullValuesRule object.

    Returns:
        set: the union set of the default pandas null values and allowed null values 
    '''
    return STR_NA_VALUES.union(set(input_rule.allowed_null_values_list))


'''
Initialize function dictionaries for setting each type of SetValueRule.
There is a setter function for each SetValueRule in RuleSet (only the ThousandsSeparatorRule does not have a setter function; its separator value
is used by other functions).
If a new rule is added to RuleSet, a new setting function should be written. The new function should be added to set_values_rule_dict.
'''
set_values_dict = {}

set_values_dict["SetNullValuesRule"] = set_custom_null_values