# -*- coding: utf-8 -*-
"""
This code is to load and prepare all of the mini csv files for interactive displaying.
Below is the list of the files without their extensions.

Consumer_complaints_TopCompanies
Issue_complaints_TopCompanies
Product_complaints_TopCompanies
Response_complaints_TopCompanies
State_complaints_TopCompanies
Sub-product_complaints_TopCompanies
Tags_complaints_TopCompanies
Timely response_complaints_TopCompanies
Top30Companies_TotalComplaints


MortgageTop30Companies_TotalComplaints
Mortgage_Consumer_complaints_TopCompanies
Mortgage_Issue_complaints_TopCompanies
Mortgage_Response_complaints_TopCompanies
Mortgage_State_complaints_TopCompanies
Mortgage_Sub-product_complaints_TopCompanies
Mortgage_Tags_complaints_TopCompanies
Mortgage_Timely_complaints_TopCompanies

"""
import os
import pickle
import pandas as pd


def load_data():
    # Grabbing all of the csv files in the data folder minus the ones I don't want
    # and storing them in a dictionary so that they can be called by their file name
    raw_dfs = {}
    mort_dfs = {}    
    for file in os.listdir(os.path.join(os.path.dirname(__file__), 'data'):
        if file.endswith(".csv") and file != "complaints.csv" and file != "mortgage_complaints.csv" and file != "Raw_Percentage_Missing.csv" and "Mortgage" not in file:
            name = file[:-4]
            raw_dfs[name] = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data',file))
        elif file.endswith(".csv") and "Mortgage" in file:
            name = file[:-4]
            mort_dfs[name] = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data',file))

    # Defining the categories for plotting purposes
    raw_titles = ['Product Category', 'Issue Category', 'Sub-product Category', 'State', 'Consumer Respone', 'Timely Response', 'Tags Category', 'Company Response']
    raw_category = ['Product', 'Issue', 'Sub-product', 'State', 'Consumer', 'Timely', 'Tags', 'Response']
    mort_category = raw_category[1:]
    mort_titles = raw_titles[1:]
    
    # Loading the possible values for each category
    with open(os.path.join(os.path.dirname(__file__), 'data', "Category_names.txt"), "rb") as f:
        raw_list = pickle.load(f)

    with open(os.path.join(os.path.dirname(__file__), 'data', "Mortgage_category_names.txt"), "rb") as f:
        mort_list = pickle.load(f)

    return raw_dfs, mort_dfs, raw_category, mort_category, raw_titles, mort_titles, raw_list, mort_list