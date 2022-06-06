# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import numpy as np
#from joblib import load

from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource, Div, HoverTool,
                          Label, Paragraph, SingleIntervalTicker, Slider, Select)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show

#from load import load_data

# The following is all of the text that will be displayed on the web page
h1 = Div(text="Welcome To The Frugal Project",
              style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'margin': '2em 0 0 0', 'color': '#2e484c', 'font-family': "'Julius Sans One', sans-serif", 'font-size': '1.8em', 'text-align': 'center', 'text-transform': 'uppercase'})

top_para1 = Div(text="On the market for a new loan or account or credit card? Can you recall the last time that you had to open an account with a bank? You know for that new house or maybe it was for that new hot rod sitting in your driveway or maybe it was for that fancy new card in your wallet with your name on it. Well, was it an enjoyable process or did it cause you to lose a few hairs and maybe age a few years in the process? If your experience was anything like ours, then <b>this project</b> is	for you! No, we can't make the bank just give you some money but what we did do was summarize all of the <i>complaints</i> from the last several years for all of the major banks in the US, so that you can know which	banks to <b>avoid</b> in the future due to their lack of concern for their customers. Below is an <i>interactive</i> display to help you see who the major offenders are and in what areas they are lacking.",
                style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'font-family': "'Helvetica Neue', Helvetica, Arial, sans-serif", 'font-size': '1.2em', 'text-align': 'justify', 'text-justify': 'inter-word'})

top_para2 = Div(text="Maybe you aren't on the market for a new loan. Maybe, (<i>*hopefully*</i>) you are the <b>VP</b> from one of these banks over Customer Relations or Consumer Lending and you want to <b>improve</b> your business. Well, not only will our interactive display help you understand and be able to categorize the complaints that you are recieving, but it will also help you see how your bank <b>stacks up</b> compared to your <i>biggest competitors</i>. In fact we not only provide you with the visualizations to help you understand but we took it a step further and created an <u>AI model</u> that will help you <i>classify</i> all of those communications from your disgruntled customers to help you be able to keep track of whether or not your <b>improvements</b> are making a difference.",
                style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'font-family': "'Helvetica Neue', Helvetica, Arial, sans-serif", 'font-size': '1.2em', 'text-align': 'justify', 'text-justify': 'inter-word'})

top_para3 = Div(text='All of the <a href="https://files.consumerfinance.gov/ccdb/complaints.csv.zip">data</a> comes from Consumer Financial Protection Bureau. One of the key roles of the CFPB is to collect and track consumer complaints about various companies and their loan processes.',
                style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'font-family': "'Helvetica Neue', Helvetica, Arial, sans-serif", 'font-size': '1.2em', 'text-align': 'justify', 'text-justify': 'inter-word'})

h4_1 = Div(text="Visualization of Complaints",
           style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'margin': '2em 0 0 0', 'color': '#2e484c', 'font-family': "'Julius Sans One', sans-serif", 'font-size': '1.4em'})
	
top_para4 = Div(text="Inorder to make this interactive display functional, it is limited to 30 Companies which had the highest number of complaints. </p>",
                style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'font-family': "'Helvetica Neue', Helvetica, Arial, sans-serif", 'font-size': '1.2em', 'text-align': 'justify', 'text-justify': 'inter-word'})

h4_2 = Div(text="Predicting Complaints",
           style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'margin': '2em 0 0 0', 'color': '#2e484c', 'font-family': "'Julius Sans One', sans-serif", 'font-size': '1.4em'})

mid_para1 = Div(text="While creating the visualizations, we noticed that over half of the compalints in the raw data do not contain the detailed customer complaint. Meaning that some data cleaning needed to happen before we could train our AI model to predict our complaints. We also wanted our model to be able to predict the issue of the complaint and not just the category of the complaint, so our model was trained only on the mortgage loan data. Further improvements will be to include all issues from all product categories. Below details out how well the models were able to learn the necessary features in order to determine the issue of the complaint.",
                style={'min-width': '600px', 'max-width': '900px', 'width': '80%', 'font-family': "'Helvetica Neue', Helvetica, Arial, sans-serif", 'font-size': '1.2em', 'text-align': 'justify', 'text-justify': 'inter-word'})

begin_text = column(h1, top_para1, top_para2, top_para3, h4_1, top_para4, sizing_mode="stretch_both")
mid_text = column(h4_2, mid_para1, sizing_mode="stretch_both")


