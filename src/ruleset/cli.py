import sys
import os
from importlib.resources import files
from textx import get_location, TextXSyntaxError
from textx.metamodel import metamodel_from_file
import pandas as pd
from collections import Counter
from collections import defaultdict
from pandas._libs.parsers import STR_NA_VALUES
from ruleset import set_value_rules as s
from ruleset import column_rules as c
from ruleset import in_column_value_rules as i
from ruleset import cross_column_rules as cc
from datetime import datetime
import argparse

'''
Declare global variables.
'''
REFERENCE_FILE = ""
RULES_FILE = ""
DATA_FILE = ""
TIMESTAMP = ""
LOGFILE = ""
LOGFILEPATH = ""
set_value_rules_dict = {}
column_rules_dict = {}
column_names_list = []
block_rules_list = []
column_value_rules_dict = {}
conditional_rules_list = []
all_na_values = ""
data_df = ""
data_columns_with_rules = []
master_column_value_rules_dict = defaultdict(list)
master_local_value_rules_dict = defaultdict(list)

def get_grammar_path():
	'''
	Locate RuleSet.tx as packaged inside the installed `ruleset` package,
	rather than requiring the user to pass its path on the command line.
	'''
	return str(files('ruleset').joinpath('RuleSet.tx'))

def create_logfile():
	global TIMESTAMP
	global LOGFILE
	TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") # record date and time when run starts in TIMESTAMP.
	if not os.path.exists(LOGFILEPATH):
		os.makedirs(LOGFILEPATH)
	logfile_name = LOGFILEPATH + "/" + TIMESTAMP + "_ruleset.log"
	LOGFILE = open(logfile_name, "w")
	return

def read_rules_file():
	'''
	Read the Ruleset metamodel from metamodel file.
	Read the rules file.
	Parse rules into the rules dictionaries- key= rule name; value = rule object.
	'''
	global set_value_rules_dict
	global column_rules_dict
	global column_value_rules_dict
	global conditional_rules_list
	global block_rules_list

	try:

		metamodel_infile = REFERENCE_FILE
		mm = metamodel_from_file(metamodel_infile, autokwd=True)
	except FileNotFoundError as err:
		LOGFILE.write(f'Error: Cannot find {REFERENCE_FILE} to create RuleSet metamodel.')
	except PermissionError as p:
		LOGFILE.write(f"Error: Permission denied for {REFERENCE_FILE}.") 
		
	try:
		data_rules = mm.model_from_file(RULES_FILE)
		LOGFILE.write(f'Info: Rules File {RULES_FILE} is OK.\n')
	except TextXSyntaxError as err:
		LOGFILE.write(f'Error: Syntax Error found in {err.filename} in line {err.line}, column {err.col}\n')
		sys.exit()
	except FileNotFoundError as err:
		LOGFILE.write(f'Error: {RULES_FILE} is not a valid path to the Rules file.')
		sys.exit()

	set_value_rules_dict = {type(rule).__name__: rule for rule in data_rules.set_value_rules}
	column_rules_dict = {type(rule).__name__: rule for rule in data_rules.column_rules}
	column_value_rules_dict = {rule.column_name.name: rule for rule in data_rules.column_value_rules}
	conditional_rules_list= data_rules.conditional_rules
	block_rules_list = data_rules.block_rules
	
	return

def validate_rules_file():
	'''
	Validate rules file. 
	Checks:
	(a) Check if list of column names exists. If not, then log error message and exit.
	(b) Check if each column in the column names list has an associated set of value rules in the master_column_value_rules_dict.
	(b) Check if each column with at least one value rule is listed in the columns list.
	'''
	global column_names_list
	try:
		column_names_list = [column.name for column in column_rules_dict['ColumnListRule'].column_names_list]
	except KeyError as err:
		LOGFILE.write("Error: A list of column names is required in the rules file. Please enter a list of column names and try again." + "\n" + "Exiting ruleset-engine.\n")
		sys.exit()
		
	if column_value_rules_dict.keys():
		column_names_set = set(column_names_list) #create set of the list of column names
		columns_in_column_value_rules = master_column_value_rules_dict.keys()
		columns_in_column_value_rules_set = set(columns_in_column_value_rules) #create set of all column names with at least one value rule.
		
		columns_with_no_value_rules = column_names_set - columns_in_column_value_rules_set #create set with columns that have no value rules.
		columns_not_in_columns_list = columns_in_column_value_rules_set - column_names_set #create set of columns with value rule(s) but that are not included in list of column names.
		
		if (len(columns_with_no_value_rules) == 0):
			LOGFILE.write("Info: All columns in columns list have associated value rules.\n")
		else:
			for column_name in columns_with_no_value_rules:
				LOGFILE.write(f'Warning: Column {column_name} has no associated value rules.\n')
		
		if (len(columns_not_in_columns_list) == 0):
			LOGFILE.write("Info: All columns with at least one value rule are included in the columns list.\n")
		else:
			for column_name in columns_not_in_columns_list:
				LOGFILE.write(f'Warning: Column {column_name} has value rules, but is not in columns list.\n')
	else:
		LOGFILE.write('Warning: No column value rules included in rules file.\n')

	return

