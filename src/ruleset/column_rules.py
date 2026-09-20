import pandas as pd
from ruleset import helper as h
from collections import defaultdict

def check_column_list_rule(df, input_rule, **kwargs):
    '''
    Matches the list of columns names in the input file against the list provided to
    the ColumnListRule. ColumnListRule is the only required rule in RuleSet; it specifies a list of column names.
    A warning is generated if:
    (a) If columns specified in the rules file are missing in data file.
    (b) If columns are found in the data file that are not present in the rules file.
    (Switched off for now.)

    Args:
        df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
        input_rule (ColumnListRule) : the ColumnListRule object.
        
    Returns:
        list: a list of generated messages.
    '''
    df_column_names_list = list(df)
    df_column_names_set = set(df_column_names_list)
    message_list = []
    
    input_rule_column_names_set = set([column.name for column in input_rule.column_names_list])
    
    in_input_rule_not_in_df = input_rule_column_names_set - df_column_names_set
    
    in_df_not_in_input_rule = df_column_names_set - input_rule_column_names_set
    
    if input_rule_column_names_set == df_column_names_set:
        message_list.append(f'Info: All columns present in data file.')
    
    if in_input_rule_not_in_df:
        in_input_rule_not_in_df_string = ",".join(in_input_rule_not_in_df)
        # message_list.append(f'Warning: Column(s) {in_input_rule_not_in_df_string} listed in rules file, but missing in data file.')
    
    if in_df_not_in_input_rule:
        in_df_not_in_input_rule_string = ",".join(in_df_not_in_input_rule)
        # message_list.append(f'Warning: Column(s) {in_df_not_in_input_rule_string} found in data file, but not listed in rules file.')
    
    return message_list

def check_required_columns_rule(df, input_rule, input_column_names_list, **kwargs):
    '''
    If the 'all columns required' flag is set then it checks if all columns listed in column names list are present in the data file.
    Generates an error message with name of missing column(s).
    
    Args:
        df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
        input_rule (RequiredColumnsRule) : the RequiredColumnsRule object.
        input_column_names_list (list) : the list of column names specified in the rules file.
        
    Returns:
        list: a list of generated messages.
    '''
    df_column_names_list = list(df)
    df_column_names_set = set(df_column_names_list)
    input_rule_column_names_set = set(input_column_names_list)
    message_list = []

    in_input_rule_not_in_df = input_rule_column_names_set - df_column_names_set
    if in_input_rule_not_in_df:
        for column_name in in_input_rule_not_in_df:
            message_list.append(f'Error: Column {column_name} is missing in data file, but listed in rules file. All columns listed in rules file are required.')
    else:
        message_list.append(f"Info: All required columns found in data file.")
    
    return message_list

def check_extra_columns_rule(df, input_rule, input_column_names_list, **kwargs):
    '''
    If the 'extra columns allowed' flag is set then it checks if any columns not listed in the column names list are present in the data file.
    Generates an error message with name of extra column(s).
    
    Args:
        df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
        input_rule (ExtraColumnsRule) : the ExtraColumnsRule object.
        input_column_names_list (list) : the list of column names specified in the rules file.
        
    Returns:
        list: a list of generated messages.
    '''
    df_column_names_list = list(df)
    df_column_names_set = set(df_column_names_list)
    input_rule_column_names_set = set(input_column_names_list)
    in_df_not_in_input_rule = df_column_names_set - input_rule_column_names_set
    message_list = []
    
    if in_df_not_in_input_rule:
        for column_name in in_df_not_in_input_rule:
            message_list.append(f'Error: Column {column_name} found in data file is not listed in rules file. No extra columns are allowed.')
    else:
        message_list.append(f'Info: No extra columns included in data file.')
    
    return message_list

def check_column_order_rule(df, input_rule, input_column_names_list, **kwargs):
    '''
    If the 'keep column order' flag is set then it checks if columns in data file are in the same order as specified in the rules file.
    If column names are different between these two files then a column order is not evaluated, a warning message is generated instead.
    
    Args:
        df (pandas.core.frame.DataFrame): the Pandas dataframe that stores the parsed data.
        input_rule (ColumnOrderRule) : the ColumnOrderRule object.
        input_column_names_list (list) : the list of column names specified in the rules file.
        
    Returns:
        list: a list of generated messages.
    '''
    num_of_out_of_order_columns = 0
    df_column_names_list = list(df)
    df_column_names_set = set(df_column_names_list)
    input_rule_column_names_set = set(input_column_names_list)
    message_list = []
    
    if (df_column_names_set == input_rule_column_names_set):
        for column_name in input_column_names_list:
            if df_column_names_list.index(column_name) != input_column_names_list.index(column_name):
                message_list.append(f'Error: {column_name} is out of order in data file. ')
                num_of_out_of_order_columns +=1
        if num_of_out_of_order_columns == 0:
            message_list.append('Info: Column order is OK.')
    else:
        message_list.append(f"Warning: Column names in rules file and data file do not match. Cannot evaluate column order.")
    
    return message_list

'''
Initialize function dictionary for checking each type of ColumnRule.
There is a checker function for each rule in RuleSet. 
If a new column checking rule is added to RuleSet, a new checking function should be written. The new function should be added to column_rule_checker_dict.
'''

column_rule_checker_dict = {}

column_rule_checker_dict["ColumnListRule"] = check_column_list_rule

column_rule_checker_dict["RequiredColumnsRule"] = check_required_columns_rule

column_rule_checker_dict["ExtraColumnsRule"] = check_extra_columns_rule

column_rule_checker_dict["ColumnOrderRule"] = check_column_order_rule