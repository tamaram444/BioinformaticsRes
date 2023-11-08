#! /usr/bin/env python
###### script for analyzing read number
###### reads already cleaned, just select the samples that has a read count >= x percentile of reads distribution
###### it's the second step of GBS pipeline
###### need a file containing the number of reads for each demultiplexed sample
###### its a wrapper for samtools and bwa so you need this program installed in your computer
###### needs in the same folder 

from __future__ import print_function
import os
import numpy as np
from commands import getoutput
from optparse import OptionParser


bam_files=getoutput('ls *_sort.bam').split('\n')
for i in bam_files:
        cmd='samtools index %s' % i
        print(cmd)
        os.system(cmd)

###snp calling
print('start snp calling')
os.system('samtools mpileup -uDgf %s *_sort.bam|bcftools view -vcg -d 0.3 - > all_snp_raw.vcf' % ref)