def set_na_values():
	'''
	If null values list has been specified then a NullValuesRule object will be included in the rules file.
	Use the set_custom_null_values to extract the null values list and add it to the default na values 
	list to create the all_na_values list. Delete rule as it does not have to be run again.
	If no NullValuesRule has been specified then the default na values list is assigned to all_na_values.
	'''

	global all_na_values
	try:
		input_rule = set_value_rules_dict['SetNullValuesRule']
		input_rule_name = type(input_rule).__name__
		all_na_values = s.set_values_dict[input_rule_name](input_rule)
	except:
		all_na_values = STR_NA_VALUES

	return

def summarize_data_file():
	'''
	Provides a summary of input file: number of rows, columns and number of missing/null values.
	'''
	rows, columns = data_df.shape
	summary = {
		"Rows": rows, 
		"Columns": columns,
		"Missing Values": data_df.isnull().sum().to_dict(),
	}
	LOGFILE.write(f"Info: Rows:{summary['Rows']}\n")
	LOGFILE.write(f"Info: Columns:{summary['Columns']}\n")
	LOGFILE.write(f"Info: Missing Values:\n") if summary['Missing Values'] else LOGFILE.write(f"\n")
	for (key,value) in summary['Missing Values'].items():
		LOGFILE.write(f"Info: Missing value count for {key}: {value}\n")
	return

def read_data_file():
	'''
	Read input file with data to be validated. 
	all_na_values includes the na values, in addition to the list of na values accepted by pandas, specified in rules file.
	Create a pandas dataframe from parsed data input file.
	If read is successful, print summary of data file to log file.
	'''

	global data_df

	if not os.path.exists(DATA_FILE):
			raise FileNotFoundError(f"File does not exist: {DATA_FILE}")

	try:
		data_df = pd.read_csv(DATA_FILE, dtype = object, na_values = all_na_values, skip_blank_lines=False)
		LOGFILE.write(f"Info: Data file {DATA_FILE} parsed as csv.\n")
		summarize_data_file()
		return data_df
	except Exception:
		pass

	try:
		data_df = pd.read_csv(DATA_FILE, sep = "\t", dtype = object, na_values = all_na_values, skip_blank_lines=False)
		LOGFILE.write(f"Info: Data file {DATA_FILE} parsed as tsv.\n")
		summarize_data_file()
		return data_df
	except Exception:
		pass

	try:
		data_df = pd.read_excel(DATA_FILE, dtype = object, na_values = all_na_values)
		LOGFILE.write(f"Info: Data file {DATA_FILE} parsed as Excel.\n")
		summarize_data_file()
		return data_df
	except Exception:
		pass

	# If all formats fail, log the error
	try:
		raise ValueError(f"Bad file format for {DATA_FILE}.")
	except ValueError:
		LOGFILE.write(f"Bad file format for {DATA_FILE}.\n")
		raise

def gather_column_value_rules():
	'''
	Rules for each column may be included in a rule block, or as a single column value rule.
	This function gathers and arranges all the rules by column name in the master_column_value_rules_dict.
	'''
	global master_column_value_rules_dict
	global master_local_value_rules_dict

	for block_rule in block_rules_list:
		column_names_in_block_rule = [column_name.name for column_name in block_rule.block_rule_column_names_list]
		for name in column_names_in_block_rule:
			master_column_value_rules_dict[name].extend(block_rule.valuerules)
			master_local_value_rules_dict[name].extend(block_rule.setlocalrules)

	for name in column_value_rules_dict.keys():
		master_column_value_rules_dict[name].extend(column_value_rules_dict[name].valuerules)
		master_local_value_rules_dict[name].extend(column_value_rules_dict[name].setlocalrules)
	
	validate_rules_file()
	
	error_message = ""
	for name, column_value_rule_list in master_column_value_rules_dict.items():
		column_value_rule_name_list = [type(rule).__name__ for rule in column_value_rule_list]
		column_value_rule_name_counts = Counter(column_value_rule_name_list)
		column_value_rule_duplicates = [name for name, count in column_value_rule_name_counts.items() if count >1]
		for rule_name in column_value_rule_duplicates:
			error_message += (f'Error: Column {name} has multiple {rule_name} rules.\n')

	for name, local_value_rule_list in master_local_value_rules_dict.items():
		local_value_rule_name_list = [type(rule).__name__ for rule in local_value_rule_list]
		local_value_rule_name_counts = Counter(local_value_rule_name_list)
		local_value_rule_duplicates = [name for name, count in local_value_rule_name_counts.items() if count >1]
		for rule_name in local_value_rule_duplicates:
			error_message += (f'Error: Column {name} has multiple {rule_name} rules.\n')

	if error_message:
		LOGFILE.write(error_message)
		LOGFILE.write('Exiting Ruleset Engine.' + '\n')
		LOGFILE.close()
		sys.exit(1)
	return

