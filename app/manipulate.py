"""
class which can manipulate a dataframe
"""
from bokeh.layouts import row,widgetbox,column,layout
from bokeh.models import Button,ColumnDataSource,TextInput
from bokeh.palettes import viridis
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import DatePicker,TableColumn,DataTable,RadioButtonGroup,Tabs,Panel,Slider,TextInput
import numpy as np

class Manipulator:
    def __init__(self,data_x,data_y,name,p):
        self.name = name
        self.figure = p
        self.data_x = np.asarray(data_x)
        self.data_y = np.asarray(data_y)
        self.mani_data_x = self.data_x
        self.mani_data_y = self.data_y
        self.cds = ColumnDataSource(dict(x=self.mani_data_x,y=self.mani_data_y))
        
        self.y_scale = TextInput(value='1',title="Y scale")
        self.x_scale = TextInput(value='1',title="X scale")
        self.y_offset = TextInput(value='0',title="Y offset")
        self.x_offset = TextInput(value='0',title="X offset")
        
        self.y_scale.on_change('value',self._on_change)
        self.x_scale.on_change('value',self._on_change)
        self.y_offset.on_change('value',self._on_change)
        self.x_offset.on_change('value',self._on_change)
        
        rolling_num = len(self.data_x)//10
        if rolling_num ==0:
            rolling_num=1
        
        self.rolling_average = Slider(start=0,end=rolling_num,value=0,title='rolling average')
        self.rolling_average.on_change('value',self._on_change)

        self.plot_line()
        self.plot_line()

    def show(self):
        x_control = column(self.x_scale,self.x_offset)
        y_control = column(self.y_scale,self.y_offset)
        
        controls = column(children=[x_control,y_control],width=200)

        return widgetbox(children=[self.x_scale,self.x_offset,self.y_scale,self.y_offset,self.rolling_average],width=200)
    
    def update_data(self,data_x,data_y,name=None):
        self.data_x = np.asarray(data_x)
        self.data_y = np.asarray(data_y)
        self.cds.data = dict(x=self.data_x,y=self.data_y)
        print(name)
        if name != None:
            self.name = name
        self._reset()
    
    def _reset(self):
        """
        restore the widgets to their default settings when the data source is changed
        """
        rolling_num = len(self.data_x)//10
        if rolling_num ==0:
            rolling_num=1
        self.rolling_average.end = rolling_num
        self.rolling_average.value = 0
        
        self.y_scale.value = '1'
        self.x_scale.value = '1'
        self.x_offset.value = '0'
        self.y_offset.value = '0'


        self.rolling_average
    def _on_change(self,attr,old,new):
        self.mani_data_y = self.data_y * eval(self.y_scale.value) + eval(self.y_offset.value)
        self.mani_data_x = self.data_x * eval(self.x_scale.value) + eval(self.x_offset.value)
        
        self.mani_data_y = runningMeanFast(self.mani_data_y,self.rolling_average.value)
        self.cds.data=dict(x=self.mani_data_x,y=self.mani_data_y)
        
        
    def plot_line(self):
        self.figure.line(x='x',y='y',source=self.cds,legend=self.name)
        

def runningMeanFast(x, N):
    if N > 0:
        return np.convolve(x, np.ones((N,))/N)[(N-1):]
    else:
        return x


#import random
#x_vals = np.linspace(0,6,5000)
#y_vals=[]
#for x in x_vals:
#    y_vals.append(np.sin(x + random.uniform(-0.1,0.1)))
#x_vals2 = np.linspace(0,6,5000)
#y_vals2=[]
#for x in x_vals2:
#    y_vals2.append(np.cos(x + random.uniform(-0.1,0.1)))
#    
#p = figure(width=600, height=600)
##my = Manipulator(x_vals,y_vals,"001",p)
#my2 = Manipulator(x_vals2,y_vals2,"002",p)
#my_lines=[my,my2]
#my_panels = []

#for line in my_lines:
#    my_panels.append(Panel(child=line.show(),title=line.name))
#manipulate_tabs=Tabs(tabs=my_panels)


#p.legend.click_policy= 'hide'



#curdoc().add_root(row(p,manipulate_tabs))



