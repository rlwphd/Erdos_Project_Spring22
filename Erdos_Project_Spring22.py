# -*- coding: utf-8 -*-
import re
import pandas as pd
#import numpy as np
#from joblib import load

from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource, Div, HoverTool,
                          Label, Paragraph, SingleIntervalTicker, Slider, Select)
#from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show

#from load import load_data

# The following is all of the text that will be displayed on the web page
top_para = """<style>
.content {
    width: 70%;
    margin: auto;
}
h1 {
    margin: 2em 0 0 0;
    color: #2e484c;
    font-family: 'Julius Sans One', sans-serif;
    font-size: 2em;
    text-align: center;
    text-transform: uppercase;
}
h4 {
	color: #2e484c;
	font-family: 'Julius Sans One', sans-serif;
    font-size: 1.6em;
    text-indent: 100px
}
a:link {
    font-weight: bold;
    text-decoration: none;
    color: #0d8ba1;
}
a:visited {
    font-weight: bold;
    text-decoration: none;
    color: #1a5952;
}
a:hover, a:focus, a:active {
    text-decoration: underline;
    color: #9685BA;
}
p {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 1.2em;
    text-align: justify;
    text-justify: inter-word;
}

</style>

<div class="content">
    <h1>Welcome To The Frugal Project</h1>

    <p>On the market for a new loan or account or credit card? Can you recall the last time that you had to
    open an account with a bank? You know for that new house or maybe it was for that new hot rod sitting in 
    your driveway or maybe it was for that fancy new card in your wallet with your name on it. Well, was it an
    enjoyable process or did it cause you to lose a few hairs and maybe age a few years in the process? If your
    experience was anything like ours, then <b>this project</b> is	for you! No, we can't make the bank just give you some
    money but what we did do was summarize all of the <i>complaints</i> from the last several years for all of the major
    banks in the US, so that you can know which	banks to <b>avoid</b> in the future due to their lack of concern for their
    customers. Below is an <i>interactive</i> display to help you see who the major offenders are and in what areas they
    are lacking.</p>
    
    <p>Maybe you aren't on the market for a new loan. Maybe, (<i>*hopefully*</i>) you are the <b>VP</b> from one of these banks
    over Customer Relations or Consumer Lending and you want to <b>improve</b> your business. Well, not only will our
    interactive display help you understand and be able to categorize the complaints that you are recieving, but it
    will also help you see how your bank <b>stacks up</b> compared to your <i>biggest competitors</i>. In fact we not only
    provide you with the visualizations to help you understand but we took it a step further and created an
    <u>AI model</u> that will help you <i>classify</i> all of those communications from your disgruntled customers to help
    you be able to keep track of whether or not your <b>improvements</b> are making a difference. </p>
    
    <p>All of the <a href="https://files.consumerfinance.gov/ccdb/complaints.csv.zip">data</a> comes from
    Consumer Financial Protection Bureau. One of the key roles of the CFPB is to collect and track consumer
    complaints about various companies and their loan processes.</p>
    
    <h4>Visualization of Complaints</h4>
    
    <p>In order to make this interactive display functional, it is limited to 30 Companies which had the highest number of complaints.<br><br></p>
</div>"""

mid_para = """<style>
.midcontent {
     width: 70%;
     margin: auto;
}
h4 {
	color: #2e484c;
	font-family: 'Julius Sans One', sans-serif;
    font-size: 1.6em;
    text-indent: 100px
    }
p {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 1.2em;
    text-align: justify;
    text-justify: inter-word;
}

</style>

<div class="midcontent">

    <h4>Predicting Complaints</h4>
    
    <p>While creating the visualizations, we noticed that over half of the compalints in the raw data do not
    contain the detailed customer complaint. Meaning that some data cleaning needed to happen before we could
    train our AI model to predict our complaints. We also wanted our model to be able to predict the issue of
    the complaint and not just the category of the complaint, so our model was trained only on the mortgage
    loan data. Further improvements will be to include all issues from all product categories. Below details
    out how well the models were able to learn the necessary features in order to determine the issue of the
    complaint.<br><br></p>
    
</div>"""

