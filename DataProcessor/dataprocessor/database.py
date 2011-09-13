#!/usr/bin/env python

# built in imports
import os
import re
from operator import xor

# dependencies
import numpy as np
import tables as tab

def get_cell(datatable, colname, rownum):
    '''
    Returns the contents of a cell in a pytable. Apply unsize_vector correctly
    for padded vectors.

    Parameters
    ----------
    datatable : pytable table
        This is a pointer to the table.
    colname : str
        This is the name of the column in the table.
    rownum : int
        This is the rownumber of the cell.

    Return
    ------
    cell : varies
        This is the contents of the cell.

    '''
    cell = datatable[rownum][colname]
    # if it is a numpy array and the default size then unsize it
    if isinstance(cell, type(np.ones(1))) and cell.shape[0] == 18000:
        numsamp = datatable[rownum]['NINumSamples']
        cell = unsize_vector(cell, numsamp)

    return cell

def get_row_num(runid, table):
    '''
    Returns the row number for a particular run id.

    Parameters
    ----------
    runid : int or string
        The run id.
    table : pytable
        The run data table.

    Returns
    -------
    rownum : int
        The row number for runid.

    '''
    # the row number should be the same as the run id but there is a
    # possibility that it isn't
    rownum = table[int(runid)]['RunID']
    if rownum != int(runid):
        rownum = [x.nrow for x in table.iterrows()
                  if x['RunID'] == int(runid)][0]
        print "The row numbers in the database do not match the run ids!"
    return rownum

def unsize_vector(vector, m):
    '''Returns a vector with the nan padding removed.

    Parameters
    ----------
    vector : numpy array, shape(n, )
        A vector that may or may not have nan padding and the end of the data.
    m : int
        Number of valid values in the vector.

    Returns
    -------
    numpy array, shape(m, )
        The vector with the padding removed. m = samplenum

    '''
    # this case removes the nan padding
    if m < len(vector):
        oldvec = vector[:m]
    elif m > len(vector):
        oldvec = vector
        print('This one is actually longer, you may want to get the ' +
              'complete data, or improve this function so it does that.')
    elif m == len(vector):
        oldvec = vector
    else:
        raise StandardError("Something's wrong with the unsizing")
    return oldvec

def size_array(arr, desiredShape):
    '''Returns a one or two dimensional array that has either been padded with
    nans or reduced in shape.

    Parameters
    ----------
    arr : ndarray, shape(n,) or shape(n,m)
    desiredShape : integer or tuple
        If arr is one dimensinal, then desired shape can be a positive integer,
        else it needs to be a tuple of two positive integers.

    '''

    # this only works for arrays up to dimension 2
    message = "size_array only works with arrays of dimension 1 or 2."
    if len(arr.shape) > 2:
        raise ValueError(message)

    try:
        desiredShape[1]
    except TypeError:
        desiredShape = (desiredShape, 1)

    try:
        arr.shape[1]
        arrShape = arr.shape
    except IndexError:
        arrShape = (arr.shape[0], 1)

    print desiredShape

    # first adjust the rows
    if desiredShape[0] > arrShape[0]:
        try:
            adjRows = np.ones((desiredShape[0], arrShape[1])) * np.nan
        except IndexError:
            adjRows = np.ones(desiredShape[0]) * np.nan
        adjRows[:arrShape[0]] = arr
    else:
        adjRows = arr[:desiredShape[0]]

    newArr = adjRows

    if desiredShape[1] > 1:
        # now adjust the columns
        if desiredShape[1] > arrShape[1]:
            newArr = np.ones((adjRows.shape[0], desiredShape[1])) * np.nan
            newArr[:, :arrShape[1]] = adjRows
        else:
            newArr = adjRows[:, :desiredShape[1]]

    return newArr

