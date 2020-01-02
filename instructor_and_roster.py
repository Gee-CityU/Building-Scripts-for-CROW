#Description: output metainfo if a student is not opt out in a csv file
#How to run this script: python test.py --input_file1=data/input_instructor.csv --input_file2=data/input_registrar.csv --output_file=data/merged_file.csv
#Purpose: merge the instructor file and the registar file based on CRN to add registrar info to the instructor file. 

import argparse
import csv
import pandas
from pandas import DataFrame

# Define the way we retrive arguments sent to the script
parser = argparse.ArgumentParser(description='Create merged spreadsheet')
parser.add_argument('--input_file1', action='store',dest='input_file1',default='')
parser.add_argument('--input_file2',action='store',dest='input_file2',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()


def merge_files(filename1, filename2):
	File1 = filename1
	File2 = filename2
	Data1 = pandas.read_csv(File1)
	Data2 = pandas.read_csv(File2)
	Data_Frame1 = pandas.DataFrame(Data1)
	Data_Frame2 = pandas.DataFrame(Data2)

	#Merged_File = pandas.merge(Data_Frame1, Data_Frame2, on='CRN', how='outer')
	Merged_File = pandas.merge(Data_Frame1, Data_Frame2, on='CRN', how='inner')
	
	return(Merged_File)

Result = merge_files(args.input_file1, args.input_file2)
Result.to_csv(args.output_file, index = False)
	
print('Check the output below:')
print(Result)

# Recycle
#Filtered_Info = Data_Frame.loc[Data_Frame['Opt Out'] == 0,]


