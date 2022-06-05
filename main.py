import os
import pickle
import pandas as pd
import numpy as np
#from joblib import load

from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource, HoverTool,
                          Label, Paragraph, SingleIntervalTicker, Slider, Select)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure, show

from .load import load_data

raw_dfs, mort_dfs, raw_category, mort_category, raw_titles, mort_titles, raw_list, mort_list = load_data()

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


curdoc().add_root(raw_layout)
curdoc().title = "Complaints Classifier"
