#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np
import os

def convert_to_CPM(df,log,output):
	print ('Input file: {}'.format(os.path.basename(df)))
	cpm_df = {}
	df = pd.read_csv(df,sep='\s+').T
	print ('Converting values to CPM...')
	for rows in df.index:
		counts = df.loc[rows]
		total_counts_per_row = counts.sum()
		cpm = [(float(c)/total_counts_per_row)*1000000 for c in counts]
		cpm_df[rows] = cpm
	cpm_table = pd.DataFrame(cpm_df,columns=df.index,index=df.columns)
	if log:
		print ('Applying log2 transformation on CPM values.')
		cpm_table += 1 #adds 1 to every value as psuedo counts for log2 transformation
		cpm_table = cpm_table.applymap(np.log2)
	cpm_table.to_csv(output+'.txt',sep='\t')
	print ('Process completed. Output file {} created.'.format(output+'.txt'))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input',required=True,help="dataframe file to convert to CPM")
	parser.add_argument('-o','--output',type=str,required=True,help="output CPM file name")
	parser.add_argument('--log', action='store_true', help='apply log2 CPM')
	args = parser.parse_args()
	convert_to_CPM(df=args.input, log= args.log, output=args.output)