def size_vector(vector, m):
    '''Returns a vector with nan's padded on to the end or a slice of the
    vector if length is less than the length of the vector.

    Parameters
    ----------
    vector : numpy array, shape(n, )
        The vector that needs sizing.
    m : int
        The desired length after the sizing.

    Returns
    -------
    newvec : numpy array, shape(m, )

    '''
    nsamp = len(vector)
    # if the desired length is larger then pad witn nan's
    if m > nsamp:
        nans = np.ones(m - nsamp) * np.nan
        newvec = np.append(vector, nans)
    elif m < nsamp:
        newvec = vector[:m]
    elif m == nsamp:
        newvec = vector
    else:
        raise StandardError("Vector sizing didn't work")
    return newvec

def fill_tables(datafile='InstrumentedBicycleData.h5',
                pathToData='../BicycleDAQ/data'):
    '''Adds all the data from the hdf5 files in the h5 directory to the tables.

    Parameters
    ----------
    datafile : string
        Path to the main hdf5 file, typically an empty but structured file:
        `InstrumentedBicycleData.h5`.
    pathToData : string
        Path to the directory containing the raw run data. Both the .mat and
        .h5 files.

    Examples
    --------
    >>>import dataprocessor as dp
    >>># creates a new database with no data
    >>>dp.create_database()
    >>># adds all the data to the database
    >>>dp.fill_tables()

    '''

    # open the hdf5 file for appending
    data = tab.openFile(datafile, mode='a')
    # get the table
    datatable = data.root.data.datatable
    # get the row
    row = datatable.row
    # load the files from the h5 directory
    pathToRunH5 = os.path.join(pathToData, 'h5')
    files = sorted(os.listdir(pathToRunH5))

    print "Loading run data."

    # fill the rows with data
    for rownum, run in enumerate(files):
        print 'Adding run: %s to row number: %d' % (run, rownum)
        rundata = get_run_data(os.path.join(pathToRunH5, run))
        for par, val in rundata['par'].items():
            row[par] = val
        # only take the first 18000 samples for all runs
        for i, col in enumerate(rundata['NICols']):
            try:
                row[col] = size_vector(rundata['NIData'][i], 18000)
            except KeyError:
                print "Not including the %s measurement" % col
            except IndexError:
                print "%s was not measured" % col
        for i, col in enumerate(rundata['VNavCols']):
            row[col] = size_vector(rundata['VNavData'][i], 18000)
        row.append()
    datatable.flush()

    print "Loading signal data."
    # fill in the signal table
    signaltable = data.root.data.signaltable
    row = signaltable.row

    # these are data signals that will be created from the raw data
    processedCols = ['FrameAccelerationX',
                     'FrameAccelerationY',
                     'FrameAccelerationZ',
                     'PitchRate',
                     'PullForce',
                     'RearWheelRate',
                     'RollAngle',
                     'RollRate',
                     'ForwardSpeed',
                     'SteerAngle',
                     'SteerRate',
                     'SteerTorque',
                     'tau',
                     'YawRate']

    # get two example runs
    filteredRun, unfilteredRun = get_two_runs(pathToRunH5)

    niCols = filteredRun['NICols']
    # combine the VNavCols from unfiltered and filtered
    vnCols = set(filteredRun['VNavCols'] + unfilteredRun['VNavCols'])

    vnUnitMap = {'MagX': 'unitless',
                 'MagY': 'unitless',
                 'MagZ': 'unitless',
                 'AccelerationX': 'meter/second/second',
                 'AccelerationY': 'meter/second/second',
                 'AccelerationZ': 'meter/second/second',
                 'AngularRateX': 'radian/second',
                 'AngularRateY': 'radian/second',
                 'AngularRateZ': 'radian/second',
                 'AngularRotationX': 'degree',
                 'AngularRotationY': 'degree',
                 'AngularRotationZ': 'degree',
                 'Temperature': 'kelvin'}

    for sig in set(niCols + list(vnCols) + processedCols):
        row['signal'] = sig

        if sig in niCols:
            row['source'] = 'NI'
            row['isRaw'] = True
            row['units'] = 'volts'
            if sig.startswith('FrameAccel') or sig == 'SteerRateGyro':
                row['calibration'] = 'bias'
            elif sig.endswith('Potentiometer'):
                row['calibration'] = 'interceptStar'
            elif sig in ['WheelSpeedMotor', 'SteerTorqueSensor',
                         'PullForceBridge']:
                row['calibration'] = 'intercept'
            elif sig[:-1].endswith('Bridge'):
                row['calibration'] = 'matrix'
            else:
                row['calibration'] = 'none'
        elif sig in vnCols:
            row['source'] = 'VN'
            row['isRaw'] = True
            row['calibration'] = 'none'
            row['units'] = vnUnitMap[sig]
        elif sig in processedCols:
            row['source'] = 'NA'
            row['isRaw'] = False
            row['calibration'] = 'na'
        else:
            raise KeyError('{0} is not raw or processed'.format(sig))

        row.append()

    signaltable.flush()

    print "Loading calibration data."
    # fill in the calibration table
    calibrationtable = data.root.data.calibrationtable
    row = calibrationtable.row

    # load the files from the h5 directory
    pathToCalibH5 = os.path.join(pathToData, 'CalibData', 'h5')
    files = sorted(os.listdir(pathToCalibH5))

    for f in files:
        print "Calibration file:", f
        calibDict = get_calib_data(os.path.join(pathToCalibH5, f))
        for k, v in calibDict.items():
            if k in ['x', 'y', 'v']:
                row[k] = size_vector(v, 50)
            else:
                row[k] = v
        row.append()

    calibrationtable.flush()

    data.close()

    print datafile, "ready for action!"

