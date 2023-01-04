#!/bin/bash
#SBATCH --job-name=minigraph_seq_to_graph
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_minigraph.log

minimap="/scratch/sdubois/Stage_M2/minimap2/minimap2"

$minimap -x asm5 $1 $2 > $3
