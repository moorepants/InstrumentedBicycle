import tables as tab
import numpy as np
import os

def get_run_data(pathtofile):
    '''Returns data from the run h5 files using pytables and formats it better
    for python.

    Parameters
    ----------
    pathtofile : string
        The path to the h5 file that contains run data.

    Returns
    -------
    rundata : dictionary
        A dictionary that looks similar to how the data was stored in Matlab.

    '''

    # open the file
    runfile = tab.openFile(pathtofile)

    # intialize a dictionary for storage
    rundata = {}

    # first let's get the NIData and VNavData
    rundata['NIData'] = runfile.root.NIData.read()
    rundata['VNavData'] = runfile.root.VNavData.read()

    # now create two lists that give the column headings for the two data sets
    rundata['VNavCols'] = list(runfile.root.VNavCols.read())
    rundata['NICols'] = []
    for col in runfile.root.InputPairs:
        rundata['NICols'].append((col.name, int(col.read()[0])))

    rundata['NICols'].sort(key=lambda x: x[1])

    rundata['NICols'] = [x[0] for x in rundata['NICols']]

    # put the parameters into a dictionary
    rundata['par'] = {}
    for col in runfile.root.par:
        rundata['par'][col.name] = col.read()[0]

    # get the VNavDataText
    rundata['VNavDataText'] = list(runfile.root.VNavDataText.read())

    # close the file
    runfile.close()

    return rundata
