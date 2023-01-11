#!/bin/bash
#SBATCH --job-name=minigraph_create_graph_phased
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_cactus.log

. /local/env/envconda.sh

ENV=".env/"

if [ -d "$ENV" ];
then
    echo "$ENV conda environment already exists"
else
	bash env.sh
fi

cactus-minigraph ./jobstore $1 $2 --reference --mapCores 8

# $1 must be a txt file from the format 
# Diploid sample:
#HG002.1  ./HG002.paternal.fa
#HG002.2  ./HG002.maternal.fa
# Haploid sample:
#CHM13  ./chm13.fa