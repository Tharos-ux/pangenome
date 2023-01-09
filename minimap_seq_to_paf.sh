#!/bin/bash
#SBATCH --job-name=minimap_seq_to_paf
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_minimap.log

. /local/env/envconda.sh

ENV=".env/"

if [ -d "$ENV" ];
then
    echo "$ENV conda environment already exists"
else
	bash env.sh
fi

conda activate .env/

minimap2 -x asm5 $1 $2 > $3

conda deactivate