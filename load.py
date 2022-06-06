"""
This code is to load and prepare all of the mini csv files for interactive displaying.
Below is the list of the files without their extensions.

For type = 'raw':
Consumer_complaints_TopCompanies
Issue_complaints_TopCompanies
Product_complaints_TopCompanies
Response_complaints_TopCompanies
State_complaints_TopCompanies
Sub-product_complaints_TopCompanies
Tags_complaints_TopCompanies
Timely response_complaints_TopCompanies
Top30Companies_TotalComplaints

For type = 'mort':
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


def load_data(type='raw'):
    # Defining the categories for plotting purposes
    titles = ['Product Category', 'Issue Category', 'Sub-product Category', 'State', 'Consumer Respone', 'Timely Response', 'Tags Category', 'Company Response']
    category = ['Product', 'Issue', 'Sub-product', 'State', 'Consumer', 'Timely', 'Tags', 'Response']

    # Grabbing all of the csv files in the data folder minus the ones I don't want
    # and storing them in a dictionary so that they can be called by their file name
    dfs = {}
    if type == 'raw':
        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'data')):
            if file.endswith(".csv") and file != "complaints.csv" and file != "mortgage_complaints.csv" and file != "Raw_Percentage_Missing.csv" and "Mortgage" not in file:
                name = file[:-4]
                dfs[name] = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data',file))
        # Loading the possible values for each category
        with open(os.path.join(os.path.dirname(__file__), 'data', "Category_names.txt"), "rb") as f:
            cat_list = pickle.load(f)

    if type == 'mort':
        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'data')):
            if file.endswith(".csv") and "Mortgage" in file and file != "mortgage_complaints.csv":
                name = file[:-4]
                dfs[name] = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data',file))
        with open(os.path.join(os.path.dirname(__file__), 'data', "Mortgage_category_names.txt"), "rb") as f:
            cat_list = pickle.load(f)
        
        titles = titles[1:]
        category = category[1:]


    return dfs, category, titles, cat_list