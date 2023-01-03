#!/bin/bash
#SBATCH --job-name=minigraph_create_graph
#SBATCH --cpus-per-task=8
#SBATCH --mem=50G
#SBATCH --output=LOG_minigraph.log

minigraph="/scratch/sdubois/Stage_M2/minigraph/minigraph"

minigraph -cxggs -t16 $1 $2 $3 > $4