def replace_corrupt_strings_with_nan(vnOutput, vnCols):
    '''Returns a numpy matrix with the VN-100 output that has the corrupt
    values replaced by nan values.

    Parameters
    ----------
    vnOutput : list
        The list of output strings from an asyncronous reading from the VN-100.
    vnCols : list
        A list of the column names for this particular async output.

    Returns
    -------
    vnData : array (m, n)
        An array containing the corrected data values. n is the number of
        samples and m is the number of signals.

    '''

    vnData = []

    nanRow = [np.nan for i in range(len(vnCols))]

    # go through each sample in the vn-100 output
    for i, vnStr in enumerate(vnOutput):
        # parse the string
        vnList, chkPass, vnrrg = parse_vnav_string(vnStr)
        # if the checksum passed, then append the data unless vnList is not the
        # correct length, (this is because run139 sample 4681 seems to calculate the correct
        # checksum for an incorrect value)
        if chkPass and len(vnList[1:-1]) == len(vnCols):
            vnData.append([float(x) for x in vnList[1:-1]])
        # if not append some nan values
        else:
            if i == 0:
                vnData.append(nanRow)
            # there are typically at least two corrupted samples combine into
            # one
            else:
                vnData.append(nanRow)
                vnData.append(nanRow)

    # remove extra values so that the number of samples equals the number of
    # samples of the VN-100 output
    vnData = vnData[:len(vnOutput)]

    return np.transpose(np.array(vnData))

def parse_vnav_string(vnStr):
    '''Returns a list of the information in a VN-100 text string and whether
    the checksum failed.

    Parameters
    ----------
    vnStr : string
        A string from the VectorNav serial output (UART mode).

    Returns
    -------
    vnlist : list
        A list of each element in the VectorNav string.
        ['VNWRG', '26', ..., ..., ..., checksum]
    chkPass : boolean
        True if the checksum is correct and false if it isn't.
    vnrrg : boolean
        True if the str is a register reading, false if it is an async
        reading, and None if chkPass is false.

    '''
    # calculate the checksum of the raw string
    calcChkSum = vnav_checksum(vnStr)
    #print('Checksum for the raw string is %s' % calcChkSum)

    # get rid of the $ and the newline characters
    vnMeat = re.sub('''(?x) # verbose
                       \$ # match the dollar sign at the beginning
                       (.*) # this is the content
                       \* # match the asterisk
                       (\w*) # the checksum
                       \s* # the newline characters''', r'\1,\2', vnStr)

    # make it a list with the last item being the checksum
    vnList = vnMeat.split(',')

    # set the vnrrg flag
    if vnList[0] == 'VNRRG':
        vnrrg = True
    else:
        vnrrg = False

    #print("Provided checksum is %s" % vnList[-1])
    # see if the checksum passes
    chkPass = calcChkSum == vnList[-1]
    if not chkPass:
        #print "Checksum failed"
        #print vnStr
        vnrrg = None

    # return the list, whether or not the checksum failed and whether or not it
    # is a VNRRG
    return vnList, chkPass, vnrrg

