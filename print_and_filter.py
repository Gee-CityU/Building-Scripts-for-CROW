#Description: output metainfo if a student is not opt out in a csv file
#How to run this script: python test.py --input_file = data/input.csv --output_file = data/output.csv

import argparse
import csv
import pandas
from pandas import DataFrame

# Define the way we retrive arguments sent to the script
parser = argparse.ArgumentParser(description='Create metadata spreadsheet')
parser.add_argument('--input_file', action='store',dest='input_file',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()

if args.input_file != '':
	File = args.input_file
	Data = pandas.read_csv(File)
	Data_Frame = pandas.DataFrame(Data)
	Filtered_Info = Data_Frame.loc[Data_Frame['Opt Out'] == 0,]
	Meta_Info = Filtered_Info[['Name','Subject','Course','TOEFL','Major']]
	Meta_Info.to_csv(args.output_file, index = False)
	print('check output below:')
	print(Meta_Info)
else:
	print('There is no input file.')



