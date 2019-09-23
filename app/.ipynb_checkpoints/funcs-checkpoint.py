from e11 import H5Scan
import pickle

def load_data(year,month,day,file_nums,data_path=''):
    """
    will return the requested data files.
    """
    dfs =[]
    for f in file_nums:
        folder = data_path + year +month + day + "_" + f
        file = year +month +day + '_'+ f+'_scan.h5'
        path = folder + "/" + file
        scan = H5Scan(path) 
        dfs.append(scan.df('analysis'))
    return dfs

    