heading = Div(text=top_para, sizing_mode='stretch_width')

mid_text = Div(text=mid_para, sizing_mode='stretch_width')


# Loading in the necessary data for displaying
def load_data(type='raw'):
    # Defining the categories for plotting purposes
    titles = ['Product Category', 'Issue Category', 'Sub-product Category', 'State', 'Consumer Respone', 'Timely Response', 'Tags Category', 'Company Response']
    category = ['Product', 'Issue', 'Sub-product', 'State', 'Consumer', 'Timely', 'Tags', 'Response']

    # Path to github for files
    git_path = 'https://raw.githubusercontent.com/rlwphd/Erdos_Project_Spring22/main/data/'
    #git_path = './data/'

    # Grabbing all of the csv files in the data folder from github that are needed
    # and storing them in a dictionary so that they can be called by their file name
    raw_files = ['Top30Companies_TotalComplaints', 'Consumer_complaints_TopCompanies', 'Issue_complaints_TopCompanies', 'Product_complaints_TopCompanies', 'Response_complaints_TopCompanies', 'State_complaints_TopCompanies', 'Sub-product_complaints_TopCompanies', 'Tags_complaints_TopCompanies', 'Timely_complaints_TopCompanies']
    dfs = {}
    if type == 'raw':
        for name in raw_files:
            dfs[name] = pd.read_csv(git_path+name+".csv")
        
        # Loading the possible values for each category
        cat_list = pd.read_csv(git_path+"Category_names.csv")
        cat_list = [re.split(r"', '|, '|', ", val.replace("['","").replace("']","").replace("[","").replace("]","")) for val in cat_list.iloc[:,0].to_list()]
        cat_list = [list(map(lambda x: x if x != 'nan' else 'Not Given', line)) for line in cat_list]

    mort_files = ['MortgageTop30Companies_TotalComplaints', 'Mortgage_Consumer_complaints_TopCompanies', 'Mortgage_Issue_complaints_TopCompanies', 'Mortgage_Response_complaints_TopCompanies', 'Mortgage_State_complaints_TopCompanies', 'Mortgage_Sub-product_complaints_TopCompanies', 'Mortgage_Tags_complaints_TopCompanies', 'Mortgage_Timely_complaints_TopCompanies']
    if type == 'mort':
        for name in mort_files:
            dfs[name] = pd.read_csv(git_path+name+".csv")
        
        # Loading the possible values for each category
        cat_list = pd.read_csv(git_path+"Mortgage_Category_names.csv")
        cat_list = [re.split(r"', '|, '|', ", val.replace("['","").replace("']","").replace("[","").replace("]","")) for val in cat_list.iloc[:,0].to_list()]
        cat_list = [list(map(lambda x: x if x != 'nan' else 'Not Given', line)) for line in cat_list]
        
        titles = titles[1:]
        category = category[1:]


    return dfs, category, titles, cat_list

# Need to give the function either 'raw' or 'mort'
raw_dfs, raw_category, raw_titles, raw_list = load_data('raw')

# Creating the list of company names and setting up the total number of complaints text
company_list = raw_dfs['Top30Companies_TotalComplaints'].iloc[:,0].to_list()
tot_complaints = Paragraph(text="Total Number of Complaints for {}:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]), align='center')
tot_comp_val = Paragraph(text=str(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,1]), align='center')

# Defining which category I'm after and setting up the total number of categorical complaints text
cat_df = '{}_complaints_TopCompanies'.format(raw_category[0])
cat_complaints = Paragraph(text="Total Number of Complaints in the {} Category:".format(raw_category[0]), align='center')
cat_comp_val = Paragraph(text=str(raw_dfs[cat_df].iloc[0,2]), align='center')

