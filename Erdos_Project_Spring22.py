# -*- coding: utf-8 -*-
import re
import pandas as pd
import math
#import numpy as np
#from joblib import load

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, HoverTool, Paragraph, Select
from bokeh.palettes import Turbo256
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
    
    <p>In order to make this interactive display functional, it is limited to 30 Companies which had the highest number
    of complaints. The graph below allows you to explore some of the raw data from the CFPB. <br><br></p>
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
    loan data. Further improvements will be to include all issues from all product categories. Below allows
    one to explore the different aspects of the mortage data.<br><br></p>
    
</div>"""

heading = Div(text=top_para, sizing_mode='stretch_width')

mid_text = Div(text=mid_para, sizing_mode='stretch_width')

# Loading in the necessary data for displaying
def load_data(type='raw'):
    # Defining the categories for plotting purposes
    titles = ['Product Category', 'Issue Category', 'Sub-product Category', 'Complaints by State', 'Consumer Response', 'Timely Response', 'Tags Category', 'Company Response']
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
        cat_dict = {}
        for i,cat in enumerate(category):
            cat_dict[cat] = cat_list[i]

    mort_files = ['MortgageTop30Companies_TotalComplaints', 'Mortgage_Consumer_complaints_TopCompanies', 'Mortgage_Issue_complaints_TopCompanies', 'Mortgage_Response_complaints_TopCompanies', 'Mortgage_State_complaints_TopCompanies', 'Mortgage_Sub-product_complaints_TopCompanies', 'Mortgage_Tags_complaints_TopCompanies', 'Mortgage_Timely_complaints_TopCompanies']
    if type == 'mort':
        for name in mort_files:
            dfs[name] = pd.read_csv(git_path+name+".csv")
        
        titles = titles[1:]
        category = category[1:]

        # Loading the possible values for each category
        cat_list = pd.read_csv(git_path+"Mortgage_Category_names.csv")
        cat_list = [re.split(r"', '|, '|', ", val.replace("['","").replace("']","").replace("[","").replace("]","")) for val in cat_list.iloc[:,0].to_list()]
        cat_list = [list(map(lambda x: x if x != 'nan' else 'Not Given', line)) for line in cat_list]
        cat_dict = {}
        for i,cat in enumerate(category):
            cat_dict[cat] = cat_list[i]
        


    return dfs, category, titles, cat_dict

# Need to give the function either 'raw' or 'mort'
raw_dfs, raw_category, raw_titles, raw_list = load_data('raw')

# Creating the list of company names and setting up the total number of complaints text
company_list = raw_dfs['Top30Companies_TotalComplaints'].iloc[:,0].to_list()
tot_complaints = Paragraph(text="Total Number of Complaints for {}:".format(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0]), align='center')
tot_comp_val = Paragraph(text=str(raw_dfs['Top30Companies_TotalComplaints'].iloc[0,1]), align='center')

# Defining which category I'm after and setting up the total number of categorical complaints text
cat_df = '{}_complaints_TopCompanies'.format(raw_category[0])
cat_complaints = Paragraph(text=" ", align='center', visible=False)
cat_comp_val = Paragraph(text=" ", align='center', visible=False)

# Mouse hover display on graphs
TOOLTIPS=[
    ("Category:",'@labels'),
    ("# of Compliants:", "@values")
]

# Initializing the Data and the Graph
rlabels = raw_list['Product']
rvalues = raw_dfs[cat_df].groupby(['Company']).get_group((raw_dfs['Top30Companies_TotalComplaints'].iloc[0,0])).iloc[:,2].to_list()
rcolor = Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
rsource = ColumnDataSource(data={'labels': rlabels, 'values':rvalues, 'color':rcolor})

rplot = figure(y_range=rlabels, title=raw_titles[0], width=800, height_policy='fit', min_height=500)
rplot.yaxis.axis_label = "Options in Category"
rplot.xaxis.axis_label = "Number of Complaints"

#color_mapper = CategoricalColorMapper(palette=Spectral6, factors=labels)
rplot.hbar(
    y='labels',
    right='values',
    source=rsource,
    height=0.8,
    color='color'
)
rplot.add_tools(HoverTool(tooltips=TOOLTIPS, show_arrow=False, point_policy='follow_mouse'))


# Creating the selector for the company
def company_update(attrname, old, new):
    # Update which company is displayed
    tot_complaints.text = "Total Number of Complaints for {}:".format(com_sel.value)
    tot_comp_val.text = str(raw_dfs['Top30Companies_TotalComplaints'][raw_dfs['Top30Companies_TotalComplaints'].isin([com_sel.value]).any(1)].iloc[:,1].sum())
    cat_df = '{}_complaints_TopCompanies'.format(cat_sel.value)
    if cat_sel.value != 'Product':
        # Update the category
        cat_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(cat_sel.value, prod_sel.value)
        cat_comp_val.text = str(raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].sum())
        # Update the graph with the new values
        rlabels = raw_list[cat_sel.value]
        rvalues = raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].to_list()
        rsource.data = dict(
            labels=rlabels,
            values=rvalues,
            color=Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
        )
        rtitle = [val for val in raw_titles if cat_sel.value in val]
        rplot.title.text = rtitle[0]
        rplot.y_range.factors=rlabels
        
    else:
        # Update the graph with the new values
        rlabels = raw_list[cat_sel.value]
        rvalues = raw_dfs[cat_df].groupby(['Company']).get_group((com_sel.value)).iloc[:,2].to_list()
        rsource.data = dict(
            labels=rlabels,
            values=rvalues,
            color=Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
        )
        rtitle = [val for val in raw_titles if cat_sel.value in val]
        rplot.title.text = rtitle[0]
        rplot.y_range.factors=rlabels
    
com_sel = Select(title="Choose Company to view:", value=company_list[0], options=company_list)
com_sel.on_change('value', company_update)

# Creating the selector for the category
def category_update(attrname, old, new):
    cat_df = '{}_complaints_TopCompanies'.format(cat_sel.value)
    if cat_sel.value != 'Product':
        prod_sel.visible = True
        cat_complaints.visible = True
        cat_comp_val.visible = True
        # Update the category
        cat_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(cat_sel.value, prod_sel.value)
        cat_comp_val.text = str(raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].sum())
        # Update the graph with the new values
        rlabels = raw_list[cat_sel.value]
        rvalues = raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].to_list()
        rsource.data = dict(
            labels=rlabels,
            values=rvalues,
            color=Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
        )
        rtitle = [val for val in raw_titles if cat_sel.value in val]
        rplot.title.text = rtitle[0]
        rplot.y_range.factors=rlabels
        
    else:
        prod_sel.visible = False
        cat_complaints.visible = False
        cat_comp_val.visible = False
        # Update the graph with the new values
        rlabels = raw_list[cat_sel.value]
        rvalues = raw_dfs[cat_df].groupby(['Company']).get_group((com_sel.value)).iloc[:,2].to_list()
        rsource.data = dict(
            labels=rlabels,
            values=rvalues,
            color=Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
        )
        rtitle = [val for val in raw_titles if cat_sel.value in val]
        rplot.title.text = rtitle[0]
        rplot.y_range.factors=rlabels

cat_sel = Select(title="Choose Category to view:", value=raw_category[0], options=raw_category)
cat_sel.on_change('value', category_update)

# Creating the selector for the sub-category
def product_update(attrname, old, new):
    # Update the category
    cat_df = '{}_complaints_TopCompanies'.format(cat_sel.value)
    cat_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(cat_sel.value, prod_sel.value)
    cat_comp_val.text = str(raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].sum())
    # Update the graph with the new values
    rlabels = raw_list[cat_sel.value]
    rvalues = raw_dfs[cat_df].groupby(['Company','Product']).get_group((com_sel.value, prod_sel.value)).iloc[:,2].to_list()
    rsource.data = dict(
        labels=rlabels,
        values=rvalues,
        color=Turbo256[::math.floor(256/len(rlabels))][:len(rlabels)]
    )
    rtitle = [val for val in raw_titles if cat_sel.value in val]
    rplot.title.text = rtitle[0]
    rplot.y_range.factors=rlabels

prod_sel = Select(title="Select which Product to view in the chosen Category:", value=raw_list['Product'][-1], options=raw_list['Product'], visible=False)
prod_sel.on_change('value', product_update)

selector = column(com_sel, tot_complaints, tot_comp_val, cat_sel, prod_sel, cat_complaints, cat_comp_val, width=500, margin=(0,50,0,50))
raw_layout = row(selector, rplot, align='center')



mort_dfs, mort_category, mort_titles, mort_list = load_data('mort')

# Creating the list of company names and setting up the total number of complaints text
mcompany_list = mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[:,0].to_list()
tot_mort_complaints = Paragraph(text="Total Number of Complaints for {}:".format(mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,0]), align='center')
tot_mort_comp_val = Paragraph(text=str(mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,1]), align='center')

# Defining which category I'm after and setting up the total number of categorical complaints text
mort_df = 'Mortgage_{}_complaints_TopCompanies'.format(mort_category[0])
#mort_complaints = Paragraph(text="Total Number of Complaints in the {} Category for sub-category {}:".format(mort_category[0], mort_list['Issue'][-1]), align='center')
#mort_comp_val = Paragraph(text=str(mort_dfs[mort_df].groupby(['Company']).get_group((mcompany_list[0])).iloc[-1,1].sum()), align='center')

# Initializing the Data and the Graph
mlabels = mort_list['Issue']
mvalues = mort_dfs[mort_df].groupby(['Company']).get_group((mort_dfs['MortgageTop30Companies_TotalComplaints'].iloc[0,0])).iloc[:,1].tolist()
mcolor = Turbo256[::math.floor(256/len(mlabels))][:len(mlabels)]
msource = ColumnDataSource(data={'labels': mlabels, 'values':mvalues, 'color':mcolor})

mplot = figure(y_range=mlabels, title=mort_titles[0], width=800, height_policy='fit', min_height=500)
mplot.yaxis.axis_label = "Options in Category"
mplot.xaxis.axis_label = "Percentage of Complaints"

mplot.hbar(
    y='labels',
    right='values',
    source=msource,
    height=0.8,
    color='color'
)
mplot.add_tools(HoverTool(tooltips=TOOLTIPS, show_arrow=False, point_policy='follow_mouse'))


# Creating the selector for the company
def mcompany_update(attrname, old, new):
    # Update which company is displayed
    tot_mort_complaints.text = "Total Number of Complaints for {}:".format(mortcom_sel.value)
    tot_mort_comp_val.text = str(mort_dfs['MortgageTop30Companies_TotalComplaints'][mort_dfs['MortgageTop30Companies_TotalComplaints'].isin([mortcom_sel.value]).any(1)].iloc[:,1].sum())
    # Update the category
    mort_df = 'Mortgage_{}_complaints_TopCompanies'.format(mortcat_sel.value)
    # mort_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(mortcat_sel.value, mortprod_sel.value)
    # mcat = [i for i,val in enumerate(mort_category) if mortcat_sel.value in val]
    # mort_comp_val.text = str(mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[mcat[0],1].sum())
    # Update the graph with the new values
    mlabels = mort_list[mortcat_sel.value]
    mvalues = mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[:,1].to_list()
    msource.data = dict(
        labels=mlabels,
        values=mvalues,
        color=Turbo256[::math.floor(256/len(mlabels))][:len(mlabels)]
    )
    mtitle = [val for val in mort_titles if mortcat_sel.value in val]
    mplot.title.text = mtitle[0]       
    mplot.y_range.factors=mlabels
    
mortcom_sel = Select(title="Choose Company to view:", value=mcompany_list[0], options=mcompany_list)
mortcom_sel.on_change('value', mcompany_update)

# Creating the selector for the category
def mcategory_update(attrname, old, new):
    # Update the category
    mort_df = 'Mortgage_{}_complaints_TopCompanies'.format(mortcat_sel.value)
    # mort_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(mortcat_sel.value, mortprod_sel.value)
    # mcat = [i for i,val in enumerate(mort_category) if mortcat_sel.value in val]
    # mort_comp_val.text = str(mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[mcat[0],1].sum())
    # Update the graph with the new values
    mlabels = mort_list[mortcat_sel.value]
    mvalues = mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[:,1].to_list()
    msource.data = dict(
        labels=mlabels,
        values=mvalues,
        color=Turbo256[::math.floor(256/len(mlabels))][:len(mlabels)]
    )
    mtitle = [val for val in mort_titles if mortcat_sel.value in val]
    mplot.title.text = mtitle[0] 
    mplot.y_range.factors=mlabels

mortcat_sel = Select(title="Choose Category to view complaint distribution:", value=mort_category[0], options=mort_category)
mortcat_sel.on_change('value', mcategory_update)

# # Creating the selector for the sub-category
# def mproduct_update(attrname, old, new):
#     # Update the category
#     mort_df = 'Mortgage_{}_complaints_TopCompanies'.format(mortcat_sel.value)
#     mort_complaints.text = "Total Number of Complaints in the {} Category for sub-category {}:".format(mortcat_sel.value, mortprod_sel.value)
#     mcat = [i for i,val in enumerate(mort_category) if mortcat_sel.value in val]
#     mort_comp_val.text = str(mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[mcat[0],1].sum())
#     # Update the graph with the new values
#     mlabels = mort_list[mortcat_sel.value]
#     mvalues = mort_dfs[mort_df].groupby(['Company']).get_group((mortcom_sel.value)).iloc[:,1].to_list()
#     msource.data = dict(
#         labels=mlabels,
#         values=mvalues,
#         color=Turbo256[::math.floor(256/len(mlabels))][:len(mlabels)]
#     )
#     mtitle = [val for val in mort_titles if mortcat_sel.value in val]
#     mplot.title.text = mtitle[0]
#     mplot.y_range.factors=mlabels

# mortprod_sel = Select(title="Select which Product to view in the chosen Category:", value=mort_list['Issue'][-1], options=mort_list['Issue'])
# mortprod_sel.on_change('value', mproduct_update)

# mselector = column(mortcom_sel, tot_mort_complaints, tot_mort_comp_val, mortcat_sel, mortprod_sel, mort_complaints, mort_comp_val, width=500, margin=(0,50,0,50))
mselector = column(mortcom_sel, tot_mort_complaints, tot_mort_comp_val, mortcat_sel, width=500, margin=(0,50,0,50))
mort_layout = row(mselector, mplot, align='center')

final_layout = column(heading, raw_layout, mid_text, mort_layout, sizing_mode='stretch_both')

# Server display of app
curdoc().add_root(final_layout)
curdoc().title = "Complaints Classifier"

# Local display of app
show(final_layout)