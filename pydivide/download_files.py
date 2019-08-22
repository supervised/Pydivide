# Copyright 2017 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pydivide

###############################################################################
#
# Download Files Section
#
###############################################################################

from . import download_files_utilities as utils
from .utilities import orbit_time
from dateutil.parser import parse

     
def download_files(filenames=None,
                   instruments=None, 
                   list_files=False,
                   level='l2', 
                   insitu=True, 
                   iuvs=False, 
                   new_files=False, 
                   start_date='2014-01-01', 
                   end_date='2020-01-01', 
                   update_prefs=False,
                   only_update_prefs=False, 
                   exclude_orbit_file=False,
                   local_dir=None,
                   unittest=False):
    """
    Parameters:
    filenames: str/list of str ['yyyy-mm-dd']
        List of dates to be downloaded (eg. ['2015-12-31']).
    instruments: str/list of str
        Instruments from which you want to download data.
    list_files: bool (True/False0
        If true, lists the files instead of downloading them.
    level: str
        Data level to download.
    insitu: bool (True/False)
        If true, specifies only insitu files.
    iuvs: bool (True/False)
        If true,
    new_files: bool (True/False)
        Checks downloaded files and only downloads those that haven't already been downloaded.
    start_date: str
        String that is the start date for downloading data (YYYY-MM-DD)
    end_date: str
        String that is the end date for downloading data (YYYY-MM-DD)
    update_prefs: bool (True/False)
        If true, updates where you want to store data locally
    only_update_prefs: bool (True/False)
        If true, *only* updates where to store dat alocally, doesn't download files.
    exclude_orbit_file: bool (True/False)
        If true, won't download the latest orbit tables.
    local_dir: str
        If indicated, specifies where to download files for a specific implementation of this function.
    downloadonly: bool (True/False)
        If True then files are downloaded only,
        if False then CDF files are also loaded into pytplot using cdf_to_tplot.
    prefix: str
        The tplot variable names will be given this prefix.
        By default, no prefix is added.
    suffix: str
        The tplot variable names will be given this suffix.
        By default, no suffix is added.
    get_support_data: bool
    Data with an attribute "VAR_TYPE" with a value of "support_data"
        will be loaded into tplot.  By default, only loads in data with a
        "VAR_TYPE" attribute of "data".
    """
    
    import os

    # Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day + 1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        
    if update_prefs or only_update_prefs:
        utils.set_root_data_dir()
        if only_update_prefs:
            return
    
    public = utils.get_access()
    if not public:
        utils.get_uname_and_password()

    if filenames is None:
        if insitu and iuvs:
            print("Can't request both INSITU and IUVS in one query.")
            return
        if not insitu and not iuvs:
            print("If not specifying filename(s) to download, Must specify either insitu=True or iuvs=True.")
            return
        
    if instruments is None:
        instruments = ['kp']
        if insitu:
            level = 'insitu'
        if iuvs:
            level = 'iuvs'
            
    for instrument in instruments:
        # Build the query to the website
        query_args = []
        query_args.append("instrument=" + instrument)
        query_args.append("level=" + level)
        if filenames is not None:
            query_args.append("file=" + filenames)
        query_args.append("start_date=" + start_date)
        query_args.append("end_date=" + end_date)
        if level == 'iuvs':
            query_args.append("file_extension=tab")
        if local_dir is None:
            mvn_root_data_dir = utils.get_root_data_dir()
        else:
            mvn_root_data_dir = local_dir
        
        data_dir = os.path.join(mvn_root_data_dir, 'maven', 'data', 'sci', instrument, level)
        
        query = '&'.join(query_args)
        
        s = utils.get_filenames(query, public)
        
        if not s:
            print("No files found for {}.".format(instrument))

        if s:
            s = str(s)
            s = s.split(',')
        
            if list_files:
                for f in s:
                    print(f)
                return
        
            if new_files:
                s = utils.get_new_files(s, data_dir, instrument, level)
                
            if not unittest:
                print("Your request will download a total of: " + str(len(s)) + " files for instrument " +
                      str(instrument))
                print('Would you like to proceed with the download? ')
                valid_response = False
                cancel = False
                while not valid_response:
                    response = (input('(y/n) >  '))
                    if response == 'y' or response == 'Y':
                        valid_response = True
                    elif response == 'n' or response == 'N':
                        print('Cancelled download. Returning...')
                        valid_response = True
                        cancel = True
                    else:
                        print('Invalid input.  Please answer with y or n.')

                if cancel:
                    continue

            if not exclude_orbit_file:
                print("Before downloading data files, checking for updated orbit # file from naif.jpl.nasa.gov")
                print("")
                utils.get_orbit_files()
        
            i = 0
            utils.display_progress(i, len(s))
            for f in s:
                i += 1
                full_path = utils.create_dir_if_needed(f, data_dir, level)
                utils.get_file_from_site(f, public, full_path)
                utils.display_progress(i, len(s))

    return
