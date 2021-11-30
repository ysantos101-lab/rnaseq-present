library(pheatmap)
library(RColorBrewer)
library(viridis)


args = commandArgs(trailingOnly=TRUE)

num_classA <- as.numeric(args[1])
num_genes <- as.numeric(args[2])

data_raw = read.table("./_RNA_tmp/DEG_cpm.txt",header=TRUE)
#data_raw = read.table("./DEG_cpm_types.txt",header=TRUE)
#data_raw = read.table("./raw_table.txt",header=TRUE)

dim(data_raw)

#colors <- c(rep("steelblue",28),rep("red",67))
#colors <- c("blueviolet","blue","lightskyblue1","blanchedalmond","darksalmon","indianred3","firebrick1")

#pdf("heatmap.pdf")
png("./output/heatmap.png", width = 4, height = 4, units = 'in', res = 900)
#tiff("heatmap.tiff",width = 8,height=8, units = 'in', res = 900)

pheatmap(data_raw,color = colorRampPalette(c("blue","white","red"))(50),fontsize=(1.8),scale="row",treeheight_row = 8,treeheight_col=0,cluster_cols=FALSE,gaps_col=c(num_classA))
#pheatmap(data_raw,color = colorRampPalette(c("blue","white","red"))(20),breaks=c(.001,.002,.005,.01,.02,.03,.04,.05,.08,.1,.2,.5,1,1.5,2,3,4,5,7,9,11),fontsize=.8, scale="none",treeheight_row = 0,treeheight_col=0,cluster_cols=FALSE)
#pheatmap(data_raw,color = colorRampPalette(c("blue","white","red"))(15),breaks=c(0,.25,.5,.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5),fontsize=.8, scale="row",treeheight_row = 0,treeheight_col=0,cluster_cols=FALSE)





#pheatmap(data_raw,cluster_cols=FALSE,fontsize=4, scale = "row",  colour = colors )
#pheatmap(data_raw,cluster_cols=FALSE,fontsize=4, scale="row")

#pheatmap(data_raw,fontsize=4, scale="column",cluster_cols=FALSE)
#pheatmap(data_raw,fontsize=4, scale="row",cluster_cols=FALSE)





#pheatmap(data_raw,fontsize=2, color = c(rep("blue4",20),rep("cornflowerblue",20),"cornsilk",rep("coral1",20),rep("brown4",20)), scale="row",treeheight_row = 0,treeheight_col = 0,cluster_cols=FALSE)

#pheatmap(data_raw,fontsize=2, treeheight_row = 0,treeheight_col=0,cluster_cols=FALSE)

#pheatmap(data_raw,fontsize=2,treeheight_row = 0,treeheight_col=0,cluster_cols=FALSE)
#pheatmap(data_raw,fontsize=2, color = inferno(100), scale="row",treeheight_row = 0,treeheight_col = 0,cluster_cols=FALSE)
#pheatmap(data_raw,fontsize=1, color = viridis(11), scale="row",treeheight_row = 0,treeheight_col = 0,cluster_cols=FALSE)


#pheatmap(data_raw,show_colnames=FALSE, show_rownames=FALSE, fontsize=3, color = inferno(9),  scale="row",treeheight_row = 0,cluster_cols=FALSE)







dev.off()

#pheatmap(data_raw,fontsize=4,cluster_cols=FALSE)
#pheatmap(data_raw,fontsize=4, scale="row",fontsize_row=0.0000001,treeheight_row = 0)

#pheatmap(data_raw,fontsize=4)
#pheatmap(data_raw,fontsize=4, scale="column")



#pheatmap(data_raw,cluster_cols=FALSE,fontsize=4 )
#pheatmap(data_raw,cutree_cols=2,fontsize=4 )