def vnav_checksum(vnStr):
    '''
    Returns the checksum in hex for the VN-100 string.

    Parameters
    ----------
    vnStr : string
        Of the form '$...*X' where X is the two digit checksum.

    Returns
    -------
    chkSum : string
        Two character hex representation of the checksum. The letters are
        capitalized and single digits have a leading zero.

    '''
    chkStr = re.sub('''(?x) # verbose
                       \$ # match the dollar sign
                       (.*) # match the stuff the checksum is calculated from
                       \* # match the asterisk
                       \w* # the checksum
                       \s* # the newline characters''', r'\1', vnStr)

    checksum = reduce(xor, map(ord, chkStr))
    # remove the first '0x'
    hexVal = hex(checksum)[2:]

    # if the hexVal is only a single digit, it needs a leading zero to match
    # the VN-100's output
    if len(hexVal) == 1:
        hexVal = '0' + hexVal

    # the letter's need to be capitalized to match too
    return hexVal.upper()

def get_two_runs(pathToH5):
    '''Gets the data from both a filtered and unfiltered run.'''

    # load in the data files
    files = sorted(os.listdir(pathToH5))

    # get an example filtered and unfiltered run (wrt to the VN-100 data)
    filteredRun = get_run_data(os.path.join(pathToH5, files[0]))
    if filteredRun['par']['ADOT'] is not 14:
        raise ValueError('Run %d is not a filtered run, choose again' %
              filteredRun['par']['RunID'])

    unfilteredRun = get_run_data(os.path.join(pathToH5, files[-1]))
    if unfilteredRun['par']['ADOT'] is not 253:
        raise ValueError('Run %d is not a unfiltered run, choose again' %
              unfilteredRun['par']['RunID'])

    return filteredRun, unfilteredRun

def load_database(filename='InstrumentedBicycleData.h5', mode='r'):
    '''Returns the a pytables database.'''
    return tab.openFile(filename, mode=mode)

def create_database(filename='InstrumentedBicycleData.h5',
                    pathToH5='../BicycleDAQ/data/h5',
                    compression=False):
    '''Creates an HDF5 file for data collected from the instrumented
    bicycle.'''

    if os.path.exists(filename):
        response = raw_input(('{0} already exists.\n' +
            'Do you want to overwrite it? (y or n)\n').format(filename))
        if response == 'y':
            print "{0} will be overwritten".format(filename)
            pass
        else:
            print "{0} was not overwritten.".format(filename)
            return

    print "Creating database..."

    # open a new hdf5 file for writing
    data = tab.openFile(filename, mode='w',
                        title='Instrumented Bicycle Data')
    # create a group for the data
    rgroup = data.createGroup('/', 'data', 'Data')

    # generate the signal table description class
    SignalTable = create_signal_table_class()
    # add the signal table to the group
    sTable = data.createTable(rgroup, 'signaltable',
                              SignalTable, 'Signal Information')
    sTable.flush()

    # generate the calibration table description class
    CalibrationTable = create_calibration_table_class()
    # add the calibration table to the group
    cTable = data.createTable(rgroup, 'calibrationtable',
                              CalibrationTable, 'Calibration Information')
    cTable.flush()

    # get two example runs
    filteredRun, unfilteredRun = get_two_runs(pathToH5)
    # generate the table description class
    RunTable = create_run_table_class(filteredRun, unfilteredRun)
    if compression:
        # setup up a compression filter
        fil = tab.Filters(complevel=1, complib='zlib')
        # add the data table to this group
        rtable = data.createTable(rgroup, 'datatable',
                                  RunTable, 'Run Data',
                                  filters=fil)
    else:
        # add the data table to this group
        rtable = data.createTable(rgroup, 'datatable',
                                  RunTable, 'Run Data')

    rtable.flush()

    data.close()

    print "{0} successfuly created.".format(filename)