# Initializing the Data and the Graph
#source = ColumnDataSource(data=raw_dfs[cat_df].loc[raw_dfs[cat_df].iloc[0,:]==raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]])
rlabels = raw_list[0]
rvalues = raw_dfs[cat_df][raw_dfs[cat_df].isin([raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]]).any(1)]

rplot = figure(y_range=rlabels, title=raw_titles[0], width=800, height=500)
rplot.xaxis.axis_label = "Options in Category"
rplot.yaxis.axis_label = "Percentage of Complaints"

#color_mapper = CategoricalColorMapper(palette=Spectral6, factors=labels)
# plot.hbar(
#     y=labels,
#     right=values,
#     #source=source,
#     #fill_color=color_mapper,
#     fill_color='blue',
#     fill_alpha=0.8,
#     line_color='#7c7e71',
#     line_width=0.5,
#     line_alpha=0.5,
# )
#plot.add_tools(HoverTool(tooltips="@values", show_arrow=False, point_policy='follow_mouse'))


# Creating the selector for the company
# def company_update(attr, old, new):
#     tot_complaints.text = "Total Number of Complaints for {}:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0])
#     tot_comp_val.text = str(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,1])
#     values = raw_dfs[cat_df][ raw_dfs[cat_df].isin([raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0]]).any(1)]
#     plot.right = values
    
com_sel = Select(title="Choose Company to view:", value=company_list[0], options=company_list)
# com_sel.on_change('value', company_update)

# Creating the selector for the category
# def category_update(attr, old, new):
#     cat_complaints.text = "Total Number of Complaints in the {} Category:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[com_sel.value,0])
#     cat_comp_val.text = str(raw_dfs['Top30Companies_TotalComplaints'].iloc[cat_sel.value,1])

cat_sel = Select(title="Choose Category to view:", value=raw_category[0], options=raw_category)
# cat_sel.on_change('value', category_update)

selector = column(com_sel, tot_complaints, tot_comp_val, cat_sel, cat_complaints, cat_comp_val, width=500, margin=(0,50,0,50))
raw_layout = row(selector, rplot, align='center')



mort_dfs, mort_category, mort_titles, mort_list = load_data('mort')

# Creating the list of company names and setting up the total number of complaints text
mcompany_list = mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[:,0].to_list()
tot_mort_complaints = Paragraph(text="Total Number of Complaints for {}:".format(mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,0]), align='center')
tot_mort_comp_val = Paragraph(text=str(mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,1]), align='center')

# Defining which category I'm after and setting up the total number of categorical complaints text
mort_df = 'Mortgage_{}_complaints_TopCompanies'.format(mort_category[0])
mort_complaints = Paragraph(text="Total Number of Complaints in the {} Category:".format(mort_category[0]), align='center')
mort_comp_val = Paragraph(text=str(mort_dfs[mort_df].iloc[0,1]), align='center')

# Initializing the Data and the Graph
#source = ColumnDataSource(data=raw_dfs[cat_df].loc[raw_dfs[cat_df].iloc[0,:]==raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]])
mlabels = mort_list[0]
mvalues = mort_dfs[mort_df][mort_dfs[mort_df].isin([mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,0]]).any(1)]

mplot = figure(y_range=mlabels, title=mort_titles[0], width=800, height=500)
mplot.xaxis.axis_label = "Options in Category"
mplot.yaxis.axis_label = "Percentage of Complaints"

mortcom_sel = Select(title="Choose Company to view:", value=mcompany_list[0], options=mcompany_list)

mortcat_sel = Select(title="Choose Category to view:", value=mort_category[0], options=mort_category)

mselector = column(mortcom_sel, tot_mort_complaints, tot_mort_comp_val, mortcat_sel, mort_complaints, mort_comp_val, width=500, margin=(0,50,0,50))
mort_layout = row(mselector, mplot, align='center')

final_layout = column(heading, raw_layout, mid_text, mort_layout, sizing_mode='stretch_both')

#curdoc().add_root(final_layout)
#curdoc().title = "Complaints Classifier"
show(final_layout)