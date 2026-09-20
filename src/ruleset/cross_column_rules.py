import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
from collections import defaultdict
from ruleset import helper as h
from ruleset import set_value_rules as s
from ruleset import column_rules as c
from ruleset import in_column_value_rules as i

def validate_rule(rule_name, df, input_column_name, input_rule, input_set_value_rules, input_column_rules, input_column_value_rules):
	valuerules_list = input_rule.valuerules
	if len(valuerules_list) > 1:
		ruleset_message = f'Conditional rule {rule_name} is invalid. Only one atomic rule per column is allowed.\n'
		return ruleset_message
	else:
		value_rule = valuerules_list[0]
		value_rule_name = type(value_rule).__name__
		if i.in_column_value_rule_checker_dict[value_rule_name]:
			[ruleset_message_booleans, ruleset_message_errors] = i.in_column_value_rule_checker_dict[value_rule_name](df = df, input_rule = value_rule, input_column_name = input_column_name, input_set_value_rules = input_set_value_rules, input_column_rules = input_column_rules, input_column_value_rules = input_column_value_rules)
			ruleset_boolean_dict = {index + 1: value for index, value in enumerate(ruleset_message_booleans)}
		return ruleset_boolean_dict