def create_signal_table_class():
    '''Creates a class that is used to describe the table containing
    information about the signals.'''

    class SignalTable(tab.IsDescription):
        calibration = tab.StringCol(20)
        isRaw = tab.BoolCol()
        sensor = tab.StringCol(20)
        signal = tab.StringCol(20)
        source = tab.StringCol(2)
        units = tab.StringCol(20)

    return SignalTable

def create_calibration_table_class():
    '''Creates a class that is used to describe the table containing the
    calibration data.'''

    class CalibrationTable(tab.IsDescription):
        accuracy = tab.StringCol(10)
        bias = tab.Float32Col(dflt=np.nan)
        calibrationID = tab.StringCol(5)
        calibrationSupplyVoltage = tab.Float32Col(dflt=np.nan)
        name = tab.StringCol(20)
        notes = tab.StringCol(500)
        offset = tab.Float32Col(dflt=np.nan)
        runSupplyVoltage = tab.Float32Col(dflt=np.nan)
        runSupplyVoltageSource = tab.StringCol(10)
        rsq = tab.Float32Col(dflt=np.nan)
        sensorType = tab.StringCol(20)
        signal = tab.StringCol(26)
        slope = tab.Float32Col(dflt=np.nan)
        timeStamp = tab.StringCol(21)
        units = tab.StringCol(20)
        v = tab.Float32Col(shape=(50,))
        x = tab.Float32Col(shape=(50,))
        y = tab.Float32Col(shape=(50,))

    return CalibrationTable

def create_run_table_class(filteredrun, unfilteredrun):
    '''Returns a class that is used for the table description for raw data
    for each run.

    Parameters
    ----------
    filteredrun : dict
        Contains the python dictionary of a run with filtered VN-100 data.
    unfilteredrun : dict
        Contains the python dictionary of a run with unfiltered VN-100 data.

    Returns
    -------
    Run : class
        Table description class for pytables with columns defined.

    '''

    # combine the VNavCols from unfiltered and filtered
    VNavCols = set(filteredrun['VNavCols'] + unfilteredrun['VNavCols'])

    # these columns may be used in the future but for now there is no reason to
    # introduce them into the database
    ignoredNICols = (['SeatpostBridge' + str(x) for x in range(1, 7)] +
                     [x + 'Potentiometer' for x in ['Hip', 'Lean', 'Twist']] +
                     [x + 'FootBridge' + y for x, y in zip(['Right', 'Left'], ['1', '2'])])

    for col in ignoredNICols:
        unfilteredrun['NICols'].remove(col)

    # set up the table description
    class RunTable(tab.IsDescription):
        # add all of the column headings from par, NICols and VNavCols
        for i, col in enumerate(unfilteredrun['NICols']):
            exec(col + " = tab.Float32Col(shape=(18000, ), pos=i)")
        for k, col in enumerate(VNavCols):
            exec(col + " = tab.Float32Col(shape=(18000, ), pos=i+1+k)")
        for i, (key, val) in enumerate(unfilteredrun['par'].items()):
            pos = k + 1 + i
            if isinstance(val, type(1)):
                exec(key + " = tab.Int32Col(pos=pos)")
            elif isinstance(val, type('')):
                exec(key + " = tab.StringCol(itemsize=300, pos=pos)")
            elif isinstance(val, type(1.)):
                exec(key + " = tab.Float32Col(pos=pos)")
            elif isinstance(val, type(np.ones(1))):
                exec(key + " = tab.Float32Col(shape=(" + str(len(val)) + ", ), pos=pos)")

        # add the columns for the processed data
        processedCols = ['FrameAccelerationX',
                         'FrameAccelerationY',
                         'FrameAccelerationZ',
                         'PitchRate',
                         'PullForce',
                         'RearWheelRate',
                         'RollAngle',
                         'RollRate',
                         'ForwardSpeed',
                         'SteerAngle',
                         'SteerRate',
                         'SteerTorque',
                         'tau',
                         'YawRate']

        for k, col in enumerate(processedCols):
            if col == 'tau':
                exec(col + " = tab.Float32Col(pos=i + 1 + k)")
            else:
                exec(col + " = tab.Float32Col(shape=(18000, ), pos=i + 1 + k)")

        # get rid intermediate variables so they are not stored in the class
        del(i, k, col, key, pos, val, processedCols)

    return RunTable

