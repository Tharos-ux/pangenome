#!/bin/bash
#SBATCH --job-name=parse_genomes
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G

. /local/env/envconda.sh
conda activate .env/

python fileparsers/parse_genomes.py data/seqoccin.Bt.Char.HiFi_HiC_1.fa data/Char_1.paf 3
# python fileparsers/parse_genomes.py data/seqoccin.Bt.Char.HiFi_HiC_2.fa data/Char_2.paf 3