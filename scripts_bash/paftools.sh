#!/bin/bash
#SBATCH --job-name=PAFleGFA
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_paftools.log

. /local/env/envconda.sh

ENV=".env/"

if [ -d "$ENV" ];
then
    echo "$ENV conda environment already exists"
else
	bash env.sh
fi

conda activate $ENV

minimap2 -cx asm5 --cs $1 $2 $3 | sort -k6,6 -k8,8n | paftools.js call -f $1 - > out.vcf

conda deactivate