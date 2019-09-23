import numpy as np
from bokeh.layouts import row,widgetbox,column,layout
from bokeh.models import Button,ColumnDataSource,TextInput
from bokeh.palettes import viridis
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import DatePicker,TableColumn,DataTable,RadioButtonGroup,Tabs,Panel,Slider
from datetime import date
import os
import pandas as pd
from e11 import H5Scan


from manipulate import Manipulator
from datagrabber import DataGrab

DATAFOLDER = os.path.expanduser('~/Documents/work/data')


#######
## GET FILES
#######

data_grabber = DataGrab(DATAFOLDER) #Date-picker which controls the day for which the experimental runs are returned
def on_table_change(attr,old,new):
    """
    when the selection in the data_grabber table is changed run the update plot script
    """
    update_plot_data()
data_grabber.file_source.selected.on_change('indices', on_table_change)


#######
## COVERT INTO PLOTTABLE DATAFRAME
#######

def get_radio():
    """
    chooses which of the returned data columns is plotted 
    """
    options_dict = {0:'f',1:'a0',2:'a1',3:'a2'}
    return options_dict[data_radios.active]
def radio_callback(attr, old, new):
    update_plot_data()
data_radios = RadioButtonGroup(labels=["f", "a0", "a1","a2"], active=0)
data_radios.on_change('active',radio_callback)

#######
## GENERATE MANIPLUABLE LINE PLOTS
#######

p = figure(width=600, height=600)
manny_on_the_map = Manipulator([0],[0],"empty",p)



def update_plot_data():
    selectionIndex=data_grabber.file_source.selected.indices[0]
    df = H5Scan(data_grabber.file_source.data['address'][selectionIndex]).df('analysis')
    data_option = get_radio()
    manny_on_the_map.update_data(df['v0'],df[data_option],name=data_grabber.file_source.data['runid'][selectionIndex])

    
p.legend.click_policy= 'hide'
data_option_box = widgetbox(children=[data_radios],sizing_mode='scale_width')
layout_basic = layout(row(children=[data_grabber.show(),p,column(data_option_box,manny_on_the_map.show())]))
panel_basic = Panel(child=layout_basic,title='basic')
basic = Tabs(tabs=[panel_basic])


curdoc().add_root(basic)
