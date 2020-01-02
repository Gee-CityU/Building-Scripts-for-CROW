#Description: output metainfo if a student is not opt out in a csv file
#How to run this script: python test.py --input_file1=data/input_roster.csv --output_file=data/new_roster.csv
#Purpose: create a new roster and add a column called "Opt-Out" with values 0 and 1 to indicate whether a student is opt out or not.

import argparse
import csv
import pandas
from pandas import DataFrame

# Define the way we retrive arguments sent to the script
parser = argparse.ArgumentParser(description='Create merged spreadsheet')
parser.add_argument('--input_file1', action='store',dest='input_file1',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()

def add_opt_out(filename):
	File1 = filename	
	Data1 = pandas.read_csv(File1)
	Data_Frame1 = pandas.DataFrame(Data1)
	Data_Frame1['Opt-Out'] = [1 if x == 'OPT OUT' else 0 for x in Data_Frame1['Name']]
	File_new = Data_Frame1
	return(File_new)
	
Result = add_opt_out(args.input_file1)
Result.to_csv(args.output_file, index = False)
print(Result)

