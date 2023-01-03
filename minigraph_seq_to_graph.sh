#!/bin/bash
#SBATCH --job-name=minigraph_seq_to_graph
#SBATCH --cpus-per-task=8
#SBATCH --mem=50G
#SBATCH --output=LOG_minigraph.log

minigraph="/scratch/sdubois/Stage_M2/minigraph/minigraph"

minigraph -cx $1 $2 > $3
