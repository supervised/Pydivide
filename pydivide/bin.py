# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

from .utilities import get_inst_obs_labels
from .utilities import initialize_list
from .utilities import place_values_in_list
from .utilities import get_values_from_list
import math
import numpy


def bin(kp,
        parameter=None,
        bin_by=None,
        mins=None,
        maxs=None,
        binsize=None,
        std=False,
        avg=False,
        density=False,
        median=False,
        unittest=False):
    '''
    Bins insitu Key Parameters by up to 8 different parameters, specified within
    the data structure. Necessary that at least one of avg, std, median, or
    density be specified.

    Parameters:
        kp: struct
            KP insitu data structure read from file(s).
        parameter: str
            Key Parameter to be binned. Only one may be binned at a time.
        bin_by: int, str
            Parameters (index or name) by which to bin the specified Key Parameter.
        binsize: int, list
        Bin size for each binning dimension. Number of elements must be equal to those in bin_by.
        mins: int, list
            Minimum value(s) for each binning scheme. Number of elements must be equal to those in bin_by.
        maxs: int, list 7
            Maximum value(s) for each binning scheme. Number of elements must be equal to those in bin_by.
        avg: bool
            Calculate average per bin.
        std: bool
            Calculate standard deviation per bin.
        density: bool
            Returns number of items in each bin.
        median: bool
            Calculate median per bin.

    Returns:
        This procedures outputs up to 4 arrays to user-defined variables, corresponding to avg, std, median, and density.

    Examples:
    >>> # Bin STATIC O+ characteristic energy by spacecraft latitude (1° resolution) and longitude (2° resolution).
    >>> output_avg = pydivide.bin(insitu, parameter='static.oplus_char_energy', bin_by=['spacecraft.geo_latitude', 'spacecraft.geo_longitude'], avg=True,binsize=[2,1])

    >>> # Bin SWIA H+ density by spacecraft altitude (10km resolution), return average value and standard deviation for each bin.
    >>> output_avg,output_std = pydivide.bin(insitu, parameter='swia.hplus_density', bin_by='spacecraft.altitude', binsize=10,avg=True,std=True)
    '''
    # ERROR CHECKING
    if not isinstance(bin_by, list):
        bin_by = [bin_by]
    
    if parameter is None:
        print("Must provide an index (or name) for param to be plotted.")
        return
    
    if bin_by is None:
        print("Must provide parameters to be binned by.")
        return
    
    if not avg and not std and not median and not density:
        print("Must select array(s) to return (avg, std, median, density).")
        return
    
    if not hasattr(binsize, "__len__"):
        temp = []
        temp.append(binsize)
        binsize = temp
    if mins is not None and not hasattr(mins, "__len__"):
        temp = []
        temp.append(mins)
        mins = temp
    if maxs is not None and not hasattr(maxs, "__len__"):
        temp = []
        temp.append(maxs)
        maxs = temp

    # Store instrument and observation of parameter in lists
    inst = []
    obs = []
    if type(parameter) is int or type(parameter) is str:
        a, b = get_inst_obs_labels(kp, parameter)
        inst.append(a)
        obs.append(b)
    else:
        for param in parameter:
            a, b = get_inst_obs_labels(kp, param)
            inst.append(a)
            obs.append(b)
    parameter_inst_obs = list(zip(inst, obs))

    # Store instrument and observation of "bin by" values in lists
    inst = []
    obs = []
    for param in bin_by:
        a, b = get_inst_obs_labels(kp, param)
        inst.append(a)
        obs.append(b)       
    bin_by_inst_obs = list(zip(inst, obs))

    # Calculate the dimensions of the binned array
    # Using the min/max values and the bin sizes
    total_fields = len(bin_by)
    ranges = []
    total_bins = []
    if mins is None:
        mins = []
        for inst, obs in bin_by_inst_obs:
            min_temp = kp[inst][obs].min(skipna=True)
            if math.isnan(min_temp):
                print("All " + obs + " data is NaN.  Cannot bin by this parameter.")
                return 
            mins.append(min_temp)
    if maxs is None:
        maxs = []
        for inst, obs in bin_by_inst_obs:
            maxs.append(kp[inst][obs].max(skipna=True))
        
    for i in range(total_fields):
        if maxs[i] - mins[i] < 0:
            print("ERROR: Minimum value of " + str(mins[i]) + " is greater than the maximum value of " + str(maxs[i]))
            print("for bin-by parameter " + bin_by_inst_obs[i][1] + ".  Returning...")
            return
        ranges.append(maxs[i] - mins[i])
        total_bins.append(int(math.ceil(ranges[i] / binsize[i])))

    # Initialize the binned_list (a list of every value at a certain bin)
    # Initialize the density array (the number of values binned into a bin)
    binned_array = numpy.zeros(total_bins)
    density_array = numpy.zeros(total_bins)
    binned_list = binned_array.tolist()
    binned_list = initialize_list(binned_list)

    # Loop through the KP to place the data into the correct bin
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        bad_val = False

        # Cannot do anything with NaNs.  Ignore them and continue.
        if math.isnan(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i]):
            continue

        # Find out where to place i
        j = 0
        data_value_indexes = []
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            # Ignore if NaN or out of range
            if math.isnan(data_value) or data_value < mins[j] or data_value > maxs[j]:
                bad_val = True
                continue
            dv = math.floor((data_value - mins[j]) / binsize[j])
            data_value_indexes.append(int(dv))
            j += 1
            
        if bad_val:
            continue

        # Populate binned_list in the proper spot, and add one to the density at that spot
        data_value_indexes = tuple(data_value_indexes)
        place_values_in_list(binned_list, data_value_indexes, kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i])
        density_array[data_value_indexes] = density_array[data_value_indexes] + 1

    # Create arrays based on keywords
    if median:
        median_array = numpy.zeros(total_bins)
        median_array.fill(numpy.nan)
    if avg:
        average_array = numpy.zeros(total_bins)
        average_array.fill(numpy.nan)
    if std:
        std_array = numpy.zeros(total_bins)
        std_array.fill(numpy.nan)

    # Loop through the KP one more time to calculate median, avg, std.
    # This is necessary because we cannot calculate the median without knowing all the numbers
    # in each bin first.
    for i in range(len(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]])):
        bad_val = False

        # Cannot do anything with NaNs.  Ignore them and continue.
        if math.isnan(kp[parameter_inst_obs[0][0]][parameter_inst_obs[0][1]][i]):
            continue

        # Find out where to place i
        j = 0
        data_value_indexes = []
        
        for bin_by_inst, bin_by_obs in bin_by_inst_obs:
            data_value = kp[bin_by_inst][bin_by_obs][i]
            # Ignore if NaN or out of range
            if math.isnan(data_value) or data_value < mins[j] or data_value > maxs[j]:
                bad_val = True
                continue
            dv = math.floor((data_value - mins[j]) / binsize[j])
            data_value_indexes.append(int(dv))
            j += 1
            
        if bad_val:
            continue

        # Calculate the mean/median/mode from the values in "output_list"
        data_value_indexes = tuple(data_value_indexes)
        if median:
            # Jenkins server uses old versions of numpy and scipy
            if unittest:
                median_array[data_value_indexes] = \
                    numpy.nanmedian(get_values_from_list(binned_list, data_value_indexes))
            else:

                median_array[data_value_indexes] = \
                    numpy.nanmedian(get_values_from_list(binned_list, data_value_indexes))
        if avg or std:
            average_array[data_value_indexes] = \
                numpy.nansum(get_values_from_list(binned_list, data_value_indexes)) / density_array[data_value_indexes]
        if std:
            squared_total = []
            for x in get_values_from_list(binned_list, data_value_indexes):
                squared_total.append((x - average_array[data_value_indexes]) * (x - average_array[data_value_indexes]))
            std_array[data_value_indexes] = numpy.sqrt((numpy.sum(squared_total) / density_array[data_value_indexes]))
            
    # RETURN MEDIAN/AVERAGE/STANDARD DEVIATION
    return_list = []
    if median:
        return_list.append(median_array)
        print('Returning binned Medians')
    if avg:
        return_list.append(average_array)
        print('Returning binned Averages')
    if std:
        return_list.append(std_array)
        print('Returning binned standard deviations')
    if density:
        return_list.append(density_array)
        print('Returning binned densities')

    # Print out a little cheat sheet so people know what is in the array they're getting
    print('Now returning binned data')
    dimension = 0
    for bin_by_inst, bin_by_obs in bin_by_inst_obs:
        print('Dimension ' + str(dimension) + ' is ' + bin_by_obs)
        print('    Range: [' + str(mins[dimension]) + ', ' + str(mins[dimension] + binsize[dimension]) +
              ', ... ' + str(mins[dimension] + (binsize[dimension] * (total_bins[dimension] - 2))) +
              ', ' + str(mins[dimension] + (binsize[dimension] * (total_bins[dimension] - 1))) + ']')
        dimension += 1

    return return_list
