from __future__ import print_function
import sys, os, math
from commands import getoutput
###########################
genome=sys.argv[1]



bam_files=getoutput('ls *.bam').split('\n')
for i in bam_files:
	cmd='samtools index %s' % i
	print(cmd)
	os.system(cmd)

###########################################################################
##############
############## SNP calling and filtering subroutine
	print('starting snps calling')
	os.system('samtools mpileup -uDgf %s *.bam|bcftools view -vcg -d 0.1 - > KabxMex54_RILS_raw ' % genome)
