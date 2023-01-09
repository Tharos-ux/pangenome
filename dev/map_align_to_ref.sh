#!/bin/bash
#SBATCH --job-name=minimap_seq_to_paf
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_align.log
# Commandes pour identifier les correspondances entre, par exemple, les scaffolds de l'assemblage consensus et l'assemblage de référence

# assemblage ARS-UCD1.2_Btau5.0.1Y.fa = génome A
# requête assemblage seqoccin.Bt.v1.0.fasta = génome B
# cf https://github.com/lh3/minimap2/blob/master/cookbook.md#genome-aln

# Commande pour identifier, en première approximation, les correspondances
# alignmaxlen est un dictionnaire avec pour clefs "sca1-sca2" où sca1 est un scaffold du génome B et sca2 un scaffold du génome A
# et pour valeur le plus long alignement entre les deux scaffolds sca1 et sca2
cut -f 1,6,11 $1 | grep -v NKL | \
                                  awk '{ key=$1"-"$2; if ( $3 > alignmaxlen[key]){ alignmaxlen[key]=$3}}
                                       END{ for (key in alignmaxlen) { split(key,a,"-"); print a[1]"\t"a[2]"\t"alignmaxlen[key]}}' | \
                                  sort -k 1 > unphased_paf_corres_maxalnlen.txt
# on se limite aux alignements d'au moins 400kb
cat unphased_paf_corres_maxalnlen.txt awk '$3>4000000' | sort -k 2,2V > correspondances.txt