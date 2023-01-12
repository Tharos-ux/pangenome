#!/bin/bash
#SBATCH --job-name=minigraph_create_graph_phased
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_cactus.log

source /scratch/sdubois/Stage_M2/cactus-bin-v2.4.0/cactus_env/bin/activate

# $1 -> path to a txt file
# $2 -> output path and name (without extension)
# $3 -> identifier of reference inside txt file


# creating GFA1 file (SV graph)
cactus-minigraph ./jobstore $1 $2.gfa --reference $3

# creating paf map (assembly-to-graph alignments)
cactus-graphmap ./jobstore $1 $2.gfa $2.paf  --reference $3 --outputFasta $2.sv.gfa.fa.gz

# creating hal (cactus base alignment)
cactus-align ./jobstore $1 $2.paf $2.hal --pangenome --outVG --reference $3 

# $1 must be a txt file from the format 
# Diploid sample:
# HG002.1  ./HG002.paternal.fa
# HG002.2  ./HG002.maternal.fa
# Haploid sample:
# CHM13  ./chm13.fa
# $3 is CHM13 for instance