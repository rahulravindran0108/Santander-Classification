import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def filter(data, condition):
    """
    Remove elements that do not match the condition provided.
    Takes a data list as input and returns a filtered list.
    Conditions should be a list of strings of the following format:
      '<field> <op> <value>'
    where the following operations are valid: >, <, >=, <=, ==, !=
    """

    field, op, value = condition.split(" ")
    
    try:
        value = float(value)
    except:
        value = value.strip("\'\"")
    
    if op == ">":
        matches = data[field] > value
    elif op == "<":
        matches = data[field] < value
    elif op == ">=":
        matches = data[field] >= value
    elif op == "<=":
        matches = data[field] <= value
    elif op == "==":
        matches = data[field] == value
    elif op == "!=":
        matches = data[field] != value
    else:
        raise Exception("Invalid comparison operator. Only >, <, >=, <=, ==, != allowed.")
    
    # filter data and outcomes
    data = data[matches].reset_index(drop = True)
    return data

def satisfaction_stats(data, outcomes, key, filters = []):
    """
    Prints out the Satisfaction stats
    """
    
    # Check that the key exists
    if key not in data.columns.values :
        print "'{}' is not a feature of the Santander data. Did you spell something wrong?".format(key)
        return False

    # Merge data and outcomes into single dataframe
    all_data = pd.concat([data, outcomes], axis = 1)
    
    # Apply filters to data
    for condition in filters:
        all_data = filter_data(all_data, condition)
    all_data = all_data[[key, 'TARGET']]
    
    # Create plotting figure
    plt.figure(figsize=(8,6))

    
    min_value = all_data[key].min()
    max_value = all_data[key].max()
    value_range = max_value - min_value
        
    # Overlay each bin's survival rates
    nonsurv_vals = all_data[all_data['TARGET'] == 0][key].reset_index(drop = True)
    surv_vals = all_data[all_data['TARGET'] == 1][key].reset_index(drop = True)


    plt.hist(nonsurv_vals, alpha = 0.6,
                 color = 'red', label = 'Satisfied')
    plt.hist(surv_vals, alpha = 0.6,
                 color = 'green', label = 'Not Satisfied')
    
    plt.legend(framealpha = 0.8)
    

    # Common attributes for plot formatting
    plt.xlabel(key)
    plt.ylabel('Input')
    plt.title('Customer Satisfaction Statistics With \'%s\' Feature'%(key))
    plt.show()