def validate_data_table_column_names():
	'''
	Check the list of columns in data file against the columns with rules in the rules file.
	Raise Warning if (a) column in data file has no rules or (b) a column with rules is not present in the data file (switched off for now.)
	'''

	global data_columns_with_rules
	data_column_names = data_df.columns.to_list()
	columns_with_rules = list(master_column_value_rules_dict.keys())
	data_columns_with_rules = [item for item in data_column_names if item in columns_with_rules]
	columns_in_data_but_not_in_rules = [item for item in data_column_names if item not in columns_with_rules]
	columns_in_rules_but_not_in_data = [item for item in columns_with_rules if item not in data_column_names]
	
	# for x in columns_in_rules_but_not_in_data:
		# LOGFILE.write(f'Warning: Column {x} in rules file but not in data file.')
	# for x in columns_in_data_but_not_in_rules:
		# LOGFILE.write(f'Warning: Column {x} in data file but not in rules file.')
	return

def validate_column_rules():
	'''
	For each column rule in the rules file, run the corresponding rule checker function.
	'''
	for column_rule in column_rules_dict.keys():
		rule = column_rules_dict[column_rule]
		if c.column_rule_checker_dict[column_rule]:
			ruleset_message = c.column_rule_checker_dict[column_rule](df = data_df, input_rule = rule, input_column_names_list = column_names_list, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict)
		else:
			log_message += (f'Error: {column_rule} does not exist.\n')
		
		for message in ruleset_message:
			LOGFILE.write(message + '\n')
	return

def validate_column_value_rules():
	'''
	For each column value rule in the rules file, that is present in the data file, run the corresponding column value rule checker function.
	Note that column value rules may be specified individually, or in bulk as rule blocks. 
	The gather_column_value_rules functions gathers and stores column value rules, by column, in master_column_value_rules_dict.
	'''
	for column_name in data_columns_with_rules:
		log_message = []
		value_rules_list = master_column_value_rules_dict[column_name]
		set_local_rules_list = master_local_value_rules_dict[column_name]
		local_rules_dict = {type(local_rule).__name__: local_rule for local_rule in set_local_rules_list}

		for value_rule in value_rules_list:
			value_rule_name = type(value_rule).__name__
			if i.in_column_value_rule_checker_dict[value_rule_name]:
				ruleset_message = i.in_column_value_rule_checker_dict[value_rule_name](df = data_df, input_rule = value_rule, input_column_name = column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = master_column_value_rules_dict, local_rules = local_rules_dict)
				log_message += ruleset_message[1]
			else:
				log_message += (f'Error: {value_rule_name} does not exist.\n')
		
		if not log_message:
			LOGFILE.write(f'Info: Column: {column_name} all OK.\n')
		else:
			log_message_string = "\n".join(log_message)
			LOGFILE.write(log_message_string + "\n")
	return

def validate_rule(df, input_column_name, input_rule, input_set_value_rules, input_column_rules, input_column_value_rules):
	'''
	Helper fuction used by validate_conditional_rules function to run the correct value rule checker function.
	See below for conditional_value_rule. 
	'''
	ruleset_message = ""
	valuerules_list = input_rule.valuerules
	set_local_rules_list = input_rule.setlocalrules
	local_rules_dict = {type(local_rule).__name__: local_rule for local_rule in set_local_rules_list}
	
	if len(valuerules_list) > 1:
		ruleset_message = f'Conditional rule is invalid. Only one atomic rule per column is allowed.'
		return ruleset_message
	else:
		value_rule = valuerules_list[0]
		value_rule_name = type(value_rule).__name__
		if i.in_column_value_rule_checker_dict[value_rule_name]:
			[ruleset_message_booleans, ruleset_message_errors] = i.in_column_value_rule_checker_dict[value_rule_name](df = data_df, input_rule = value_rule, input_column_name = input_column_name, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict, local_rules = local_rules_dict)
			ruleset_boolean_dict = {index + 1: value for index, value in enumerate(ruleset_message_booleans)}
		return ruleset_boolean_dict

