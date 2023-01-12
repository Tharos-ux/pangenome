#!/bin/bash
#SBATCH --job-name=minigraph_create_graph_phased
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_cactus.log

source /scratch/sdubois/Stage_M2/cactus-bin-v2.4.0/cactus_env/bin/activate

cactus-minigraph ./jobstore $1 $2 --reference $3

# $1 must be a txt file from the format 
# Diploid sample:
#HG002.1  ./HG002.paternal.fa
#HG002.2  ./HG002.maternal.fa
# Haploid sample:
#CHM13  ./chm13.fa