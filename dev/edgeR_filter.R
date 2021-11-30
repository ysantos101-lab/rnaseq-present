#!/usr/bin/env Rscript
library(limma)
library(edgeR)

args = commandArgs(trailingOnly=TRUE)



raw_data <- read.table("./_RNA_tmp/raw_table.txt", header = TRUE)

classA_num <- as.numeric(args[1])
classB_num <-  as.numeric(args[2])
total_num <- classA_num + classB_num+1

p_val <- as.numeric(args[3])

corr_method <- args[4]

group <- c(rep("B",classA_num),rep("A",classB_num))
#dim(raw_data)
d <- DGEList(counts = raw_data[,2:total_num], genes=raw_data["gene"], group=group)


keep <- filterByExpr(d, design=NULL, group=group, lib.size=NULL)
d <- d[keep,]
#dim(d)

d <- calcNormFactors(d)

#d <- calcNormFactors(d, method = "TMM")

#d <- calcNormFactors(d)


#d <- estimateDisp(d)

d <- estimateCommonDisp(d)
d <- estimateTagwiseDisp(d)




design <- model.matrix(~0+group, data=d$samples)
colnames(design) <- levels(d$samples$group)


fit <- glmQLFit(d, design)
qlf <- glmQLFTest(fit, contrast=c(-1,1))
#out <- topTags(qlf, sort.by="logFC", adjust.method="bonferroni", p.value=.01, n=100)
out <- topTags(qlf, adjust.method=corr_method, p.value=p_val, n=9900)
#out <- topTags(qlf, sort.by="logFC", adjust.method="bonferroni", p.value=.01, n=100000)
out

#x <- png("./_RNA_tmp/volcano.png")
#print(out$table$F)
#volcanoData <- cbind(out$table$logFC, -log10(out$table$PValue))
#colnames(volcanoData) <- c("logFC", "Negative Log P-Val")
png("./output/volcano.png",width = 3, height = 3, units = 'in', res = 300)
x <- plot(x=out$table$logFC,y=-log10(out$table$PValue))

dev.off()