def validate_conditional_rules():
	"""
	Validates conditional rules in RuleSet where the antecedent is a single atomic rule
	and the consequent is a list of atomic rules.
	
	This function iterates over a dictionary of conditional rules, where each rule maps an
	"if" condition (a single atomic rule) to one or more "then" conditions (a list of atomic rules).
	For each rule:
	- It first checks which rows in the DataFrame satisfy the "if" condition.
	- If no rows match the "if" condition, it logs an informational message and skips the rule.
	- Otherwise, it validates the "then" conditions for the same rows and ensures the
	 condition holds: *if condition is True, then all "then" conditions must also be True
	 for the same rows.
	- Errors are logged if any rows satisfy the "if" condition but fail any of the "then" conditions.

	Returns:
		None. 
		The function prints validation information and errors to the logfile.
	"""

	for conditional_rule in conditional_rules_list:
		if_rule = conditional_rule.column_value_rule_input_1
		then_rule_list = conditional_rule.column_value_rule_input_2
		rule_tag = conditional_rule.rule_tag.name

		if_column_name = if_rule.column_name.name
		if_ruleset_message = validate_rule(df = data_df, input_column_name = if_column_name, input_rule = if_rule, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict) 
		
		#if there is more than one antecedent atomic rule, validate_rule sends an error message. 
		#ruleset-engine logs this error message and moves to the next conditional rule.
		if(type(if_ruleset_message) == str):
			LOGFILE.write(if_ruleset_message)
			continue
		if_is_true = {k:v for k,v in if_ruleset_message.items() if v is True}
		if not if_is_true:
			LOGFILE.write(f"Info: For conditional rule {rule_tag} there are no value pairs to validate.\n")
			continue

		for then_rule in then_rule_list:
			then_column_name = then_rule.column_name.name
			then_ruleset_message = validate_rule(df = data_df, input_column_name = then_column_name , input_rule = then_rule, input_set_value_rules = set_value_rules_dict, input_column_rules = column_rules_dict, input_column_value_rules = column_value_rules_dict) 
			then_is_true = {k:v for k,v in then_ruleset_message.items() if v is True}
			if_then_match = set(if_is_true.keys()).issubset(then_is_true.keys())
			if if_then_match:
				LOGFILE.write(f"Info: For conditional rule {rule_tag}: {if_column_name}, {then_column_name} is OK.\n")
				continue
			else:
				missing_keys = [key for key in if_is_true.keys() if key not in then_is_true.keys()]
				for key in missing_keys:
					LOGFILE.write(f"Error: Conditional rule {rule_tag} fails for columns: {if_column_name}, {then_column_name}, row {key}.\n")
				continue
	return

'''
1. Parse file paths for reference file, rules file and data file
2. Create log file
3. Read rules file. Log any errors. Create parsed rule dictionaries
4. Validate rules files. Log errors and warnings.
5. Set nullvalues.
6. Read data file. 
7. Gather all column value rules expressed as rule blocks or as individual rules.
8. Validate data file column names against column names specified in rules file. 
9. Validate column rules
10. Validate all column value rules.
11. Validate conditional rules.
12. Validate crosscolumn value rules.
'''

def main():
	'''
	Initialize CLI parser.
	Read paths to rules and data files.
	'''
	global RULES_FILE
	global DATA_FILE
	global REFERENCE_FILE
	global LOGFILEPATH

	parser = argparse.ArgumentParser(description = "Ruleset-engine validates a data table according to a rules file written in the RuleSet language.")
	parser.add_argument("--rules-file", type = str, required = True, help = "Rules file stores data rules.")
	parser.add_argument("--data-file", type = str, required = True, help = "Data file stores data to be validated.")
	parser.add_argument("--logfile-path", type = str, help = "Storage folder for log file.")
	args = parser.parse_args()
	RULES_FILE = args.rules_file
	DATA_FILE = args.data_file
	REFERENCE_FILE = get_grammar_path()
	LOGFILEPATH = args.logfile_path if args.logfile_path else "./"

	create_logfile()
	read_rules_file()
	# validate_rules_file()
	set_na_values()
	try:
		read_data_file()
	except Exception as e:
		LOGFILE.write(f"Error: could not read data file. {e}\n")
		sys.exit()
	
	gather_column_value_rules()
	validate_data_table_column_names()
	validate_column_rules()
	validate_column_value_rules()
	validate_conditional_rules()
	LOGFILE.close()

if __name__ == "__main__":
	main()