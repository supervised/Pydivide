# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

import datetime
from scipy import interpolate
import numpy as np
import pandas as pd

import pytplot as tplot


def resample(kp, time, sc_only=False):
    '''
    Modifies KP structure index to user specified time via interpolation.

    Parameters:
        kp: struct
            KP insitu data structure read from file(s).
        time: list
            Specifies subset of insitu KP data for resampling. time must be expressed in the format ‘YYYY-MM-DD HH:MM:SS’.

    Examples:
        >>> # Resample insitu time to 2016-06-20 coarse survey 3D file time.
        >>> swi_cdf = cdflib.CDF('<dir_path>/mvn_swi_l2_coarsesvy3d_20160620_v01_r00.cdf')
        >>> newtime = swi_cdf.varget('time_unix')
        >>> insitu_resampled = pydivide.resample(insitu, newtime)

        >>> # Resamples an entire day of data to just 3 points
        >>> import pytplot
        >>>insitu, iuvs = pydivide.read(input_time=['2016-02-18', '2016-02-19'])
        >>> x = pydivide.resample(insitu, [pytplot.tplot_utilities.str_to_int('2016-02-18T05:00:00'),
        >>>                      pytplot.tplot_utilities.str_to_int('2016-02-18T10:00:00'),
        >>>                      pytplot.tplot_utilities.str_to_int('2016-02-18T15:00:00')])
    '''
    new_total = len(time)
    start_time = time[0]
    end_time = time[new_total - 1]
    
    if start_time < kp['Time'][0]:
        print('The requested start time is before the earliest data point in the input data structure.')
        print('This routine DOES NOT extrapolate. Please read in more KP data that covers the requested time span.')
        return
    
    if end_time > kp['Time'][len(kp['Time']) - 1]:
        print('The requested end time is after the latest data point in the input data structure.')
        print('This routine DOES NOT extrapolate. Please read in more KP data that covers the requested time span.')
        return

    # Set up the instrument dataframes
    if kp['LPW'] is not None:
        lpw = kp['LPW']
    else:
        lpw = None
    if kp['MAG'] is not None:
        mag = kp['MAG']
    else:
        mag = None
    if kp['EUV'] is not None:
        euv = kp['EUV']
    else:
        euv = None
    if kp['SWEA'] is not None:
        swea = kp['SWEA']
    else:
        swea = None
    if kp['SWIA'] is not None:
        swia = kp['SWIA']
    else:
        swia = None
    if kp['NGIMS'] is not None:
        ngims = kp['NGIMS']
    else:
        ngims = None
    if kp['SEP'] is not None:
        sep = kp['SEP']
    else:
        sep = None
    if kp['STATIC'] is not None:
        static = kp['STATIC']
    else:
        static = None
        
    app = kp['APP']
    spacecraft = kp['SPACECRAFT']
    io_flag = kp['IOflag']
    orbit = kp['Orbit']
    time_orig = kp['TimeString']
    timeunix = kp['Time']

    # Set up instrument list to make it easy to loop through the next parts
    inst_names = ['LPW', 'EUV', 'SWEA', 'SWIA', 'STATIC', 'SEP', 'MAG', 'NGIMS', 'APP', 'SPACECRAFT']
    inst_tags = [lpw, euv, swea, swia, static, sep, mag, ngims, app, spacecraft]

    # Create an array of the old times
    old_time = timeunix

    # Find the closest values for all nearest neighbor interpolations
    closest_values = []
    for k in range(len(time)):
        if isinstance(time[k], str):
            time_ = tplot.tplot_utilities.str_to_int(time[k])
        else:
            time_ = time[k]
        closest_value_index = np.absolute(old_time.values - time_).argmin()
        closest_values.append((old_time.values - time_)[closest_value_index] + time_)

    # Get the new indexes of the dataframes based on the time
    new_time_strings = []
    for i in range(len(time)):
        if isinstance(time[i], str):
            new_time_strings.append(time[i])
        else:
            new_time_strings.append(datetime.datetime.utcfromtimestamp(time[i], ).strftime('%Y-%m-%dT%H:%M:%S'))
    new_time_series = pd.Series(new_time_strings)
    
    # Orbit Series
    spline_function = interpolate.interp1d(old_time.values, orbit.values)
    # In order for the spline_function to work, need to make sure that we're working with the integer form of time,
    # in seconds since the epoch, not datetime times
    if not isinstance(time[0], int):
        time_int = [tplot.tplot_utilities.str_to_int(t) for t in time]
        temp_series = pd.Series(spline_function(time_int))
    elif isinstance(time[0], int):
        if not isinstance(time, list):
            time.values = list(time)
        temp_series = pd.Series(spline_function(time))

    temp_df = temp_series.to_frame('Orbit')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    orbit = temp_df.iloc[:, 0]
        
    # Time String Series
    temp_series = new_time_series
    temp_df = temp_series.to_frame('Time')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    time = temp_df.iloc[:, 0]
        
    # Time Unix Series
    temp_series = pd.Series(time)
    temp_df = temp_series.to_frame('Time')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    timeunix = temp_df.iloc[:, 0]
        
    # IOFlag Series
    temp_series = []
    for k in range(len(time)):
        temp_series.append(kp['IOflag'][kp['Time'] == closest_values[k]])
    temp_series = pd.Series(temp_series)
    temp_df = temp_series.to_frame('IOflag')
    temp_df['Time Index'] = new_time_series
    temp_df.set_index('Time Index', drop=True, inplace=True)
    io_flag = temp_df.iloc[:, 0]

    # Instrument Dataframes
    
    # For each instrument:
    for i in range(len(inst_names)):
        if inst_tags[i] is not None:
            dataframe_initalized = False
            # For each observation mode:
            for obs in kp[inst_names[i]].columns:
                column_is_string = False
                # Check if the observation is a string variable.
                # If it is a string, you can't interpolate between two strings, so use nearest neighbor.
                # Else, use a cubic spline interpolation
                for j in range(len(kp[inst_names[i]][obs])):
                    # Note: Looking through all of these is REALLY SLOW
                    # Without hard coding the observation names that are strings,
                    # is there a way to make this faster?
                    if isinstance(kp[inst_names[i]][obs][j], str):
                        column_is_string = True
                        break
                    if isinstance(kp[inst_names[i]][obs][j], float) and np.isfinite(kp[inst_names[i]][obs][j]):
                        column_is_string = False
                        break
                if column_is_string:
                    temp_series = []
                    for k in range(len(time)):
                        temp_series.append(kp[inst_names[i]][obs][kp['Time'] == closest_values[k]])
                    temp_series = pd.Series(temp_series)
                else:
                    spline_function = interpolate.interp1d(old_time.values, kp[inst_names[i]][obs].values)

                    # In order for the spline_function to work, need to make sure that we're working with the integer
                    # form of time, in seconds since the epoch, not datetime times
                    if not isinstance(time.values[0], int):
                        time_int = [tplot.tplot_utilities.str_to_int(t) for t in time.values]
                        temp_series = pd.Series(spline_function(time_int))
                    elif isinstance(time.values[0], int):
                        if not isinstance(time.values, list):
                            time.values = list(time.values)
                        temp_series = pd.Series(spline_function(time.values))
                # Turn the series into a dataframe if it hasn't been done yet.
                # Else, add it to the dataframe
                if not dataframe_initalized:
                    temp_df = temp_series.to_frame(obs)
                    dataframe_initalized = True
                    temp_df['Time Index'] = new_time_series
                else:
                    temp_df[obs] = temp_series
            # Set the "Time Index" column as the index of the dataframe
            temp_df.set_index('Time Index', drop=True, inplace=True)
            inst_tags[i] = temp_df

    # Set up and return the new KP data structure
    tag_names = ['TimeString', 'Time', 'Orbit', 'IOflag', 'LPW', 'EUV', 'SWEA', 'SWIA', 'STATIC', 'SEP', 'MAG',
                 'NGIMS', 'APP', 'SPACECRAFT']
    # Define list of first level data structures
    data_tags = [time, timeunix, orbit, io_flag,
                 inst_tags[0], inst_tags[1], inst_tags[2], inst_tags[3], inst_tags[4], 
                 inst_tags[5], inst_tags[6], inst_tags[7], inst_tags[8], inst_tags[9]]
    # return a dictionary made from tag_names and data_tags
    kp_new = (dict(zip(tag_names, data_tags)))
    
    return kp_new
