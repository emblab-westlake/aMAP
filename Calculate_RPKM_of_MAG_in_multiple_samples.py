# -*- coding: utf-8 -*-
"""
Created on Sun Nov  26 11:43:51 2023

@author: Xinyu
"""


###input of filepath
filepath_of_bin = 
filepath_of_depth =
output_folder_path = 
###input of txt(including sample name and all sequencing reads number)
Sample_info = 

###get the sample info and sequencing results reads number of each sample
samples = []
seq_dir = {}
f = open(Sample_info)
for line in f:
    sample = line.split('\t')[0]
    samples.append(sample)
    seq_dir[sample] = float(line.split('\t')[1])
f.close()
###get MAG length
MAGs = []
import os
filepath = filepath_of_bin
Bin_list = list(os.listdir(filePath))
for i in Bin_list:
    MAGs.append(str(i).replace(".fa", ""))
MAGs = set(MAGs)

MAG_length_dir = {}
for MAG in MAGs:
    MAG_length = 0
    f = open(filepath_of_bin + '/' + MAG + '.fa')
    for line in f:
        if '>' in line:
            contig_length = float(line.split('_')[6])
            MAG_length += contig_length
    f.close()
    MAG_length_dir[MAG] = float(MAG_length)
###make result dir
sample_bin = {}
for sample in samples:
    sample_bin[sample] = {}
    for MAG in MAGs:
        sample_bin[sample][MAG] = 0
###in each count mapped Nt then calu RPKM
for sample in samples:
    bin_mapped_Num_dir = {}
    for MAG in MAGs:
        bin_mapped_Num_dir[MAG] = 0
    f = open(filepath_of_depth + '/' + sample +'.depth.txt')
    for line in f:
        MAG = line.split('_NODE')[0]
        mapped_Nt = float(line.split('\t')[2])
        bin_mapped_Num_dir[MAG] += mapped_Nt
    f.close()
    for MAG in MAGs:
        sample_bin[sample][MAG] = bin_mapped_Num_dir[MAG]*1000*1000000/150/MAG_length_dir[MAG]/float(seq_dir[sample])
    print(sample + ' have been calculated')
###write result
r = open(output_folder_path + '/Bin_abundance_in_each_sample_RPKM.txt','w')
r.write('\t')
for sample in samples:
    r.write(sample+'\t')
r.write('\n')
for MAG in MAGs:
    r.write(MAG + '\t')
    for sample in samples:
        r.write(str(sample_bin[sample][MAG])+'\t')
    r.write('\n')
r.close()



