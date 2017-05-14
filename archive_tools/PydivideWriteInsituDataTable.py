import pandas as pd
import re,os
from subprocess import call

variable_names =['',
                 '',
                 'ELECTRON_DENSITY',
                'ELECTRON_DENSITY_QUAL_MIN',
                'ELECTRON_DENSITY_QUAL_MAX',
                'ELECTRON_TEMPERATURE',
                'ELECTRON_TEMPERATURE_QUAL_MIN',
                'ELECTRON_TEMPERATURE_QUAL_MAX',
                'SPACECRAFT_POTENTIAL',
                'SPACECRAFT_POTENTIAL_QUAL_MIN',
                'SPACECRAFT_POTENTIAL_QUAL_MAX',
                'EWAVE_LOW_FREQ',
                'EWAVE_LOW_FREQ_QUAL_QUAL',
                'EWAVE_MID_FREQ',
                'EWAVE_MID_FREQ_QUAL_QUAL',
                'EWAVE_HIGH_FREQ',
                'EWAVE_HIGH_FREQ_QUAL_QUAL',
                'IRRADIANCE_LOW',
                'IRRADIANCE_LOW_QUAL',
                'IRRADIANCE_MID',
                'IRRADIANCE_MID_QUAL',
                'IRRADIANCE_LYMAN',
                'IRRADIANCE_LYMAN_QUAL',
                'SOLAR_WIND_ELECTRON_DENSITY',
                'SOLAR_WIND_ELECTRON_DENSITY_QUAL',
                'SOLAR_WIND_ELECTRON_TEMPERATURE',
                'SOLAR_WIND_ELECTRON_TEMPERATURE_QUAL',
                'ELECTRON_PARALLEL_FLUX_LOW',
                'ELECTRON_PARALLEL_FLUX_LOW_QUAL',
                'ELECTRON_PARALLEL_FLUX_MID',
                'ELECTRON_PARALLEL_FLUX_MID_QUAL',
                'ELECTRON_PARALLEL_FLUX_HIGH',
                'ELECTRON_PARALLEL_FLUX_HIGH_QUAL',
                'ELECTRON_ANTI_PARALLEL_FLUX_LOW',
                'ELECTRON_ANTI_PARALLEL_FLUX_LOW_QUAL',
                'ELECTRON_ANTI_PARALLEL_FLUX_MID',
                'ELECTRON_ANTI_PARALLEL_FLUX_MID_QUAL',
                'ELECTRON_ANTI_PARALLEL_FLUX_HIGH',
                'ELECTRON_ANTI_PARALLEL_FLUX_HIGH_QUAL',
                'ELECTRON_SPECTRUM_SHAPE_PARAMETER',
                'ELECTRON_SPECTRUM_SHAPE_PARAMETER_QUAL',
                'HPLUS_DENSITY',
                'HPLUS_DENSITY_QUAL',
                'HPLUS_FLOW_VELOCITY_MSO_X',
                'HPLUS_FLOW_VELOCITY_MSO_X_QUAL',
                'HPLUS_FLOW_VELOCITY_MSO_Y',
                'HPLUS_FLOW_VELOCITY_MSO_Y_QUAL',
                'HPLUS_FLOW_VELOCITY_MSO_Z',
                'HPLUS_FLOW_VELOCITY_MSO_Z_QUAL',
                'HPLUS_TEMPERATURE',
                'HPLUS_TEMPERATURE_QUAL',
                'SOLAR_WIND_DYNAMIC_PRESSURE',
                'SOLAR_WIND_DYNAMIC_PRESSURE_QUAL',
                'STATIC_QUALITY_FLAG',
                'HPLUS_DENSITY',
                'HPLUS_DENSITY_QUAL',
                'OPLUS_DENSITY',
                'OPLUS_DENSITY_QUAL',
                'O2PLUS_DENSITY',
                'O2PLUS_DENSITY_QUAL',
                'HPLUS_TEMPERATURE',
                'HPLUS_TEMPERATURE_QUAL',
                'OPLUS_TEMPERATURE',
                'OPLUS_TEMPERATURE_QUAL',
                'O2PLUS_TEMPERATURE',
                'O2PLUS_TEMPERATURE_QUAL',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_X',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_X_QUAL',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Y_QUAL',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z',
                'O2PLUS_FLOW_VELOCITY_MAVEN_APP_Z_QUAL',
                'O2PLUS_FLOW_VELOCITY_MSO_X',
                'O2PLUS_FLOW_VELOCITY_MSO_X_QUAL',
                'O2PLUS_FLOW_VELOCITY_MSO_Y',
                'O2PLUS_FLOW_VELOCITY_MSO_Y_QUAL',
                'O2PLUS_FLOW_VELOCITY_MSO_Z',
                'O2PLUS_FLOW_VELOCITY_MSO_Z_QUAL',
                'HPLUS_OMNI_DIRECTIONAL_FLUX',
                'HPLUS_CHARACTERISTIC_ENERGY',
                'HPLUS_CHARACTERISTIC_ENERGY_QUAL',
                'HEPLUS_OMNI_DIRECTIONAL_FLUX',
                'HEPLUS_CHARACTERISTIC_ENERGY',
                'HEPLUS_CHARACTERISTIC_ENERGY_QUAL',
                'OPLUS_OMNI_DIRECTIONAL_FLUX',
                'OPLUS_CHARACTERISTIC_ENERGY',
                'OPLUS_CHARACTERISTIC_ENERGY_QUAL',
                'O2PLUS_OMNI_DIRECTIONAL_FLUX',
                'O2PLUS_CHARACTERISTIC_ENERGY',
                'O2PLUS_CHARACTERISTIC_ENERGY_QUAL',
                'HPLUS_CHARACTERISTIC_DIRECTION_MSO_X',
                'HPLUS_CHARACTERISTIC_DIRECTION_MSO_Y',
                'HPLUS_CHARACTERISTIC_DIRECTION_MSO_Z',
                'HPLUS_CHARACTERISTIC_ANGULAR_WIDTH',
                'HPLUS_CHARACTERISTIC_ANGULAR_WIDTH_QUAL',
                'DOMINANT_PICKUP_ION_CHARACTERISTIC _DIRECTION_MSO_X',
                'DOMINANT_PICKUP_ION_CHARACTERISTIC _DIRECTION_MSO_Y',
                'DOMINANT_PICKUP_ION_CHARACTERISTIC _DIRECTION_MSO_Z',
                'DOMINANT_PICKUP_ION_CHARACTERISTIC _ANGULAR_WIDTH',
                'DOMINANT_PICKUP_ION_CHARACTERISTIC _ANGULAR_WIDTH_QUAL',
                'ION_ENERGY_FLUX__FOV_1_F',
                'ION_ENERGY_FLUX__FOV_1_F_QUAL',
                'ION_ENERGY_FLUX__FOV_1_R',
                'ION_ENERGY_FLUX__FOV_1_R_QUAL',
                'ION_ENERGY_FLUX__FOV_2_F',
                'ION_ENERGY_FLUX__FOV_2_F_QUAL',
                'ION_ENERGY_FLUX__FOV_2_R',
                'ION_ENERGY_FLUX__FOV_2_R_QUAL',
                'ELECTRON_ENERGY_FLUX___FOV_1_F',
                'ELECTRON_ENERGY_FLUX___FOV_1_F_QUAL',
                'ELECTRON_ENERGY_FLUX___FOV_1_R',
                'ELECTRON_ENERGY_FLUX___FOV_1_R_QUAL',
                'ELECTRON_ENERGY_FLUX___FOV_2_F',
                'ELECTRON_ENERGY_FLUX___FOV_2_F_QUAL',
                'ELECTRON_ENERGY_FLUX___FOV_2_R',
                'ELECTRON_ENERGY_FLUX___FOV_2_R_QUAL',
                'LOOK_DIRECTION_1_F_MSO_X',
                'LOOK_DIRECTION_1_F_MSO_Y',
                'LOOK_DIRECTION_1_F_MSO_Z',
                'LOOK_DIRECTION_1_R_MSO_X',
                'LOOK_DIRECTION_1_R_MSO_Y',
                'LOOK_DIRECTION_1_R_MSO_Z',
                'LOOK_DIRECTION_2_F_MSO_X',
                'LOOK_DIRECTION_2_F_MSO_Y',
                'LOOK_DIRECTION_2_F_MSO_Z',
                'LOOK_DIRECTION_2_R_MSO_X',
                'LOOK_DIRECTION_2_R_MSO_Y',
                'LOOK_DIRECTION_2_R_MSO_Z',
                'MSO_X',
                'MSO_X_QUAL',
                'MSO_Y',
                'MSO_Y_QUAL',
                'MSO_Z',
                'MSO_Z_QUAL',
                'GEO_X',
                'GEO_X_QUAL',
                'GEO_Y',
                'GEO_Y_QUAL',
                'GEO_Z',
                'GEO_Z_QUAL',
                'RMS_DEVIATION',
                'RMS_DEVIATION_QUAL',
                'HE_DENSITY',
                'HE_DENSITY_PRECISION',
                'HE_DENSITY_QUAL',
                'O_DENSITY',
                'O_DENSITY_PRECISION',
                'O_DENSITY_QUAL',
                'CO_DENSITY',
                'CO_DENSITY_PRECISION',
                'CO_DENSITY_QUAL',
                'N2_DENSITY',
                'N2_DENSITY_PRECISION',
                'N2_DENSITY_QUAL',
                'NO_DENSITY',
                'NO_DENSITY_PRECISION',
                'NO_DENSITY_QUAL',
                'AR_DENSITY',
                'AR_DENSITY_PRECISION',
                'AR_DENSITY_QUAL',
                'CO2_DENSITY',
                'CO2_DENSITY_PRECISION',
                'CO2_DENSITY_QUAL',
                'O2PLUS_DENSITY',
                'O2PLUS_DENSITY_PRECISION',
                'O2PLUS_DENSITY_QUAL',
                'CO2PLUS_DENSITY',
                'CO2PLUS_DENSITY_PRECISION',
                'CO2PLUS_DENSITY_QUAL',
                'NOPLUS_DENSITY',
                'NOPLUS_DENSITY_PRECISION',
                'NOPLUS_DENSITY_QUAL',
                'OPLUS_DENSITY',
                'OPLUS_DENSITY_PRECISION',
                'OPLUS_DENSITY_QUAL',
                'CO2PLUS_N2PLUS_DENSITY',
                'CO2PLUS_N2PLUS_DENSITY_PRECISION',
                'CO2PLUS_N2PLUS_DENSITY_QUAL',
                'CPLUS_DENSITY',
                'CPLUS_DENSITY_PRECISION',
                'CPLUS_DENSITY_QUAL',
                'OHPLUS_DENSITY',
                'OHPLUS_DENSITY_PRECISION',
                'OHPLUS_DENSITY_QUAL',
                'NPLUS_DENSITY',
                'NPLUS_DENSITY_PRECISION',
                'NPLUS_DENSITY_QUAL',
                'ATTITUDE_GEO_X',
                'ATTITUDE_GEO_Y',
                'ATTITUDE_GEO_Z',
                'ATTITUDE_MSO_X',
                'ATTITUDE_MSO_Y',
                'ATTITUDE_MSO_Z',
                'SUB_SC_LONGITUDE',
                'SUB_SC_LATITUDE',
                'SZA',
                'LOCAL_TIME',
                'ALTITUDE',
                'GEO_X',
                'GEO_Y',
                'GEO_Z',
                'MSO_X',
                'MSO_Y',
                'MSO_Z',
                'ATTITUDE_GEO_X',
                'ATTITUDE_GEO_Y',
                'ATTITUDE_GEO_Z',
                'ATTITUDE_MSO_X',
                'ATTITUDE_MSO_Y',
                'ATTITUDE_MSO_Z',
                '_',
                '_',
                'MARS_SEASON',
                'MARS_SUN_DISTANCE',
                'SUBSOLAR_POINT_GEO_LONGITUDE',
                'SUBSOLAR_POINT_GEO_LATITUDE',
                'SUBMARS_POINT_SOLAR_LONGITUDE',
                'SUBMARS_POINT_SOLAR_LATITUDE',
                'T11',
                'T12',
                'T13',
                'T21',
                'T22',
                'T23',
                'T31',
                'T32',
                'T33',
                'SPACECRAFT_T11',
                'SPACECRAFT_T12',
                'SPACECRAFT_T13',
                'SPACECRAFT_T21',
                'SPACECRAFT_T22',
                'SPACECRAFT_T23',
                'SPACECRAFT_T31',
                'SPACECRAFT_T32',
                'SPACECRAFT_T33']




