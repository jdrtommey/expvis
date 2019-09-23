"""
functions to deal with populating the datasource with files.
"""
import os
import datetime
from e11 import H5Scan

def get_files(directory,year,month,day):
    """
    given a directory will return a list of all files which match, and their dataframes
    """
    runs = []
    folder = directory + '/' + year + '/' + month + '/' + day  
    for subdir, dirs, files in os.walk(folder):
            if year+month+day in subdir:
                f = subdir.split("_")[1]
                df = H5Scan(subdir + '/' + files[0]).df('analysis')
                runs.append([f,df])
    runs.sort()    
    
    return runs

## Build the layout for selecting data

def date_to_file(date):
    """
    given a date format will produce the correct formatting for accessing folders.
    months are padded with an additional 0 if single digit
    days are padded with an additional 0
    """
    return [str(date.year),str(date.month).zfill(2),str(date.day).zfill(2)]


