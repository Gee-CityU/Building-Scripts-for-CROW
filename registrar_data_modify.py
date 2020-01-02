# Purpose: combine two tabs in a registrar-data file, and then add the selected instructor info (the output file of instructor_info.py)
# To run this script in Anaconda: python registrar_data_modify.py --input_file1=summer2017_registrar.xlsx --input_file2=instructor_selected_info.csv --output_file=modified_registrar_data.xlsx

import argparse
import csv
import pandas
from pandas import DataFrame

#Define the arguments sent to the script
parser = argparse.ArgumentParser(description='Create merged spreadsheet')
parser.add_argument('--input_file1', action='store',dest='input_file1',default='')
parser.add_argument('--input_file2',action='store',dest='input_file2',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()

# Creat a function that can combine multiple tabs into one master tab in an excel file
def combine_tabs(filename):
	Combined = pandas.concat(pandas.read_excel(filename, sheet_name=None), axis=1, ignore_index=True)
	return(Combined)

# Combine the two tabs in summer2017_registrar.xlsx	
Combined_Registrar_Info = combine_tabs(args.input_file1)
#print(Combined_Registrar_Info)
#print(Combined_Registrar_Info[7]) # [7] is the CRN column


# Problem: the original headers are not output in the Combined_Registrar_Info, but some numerical indices like 0, 1, 2 are in the headers position
# Combined_Registrar_Info.to_excel(args.output_file, index = False)

# Create a function to build data frame
def build_data_frame (filename):
	File = filename
	Data = pandas.read_csv(File)
	Data_Frame = pandas.DataFrame(Data)
	return (Data_Frame)

# Create a data frame for the instructor selected info (the output file of instructor_info.py)
Instructor_Selected_Info = build_data_frame(args.input_file2)

# Build a two-dimension dictionary for the selected instructor info, see the example below
# for example {CRN1:{'semester':'fall2017','instructor_name': 'Lee Jordan', 'instructor code':'2001'},
#			  {CRN2:{'semester':'fall2018','instructor_name': 'Cody Chen', 'instructor code':'2002' ...}
Data_Dict = Instructor_Selected_Info.set_index('CRN').T.to_dict()

# for each item in the CRN column of summer2017_registrar.xlsx
for Item in Combined_Registrar_Info[7]:
	# if a CRN is in the two-dimension dictionary (built above), then assigne different info related to this CRN to different and new columns in the master sheet with the registrat info for summer 2017
	if Item in Data_Dict:
		Combined_Registrar_Info['Semester'] = [Data_Dict[Item]['Semester'] for Item in Combined_Registrar_Info[7]]
		Combined_Registrar_Info['Instructor_First_Name'] = [Data_Dict[Item]['Instructor_First_Name'] for Item in Combined_Registrar_Info[7]]
		Combined_Registrar_Info['Instructor_Last_Name'] = [Data_Dict[Item]['Instructor_Last_Name'] for Item in Combined_Registrar_Info[7]]
		Combined_Registrar_Info['Instructor_Code'] = [Data_Dict[Item]['Instructor_Code'] for Item in Combined_Registrar_Info[7]]
	# else add 'N/A' to the new columns but this is not supposed to happen.
	else:
		Combined_Registrar_Info['Semester'] = 'NA'
		Combined_Registrar_Info['Instructor_First_Name'] = 'NA'
		Combined_Registrar_Info['Instructor_Last_Name'] = 'NA'
		Combined_Registrar_Info['Instructor_Code'] = 'NA'

# Output the finalized registrar: student registar info with the selected instructor info 
# Problems: there are empty columns in the output file
#print(Combined_Registrar_Info)
Combined_Registrar_Info.to_excel(args.output_file, index = False)