#
# Sample data file to use for accessing header info
#
froot = 'C:/Maven Data/maven/data/sci/kp/insitu/2015/05/'
fname = froot + 'mvn_kp_insitu_20150514_v09_r01.tab'
#
# Count the number of lines in the header
#
print("Reading sample file for header information...")
nheader = 0
for line in open(fname):
    if line.startswith('#'):
        nheader = nheader+1
#
# Read the header and create a DataFrame of the column header information
#
fin=open(fname)
#
#  Cycle through lines of header
#
for iline in range(nheader):
    line = fin.readline()
    #
    # Get number of columns of data stated in header
    #
    if re.search('Number of parameter columns',line):
        ncol = int(re.split("\s{3}",line)[1])
    #
    # Get the labels of the columns in the Column description section
    #
    elif re.search('PARAMETER',line):
        ParamListStartLine = iline
        ColStart = []
        ColEnd = []
        test = re.split('^#\s|\s{2,}',line)
        #
        # Get the column numbers for start and end of fields
        #
        for i in test[1:-1]:
            #
            # Yes, this is confusing; but we are starting from the 2nd
            #   entry, so we assume the start column of 1, and the start
            #   of the 2nd entry indicates the end of that column.
            #
            start = re.search(i,line).start()
            ColStart.append(start)
            if test.index(i) > 1:
                ColEnd.append(start)
            if test.index(i) == len(test[1:-1]):
                ColEnd.append(len(line))
