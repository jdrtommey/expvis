"""
class which populates a datatable of experiment runs on a given date
"""
from bokeh.layouts import row,widgetbox,column,layout
from bokeh.models import Button,ColumnDataSource,TextInput
from bokeh.palettes import viridis
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import DatePicker,TableColumn,DataTable,RadioButtonGroup,Tabs,Panel,Slider,TextInput
import numpy as np
from datetime import date
import os

class DataGrab:
    """
    provides a list of available experimental runs.
    Sensitive to the specific folder structure of the e11 lab
    """
    def __init__(self,ROOTFOLDER):
        self.ROOTFOLDER = ROOTFOLDER
        
        self.date_picker =DatePicker(title='Select date of experiment',min_date=date(2017,1,1),max_date=date.today())
        self.date_picker.on_change('value',self._date_callback)

        self.file_data =  dict(
                runid=[],
                address=[],
                filename=[]
            )
        self.file_source = ColumnDataSource(self.file_data)
        self.file_columns = [
                TableColumn(field="runid", title="Run ID"),
                TableColumn(field="filename", title="file name")
            ]
        self.data_table = DataTable(source=self.file_source, columns=self.file_columns,width =300,height=500)


    def _date_callback(self,attr,old,new):
        """
        on change of data, update the datatable showing all runs which can be plotted
        """
        date_string = date_to_file(self.date_picker.value)
        self.data_table.source.data = get_files(self.ROOTFOLDER,date_string[0],date_string[1],date_string[2])

    def show(self):
        return column(self.date_picker,self.data_table)
        
        
##### HELPER FUNCTIONS #####
def get_files(directory,year,month,day):
    """
    given a directory will return a list of all files which match, and their dataframes
    """
    runid = []
    file_address = []
    file_name=[]
    data_frames=[]
    folder = directory + '/' + year + '/' + month + '/' + day  
    for subdir, dirs, files in os.walk(folder):
            if year+month+day in subdir:
                f = subdir.split("_")[1]
                runid.append(f)
                file_address.append(subdir + '/' + files[0])
                file_name.append(files[0])

    list1 = np.array(runid)
    list2 = np.array(file_address)
    list3 = np.array(file_name)


    idx   = np.argsort(list1)

    list1 = np.array(list1)[idx]
    list2 = np.array(list2)[idx]
    list3 = np.array(list3)[idx]

    file_data = dict(runid = list1,address=list2,filename=list3)
    return file_data

def date_to_file(date):
    """
    given a date format will produce the correct formatting for accessing folders.
    months are padded with an additional 0 if single digit
    days are padded with an additional 0
    """
    return [str(date.year),str(date.month).zfill(2),str(date.day).zfill(2)]