# Loading in the necessary data for displaying
def load_data(type='raw'):
    # Defining the categories for plotting purposes
    titles = ['Product Category', 'Issue Category', 'Sub-product Category', 'State', 'Consumer Respone', 'Timely Response', 'Tags Category', 'Company Response']
    category = ['Product', 'Issue', 'Sub-product', 'State', 'Consumer', 'Timely', 'Tags', 'Response']

    # Path to github for files
    git_path = 'https://raw.githubusercontent.com/rlwphd/Erdos_Project_Spring22/main/data/'

    # Grabbing all of the csv files in the data folder from github that are needed
    # and storing them in a dictionary so that they can be called by their file name
    raw_files = ['Top30Companies_TotalComplaints', 'Consumer_complaints_TopCompanies', 'Issue_complaints_TopCompanies', 'Product_complaints_TopCompanies', 'Response_complaints_TopCompanies', 'State_complaints_TopCompanies', 'Sub-product_complaints_TopCompanies', 'Tags_complaints_TopCompanies', 'Timely response_complaints_TopCompanies']
    dfs = {}
    if type == 'raw':
        for name in raw_files:
            dfs[name] = pd.read_csv(git_path+name+".csv")
        # Loading the possible values for each category
        with open(git_path+"Category_names.txt", "r") as f:
            cat_list = json.load(f)

    mort_files = ['MortgageTop30Companies_TotalComplaints', 'Mortgage_Consumer_complaints_TopCompanies', 'Mortgage_Issue_complaints_TopCompanies', 'Mortgage_Response_complaints_TopCompanies', 'Mortgage_State_complaints_TopCompanies', 'Mortgage_Sub-product_complaints_TopCompanies', 'Mortgage_Tags_complaints_TopCompanies', 'Mortgage_Timely_complaints_TopCompanies']
    if type == 'mort':
        for name in mort_files:
            dfs[name] = pd.read_csv(git_path+name+".csv")
        with open(git_path+"Mortgage_category_names.txt", "r") as f:
            cat_list = json.load(f)
        
        titles = titles[1:]
        category = category[1:]


    return dfs, category, titles, cat_list

# Need to give the function either 'raw' or 'mort'
raw_dfs, raw_category, raw_titles, raw_list = load_data('raw')

# Creating the list of company names and setting up the total number of complaints text
company_list = raw_dfs['Top30Companies_TotalComplaints'].iloc[:,0].to_list()
tot_complaints = Paragraph(text="Total Number of Complaints for {}:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]))
tot_comp_val = Paragraph(text=str(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,1]))

# Defining which category I'm after and setting up the total number of categorical complaints text
cat_df = '{}_complaints_TopCompanies'.format(raw_category[0])
cat_complaints = Paragraph(text="Total Number of Complaints in the {} Category:".format(raw_category[0]))
cat_comp_val = Paragraph(text=str(raw_dfs[cat_df].iloc[0,1]))

# Initializing the Data and the Graph
#source = ColumnDataSource(data=raw_dfs[cat_df].loc[raw_dfs[cat_df].iloc[0,:]==raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]])
labels = raw_list[0]
values = raw_dfs[cat_df][ raw_dfs[cat_df].isin([raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]]).any(1)]

plot = figure(y_range=labels, title=raw_titles[0], height=300)
plot.xaxis.axis_label = "Options in Category"
plot.yaxis.axis_label = "Percentage of Complaints"

#color_mapper = CategoricalColorMapper(palette=Spectral6, factors=labels)
plot.hbar(
    y=labels,
    right=values,
    #source=source,
    #fill_color=color_mapper,
    fill_color='blue',
    fill_alpha=0.8,
    line_color='#7c7e71',
    line_width=0.5,
    line_alpha=0.5,
)
plot.add_tools(HoverTool(tooltips="@values", show_arrow=False, point_policy='follow_mouse'))


# Creating the selector for the company
def company_update(attr, old, new):
    tot_complaints.text = "Total Number of Complaints for {}:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0])
    tot_comp_val.text = str(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,1])
    values = raw_dfs[cat_df][ raw_dfs[cat_df].isin([raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0]]).any(1)]
    plot.right = values
    
com_sel = Select(title="Choose Company to view:", value=company_list[0], options=company_list)
com_sel.on_change('value', company_update)

# Creating the selector for the category
def category_update(attr, old, new):
    cat_complaints.text = "Total Number of Complaints in the {} Category:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0])
    cat_comp_val.text = str(raw_dfs['Top30Companies_TotalComplaints'].iloc[cat_sel.value,1])

cat_sel = Select(title="Choose Category to view:", value=raw_category[0], options=raw_category)
cat_sel.on_change('value', category_update)

selector = column(com_sel, tot_complaints, tot_comp_val, cat_sel, cat_complaints, cat_comp_val)
raw_layout = row(selector, plot, sizing_mode='scale_width')



#mort_dfs, mort_category, mort_titles, mort_list = load_data('mort')


final_layout = column(begin_text, raw_layout, mid_text, sizing_mode='stretch_both')

curdoc().add_root(final_layout)
curdoc().title = "Complaints Classifier"