#
#  Use the column field information to build colspecs argument for read_fwf
#
ColSpecs = []
for i,j in zip(ColStart,ColEnd):
    ColSpecs.append([i,j])
fin.close()
#
#  Read the table as a fixed width field table
#
#test = pd.read_fwf(fname,
#                   skiprows=range(ParamListStartLine)+[ParamListStartLine+1],
#                   colspecs=ColSpecs,header=0,nrows=ncol)

test = pd.read_fwf(fname,
                   skiprows=ParamListStartLine,
                   colspecs=ColSpecs,header=0,nrows=ncol+1)
#
#  Define filenames for creating LaTeX table from fwf
#
test.insert(0, 'VARIABLE', variable_names)
test = test.drop('FORMAT', 1)
tempname = 'C:/temp/temp.tex'
foutname = 'C:/temp/kp_data_insitu_info_table.tex'
fout = open(tempname,'w')
TableCols = ['VARIABLE', 'INSTRUMENT','PARAMETER','UNITS','NOTES']
HeaderLine = ' & '.join(TableCols) + '\\\\'
#
# Write LaTeX preamble
#
print("Writing LaTeX table...")
fout.write('\\documentclass[6pt]{article}\n')
fout.write('\\usepackage{booktabs}\n')
fout.write('\\usepackage{longtable}\n')
fout.write('\\usepackage{amssymb, amsmath, graphicx}\n')
fout.write('\\usepackage{rotating}\n')
fout.write('\\usepackage{geometry}\n')
fout.write('\\geometry{letterpaper, landscape, margin=0.1in}\n')
fout.write('\n')
fout.write('\\begin{document}')
fout.write('\n')
#
# Write the replacement lines for converting to longtable
#
fout.write('\\begin{footnotesize}\n')
fout.write('\\begin{center}\n')
fout.write('\\begin{longtable}{|p{3in}|p{.8in}|p{2in}|p{.8in}|p{3in}|}\n')
fout.write('\\caption[MAVEN In-Situ Key Parameter Data Table]{MAVEN In-Situ Key Parameter Data Table}\\\\\n')
fout.write('\n')
fout.write('\\hline\n%s%%FirstHead\n\\hline\n\\endfirsthead\n\n' % HeaderLine)
fout.write('\\hline\n%s%%LaterHead\n\\hline\n\\endhead\n\n' % HeaderLine)
fout.write('\\hline\n \\multicolumn{%1d}{c}{\\textit{(Continued on next page)}}\\\\\n' % len(TableCols))
fout.write('\\endfoot\n\n')
fout.write('\\hline\\hline\n\\endlastfoot\n\n')
fout.write('%% End add lines to top\n')
fout.write('%% Also Remove \\end{tabular} and \\bottomrule from end of document\n\n')
#
# Use unlimited column width for producing table.  LaTeX will word-wrap for us
#
pd.set_option('max_colwidth', -1)
#
# Write table
#
fout.write( pd.DataFrame(test).to_latex( columns=TableCols,index=False,
                                         na_rep='',longtable=False ) )
