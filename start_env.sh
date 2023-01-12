#!/bin/sh
. /local/env/envconda.sh

ENV=".env/"

if [ -d "$ENV" ];
then
    echo "$ENV conda environment already exists"
else
	bash env.sh
fi

conda activate $ENV
source /scratch/sdubois/Stage_M2/cactus-bin-v2.4.0/cactus_env/bin/activate