def get_run_data(pathtofile):
    '''
    Returns data from the run h5 files using pytables and formats it better
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

    # put the parameters into a dictionary
    rundata['par'] = {}
    for col in runfile.root.par:
        # convert them to regular python types
        try:
            if col.name == 'Speed':
                rundata['par'][col.name] = float(col.read()[0])
            else:
                rundata['par'][col.name] = int(col.read()[0])
        except:
            pstr = str(col.read()[0])
            rundata['par'][col.name] = pstr
            if pstr[0] == '$':
                parsed = parse_vnav_string(pstr)[0][2:-1]
                if len(parsed) == 1:
                    try:
                        parsed = int(parsed[0])
                    except:
                        parsed = parsed[0]
                else:
                    parsed = np.array([float(x) for x in parsed])
                rundata['par'][col.name] = parsed

    if 'Notes' not in rundata['par'].keys():
        rundata['par']['Notes'] = ''

    # get the NIData
    rundata['NIData'] = runfile.root.NIData.read()

    # get the VN-100 data column names
    # make the array into a list of python string and gets rid of unescaped
    # control characters
    columns = [re.sub(r'[^ -~].*', '', str(x))
               for x in runfile.root.VNavCols.read()]
    # gets rid of white space
    rundata['VNavCols'] = [x.replace(' ', '') for x in columns]

    # get the NI column names
    # make a list of NI columns from the InputPair structure from matlab
    rundata['NICols'] = []
    for col in runfile.root.InputPairs:
        rundata['NICols'].append((str(col.name), int(col.read()[0])))

    rundata['NICols'].sort(key=lambda x: x[1])

    rundata['NICols'] = [x[0] for x in rundata['NICols']]

    # get the VNavDataText
    rundata['VNavDataText'] = [re.sub(r'[^ -~].*', '', str(x))
                               for x in runfile.root.VNavDataText.read()]

    # redefine the NIData using parsing that accounts for the corrupt values
    # better
    rundata['VNavData'] = replace_corrupt_strings_with_nan(
                           rundata['VNavDataText'],
                           rundata['VNavCols'])

    # close the file
    runfile.close()

    return rundata

def get_calib_data(pathToFile):
    '''
    Returns calibration data from the run h5 files using pytables and
    formats it as a dictionairy.

    Parameters
    ----------
    pathToFile : string
        The path to the h5 file that contains the calibration data, normally:
        pathtofile = '../BicycleDAQ/data/CalibData/h5/00000.h5'

    Returns
    -------
    calibData : dictionary
        A dictionary that looks similar to how the data was stored in Matlab.

    '''

    calibFile = tab.openFile(pathToFile)

    calibData = {}

    for thing in calibFile.root.data:
        if len(thing.read().flatten()) == 1:
            calibData[thing.name] = thing.read()[0]
        else:
            if thing.name in ['x', 'v']:
                try:
                    calibData[thing.name] = np.mean(thing.read(), 1)
                except ValueError:
                    calibData[thing.name] = thing.read()
            else:
                calibData[thing.name] = thing.read()

    calibFile.close()

    return calibData