#
# Re-set max_colwidth to default value
#
pd.reset_option('max_colwidth')
#
# Add \end blocks for longtable and center
#
fout.write('\\end{longtable}\n\\end{center}\n')
fout.write('\\end{footnotesize}\n')
fout.write('\end{document}')
fout.flush()
fout.close()
#
# Now, go back, open the written file and re-write corrections
# First, footnote information
#
print("Editing LaTeX table (adding footnotes, etc.)...")
Note1 = '\\footnotemark'
DoneNote1 = False
Text1 = '\\footnotetext{Instrument name is used to define substructures/dictionaries}\n'
Note2 = '\\footnote{EUV is here included as a separate instrument for naming purposes in the Tookit}'
DoneNote2 = False
Note3 = '\\footnote{Spacecraft substruct data contains ephemeris and geometry data within KP data files}'
DoneNote3 = False
Note4 = '\\footnote{APP orientation information is placed into its own substruct for visualization purposes}'
DoneNote4 = False
Note5 = '\\footnote{While these are spacecraft data, they are placed at base level struct/dict}'
DoneNote5 = False
#
#  Now, cycle through the lines of the file
#
fout = open(foutname,'w')
for line in open(tempname):
    # Remove the old tabular environment syntax
    if ( line.startswith('\\begin{tabular}') or 
         line.startswith('\\toprule') or 
         line.startswith('\\bottomrule') or
         line.startswith('\\midrule') or
         line.startswith('\\end{tabular}') ):
        fout.write('')
    elif 'INSTRUMENT' in line:
        # Add the Instrument name footnote (special case b/c in header)
        if 'FirstHead' in line and not DoneNote1:
            fout.write(line.replace('INSTRUMENT','INSTRUMENT'+Note1))
            DoneNote1 = True
        elif 'LaterHead' in line:
            fout.write(line)
        else:
            pass
    elif 'UTC/SCET' in line:
        # Also needed to write the instrument name footnote
        fout.write(Text1)
        fout.write(line)
    elif 'LPW-EUV' in line:
        # Change the LPW-EUV to EUV and add note
        if DoneNote2:
            fout.write(line.replace('LPW-EUV','EUV'))
        else:
            fout.write(line.replace('LPW-EUV','EUV'+Note2))
            DoneNote2 = True
    elif 'SPICE' in line:
        if 'APP' in line:
            # Change Articulating Platform instrument name from SPICE to APP
            if not DoneNote4:
                fout.write(line.replace('SPICE','APP'+Note4))
                DoneNote4 = True
            else:
                fout.write(line.replace('SPICE','APP'))
        elif 'Orbit Number' in line:
            # Add notes for Orbit number and IO_flag
            line = line.replace('SPICE','---'+Note5)
            fout.write(line)
        elif 'Inbound' in line:
            fout.write(line.replace('SPICE','---'+Note5))
        else:
            # Replace ASCII arrow with LaTeX arrows in coord transform entries
            if '->' in line:
                line = line.replace('->','$\\rightarrow$')
            if not DoneNote3:
                # Change SPICE to SPACECRAFT in all other SPICE entries
                fout.write(line.replace('SPICE','SPACECRAFT'+Note3,1))
                DoneNote3 = True
            else:
                fout.write(line.replace('SPICE','SPACECRAFT'))
    else:
        # If nothing changed, write the old line
        fout.write(line)
fout.flush()
fout.close()
#
# Now, Run LaTeX from here
#
#print("Generating LaTeX table...")
#call(["latex",foutname],stdout=open(os.devnull,'w'))
#print("Generating PDF-capable postscipt file...")
#call(["dvips", "-Ppdf", "-o", 
#      foutname.replace('tex','ps'), foutname.replace('tex','dvi')],
#      stdout=open(os.devnull,'w'),stderr=open(os.devnull,'w'))
#print("Generating PDF file of table...")
#call(["ps2pdf",foutname.replace('tex','ps')],stdout=open(os.devnull,'w'))
#print("Cleaning up....")
#call(["rm",tempname])
#for i in ['aux','dvi','log','ps','tex']:
#    call(["rm",foutname.replace('tex',i)])
