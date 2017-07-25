import pandas as pd
from os.path import dirname, join, abspath
import os
import sqlite3

from bokeh.client import push_session
from bokeh.io import curdoc, output_server
from bokeh.layouts import widgetbox, column
from bokeh.models import ColumnDataSource, Slider, MultiSelect, Select, RadioButtonGroup, Button, Paragraph
from bokeh.plotting import figure
from bokeh.charts import Histogram

#Prep Data
#DATA_DIR_OUT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tmp'))
# File locations
db_label = ["Fiscal Year", "Calendar Year", "Fiscal Quarter", "Calendar Quarter"]
db_folder = ["Fiscal_Year", "Calendar_Year", "Fiscal_Quarter", "Calendar_Quarter"]
select_database_dict = dict(zip(db_label, db_folder))
select_database = Select(title="Select a Database", options = db_label, value="Fiscal Year")

dir_name = "/home/isaac/Dropbox/BokehDataCamp/Data_CSV/Fiscal_Year/"


file_names = next(os.walk(dir_name))[-1]
data_names = [f.split(".csv")[0] for f in file_names]

# Load data
total_op = pd.read_csv(dir_name+file_names[0])
total_op.drop('Unnamed: 0', axis = 1, inplace=True)
total_op_old = total_op[total_op["Year"]=="FY2015"]

# Create plots
source = ColumnDataSource(total_op_old)
plot = figure()
plot.circle(x = "index", y = "Operating Income Margin", source=source)

#Create a widget to selet year
year_option = sorted(list(set(total_op["Year"])))
select_years = Select(title="Select a Year", options=year_option, value="FY2015")

# Add a call back
def callback(attr, old, new):
    total_op_new = total_op[total_op["Year"]==select_years.value]
    source.data = ColumnDataSource(total_op_new).data 

select_years.on_change("value", callback)

#Create a widgetbox layout
lay_out = column(widgetbox(select_database, button, para, select_years, width = 500), plot)

#Add the lay_out to the current document
curdoc().add_root(lay_out)
