#!/bin/bash
#SBATCH --job-name=KEKtus
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_cactus.log
#SBATCH --constraint avx2

source /scratch/sdubois/Stage_M2/cactus-bin-v2.4.0/cactus_env/bin/activate

# $1 -> path to a txt file
# $2 -> output path and name (without extension)
# $3 -> identifier of reference inside txt file
# $4 -> a temp name

# destroy any .jobstore
[ -d ./jobstore_$4 ] && rm -r ./jobstore_$4

# creating GFA1 file (SV graph)
cactus-minigraph ./jobstore_$4 $1 $2.gfa --reference $3

# creating paf map (assembly-to-graph alignments)
cactus-graphmap ./jobstore_$4 $1 $2.gfa $2.paf  --reference $3 --outputFasta $2.sv.gfa.fa.gz

# creating hal (cactus base alignment)
cactus-align ./jobstore_$4 $1 $2.paf $2.hal --pangenome --outGFA --outVG --reference $3 

# final step
cactus-graphmap-join ./jobstore_$4 --vg $2.vg --outDir ./$2 --outName $4 --reference $3 --gfa

# --vcf --giraffe
# $1 must be a txt file from the format 
# Diploid sample:
# HG002.1  ./HG002.paternal.fa
# HG002.2  ./HG002.maternal.fa
# Haploid sample:
# CHM13  ./chm13.fa
# $3 is CHM13 for instance