#!/usr/bin/env python
#source=open('./all_cpm.txt','r')
#source=open('tmm_out.txt','r')
source=open('./_RNA_tmp/all_cpm.txt','r')


#geneFile=open('./list_DEGs.txt','r')
geneFile=open('./_RNA_tmp/list_DEGs.txt','r')
#geneFile=open('./glm_res.txt','r')
#geneFile=open('./50_each_DEGs.txt','r')
gene_list=[]
toss=geneFile.readline();toss=geneFile.readline()
for line in geneFile:
	data=line.split()
	gene_list.append(data[1].strip().replace('"',''))
	if len(data)<3:
		break

geneFile.close()
print('num genes in DEG cpm: ' + str(len(gene_list)))
res=open('./_RNA_tmp/DEG_cpm.txt','w')

res.write(source.readline())

for line in source:
	data=line.strip().split('\t')
	if data[0] in gene_list:
		#res.write(line.replace('-','_'))
		res.write(line)



source.close()
res.close()

