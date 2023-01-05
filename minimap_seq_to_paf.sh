#!/bin/bash
#SBATCH --job-name=minimap_seq_to_paf
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_minimap.log

minimap="/scratch/sdubois/Stage_M2/minimap2/minimap2"

$minimap -x asm5 $1 $2 > $3
