import subprocess
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse
from collections import Counter


def make_my_table(classA_filenames,classB_filenames,classA_name,classB_name):



    subprocess.call("mkdir _RNA_tmp",shell=True)
    res=open('./_RNA_tmp/raw_table.txt','w')
    res.write('gene'+'\t')





    IDs=[]
    numClassA=0;numClassB=0;classA_IDs=[];classB_IDs=[]

    IDs.extend(classA_filenames)
    IDs.extend(classB_filenames)

    num_classA=len(classA_filenames)
    num_classB=len(classB_filenames)


    for val in classA_filenames:
        classA_IDs.append(val.split('/')[-1].replace('.txt',''))
    for val in classB_filenames:
        classB_IDs.append(val.split('/')[-1].replace('.txt',''))


    classA_cov=[]
    classB_cov=[]

            

    values=dict()
    gene_list=[]
    
    genes=dict()
    num_done=0

    first=True
    for filename in IDs:
        ID=filename.split('/')[-1].replace('.txt','')
        res.write('\t')
        res.write(ID)
        cur_file=open(filename,'r')
        numZero=0
        numNon=0
        toss=cur_file.readline()
        values[ID]=[]
        num_lines=0
        for line in cur_file:
            num_lines+=1
            data=line.strip().split()
            if first:
                gene_list.append(data[0])
            values[ID].append(data[1])
            if float(data[1])==0:
                numZero+=1
            else:
                numNon+=1
            if data[0] not in genes:
                genes[data[0]]=[]
            genes[data[0]].append(data[1])
        
        if num_lines<1000:
            print('FEWER than 1000 lines in: ' + ID)
        cur_file.close()
        num_done+=1
        first=False
        cov=float(numNon)/float(numNon+numZero)
        print('Coverage for '+ID+' is: '+'\t'+ str(cov))
        if ID in classA_IDs:
            classA_cov.append(cov)
        elif ID in classB_IDs:
            classB_cov.append(cov)
    
    res.write('\n')
    
    for gene in gene_list:
        res.write(gene)
        first=False
        #res.write(gene + '\t')
        for val in genes[gene]:
            res.write('\t'+val)
        res.write('\n')
    
    make_violin(classA_cov,classB_cov,classA_name,classB_name)
    
    res.close()


def make_violin(classA_cov,classB_cov,classA_name='classA',classB_name='classB'):

	if len(classA_name)<2:
		classA_name='classA'
	if len(classB_name)<2:
		classB_name='classB'

	fig1,ax1 = plt.subplots()
	ax1.set_title(classA_name+' Transcriptome Coverage')
	ax1.boxplot(classA_cov)
	#plt.show()

	subprocess.call("mkdir output",shell=True)
	plt.savefig('./output/classA_cov.png', figsize=(3,3), dpi=300)

	
	fig2,ax2=plt.subplots()
	ax2.set_title(classB_name+' Transcriptome Coverage')
	ax2.boxplot(classB_cov)
	plt.savefig('./output/classB_cov.png', figsize=(3,3), dpi=300)
	#plt.show()



	




