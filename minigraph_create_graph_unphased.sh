#!/bin/bash
#SBATCH --job-name=minigraph_create_graph_unphased
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_minigraph.log

. /local/env/envconda.sh

ENV=".env/"

if [ -d "$ENV" ];
then
    echo "$ENV conda environment already exists"
else
	bash env.sh
fi

conda activate .env/

minigraph -cxggs -t16 $1 $2 > $3

conda deactivate