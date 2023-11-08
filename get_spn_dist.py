##### script for getting the snp per individual 
##### modified for having the occurrence of snp per class of features (utr, CDS and exons)
from __future__ import print_function
import os, sys
from commands import getoutput

all_snps=sys.argv[1]####### files with snps in genic position
#syn=sys.argv[2] #### file with names and genotypesi
genic_snps=sys.argv[2]
outfile=sys.argv[3]


head=r"grep '#CHROM' "+all_snps
barcodes=getoutput(head).split('\t')[9:]
print(len(barcodes))
print('genotype\tTotal SNPs\tGenic\tgenes_tagged\tCDS\tIntron\tUTR', file=open('%s' % outfile, 'a'))
print(barcodes)
for i in barcodes:
	####all snps identified
	#name=d_syn[i.split('_')[1]]
	os.system('vcftools --vcf %s --indv %s --out prova --recode' % (all_snps,i))
	os.system('vcf-subset -e prova.recode.vcf > prova_alt_all.vcf')##### vcf files with only alternative allele
	total=getoutput(r'grep -v "#"' + ' prova_alt_all.vcf|sort|uniq|wc -l') ### total SNPs per genotype
	print('count all spns for %s' % i)
	###### use only genic snps
	print('start analyze genic snps for %s' % i)
	os.system('vcftools --vcf %s --indv %s --out prova_gene --recode' % (genic_snps, i))
	os.system('vcf-subset -e prova_gene.recode.vcf > prova_alt_gene.vcf')
	genic_snps_geno=getoutput(r'grep -v "#"'+ ' prova_alt_gene.vcf|sort|uniq|wc -l')
	genes_tagged=getoutput('intersectBed -wa -a genes.gff3 -b prova_alt_gene.vcf|sort|uniq|wc -l')
	cds=getoutput('grep CDS Pvulgaris_218_gene_exons.gff3| intersectBed -wa -a prova_alt_gene.vcf -b stdin|sort|uniq|wc -l')
	utr=getoutput('grep UTR Pvulgaris_218_gene_exons.gff3| intersectBed -wa -a prova_alt_gene.vcf -b stdin|sort|uniq|wc -l')
	print(genic_snps_geno,cds,utr)	
	intron=int(genic_snps_geno)-int(cds)-int(utr)
	print('%s done' % i)
	print(i, total, genic_snps_geno, genes_tagged, cds, intron, utr, sep='\t', file=open(outfile, 'a'))
	os.system('rm prova*')

