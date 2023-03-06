#!/bin/bash
#SBATCH --job-name=KEKtus
#SBATCH --cpus-per-task=8
#SBATCH --mem=80G
#SBATCH --output=LOG_cactus.log
#SBATCH --constraint avx2
#SBATCH --mail-user=siegfried.dubois@inria.fr
#SBATCH --mail-type=begin
#SBATCH --mail-type=fail
#SBATCH --mail-type=end

source /scratch/sdubois/Stage_M2/cactus-bin-v2.4.0/cactus_env/bin/activate

# $1 -> path to a txt file
# $2 -> output path and name (without extension)
# $3 -> identifier of reference inside txt file
# $4 -> a temp name
# $5 -> a config file

# destroy any .jobstore
[ -d ./jobstore_$4 ] && rm -r ./jobstore_$4

# creating GFA1 file (SV graph)
cactus-minigraph ./jobstore_$4 $1 $2.gfa --reference $3 --configFile $5

# creating paf map (assembly-to-graph alignments)
cactus-graphmap ./jobstore_$4 $1 $2.gfa $2.paf  --reference $3 --outputFasta $2.sv.gfa.fa.gz --configFile $5

# creating hal (cactus base alignment)
cactus-align ./jobstore_$4 $1 $2.paf $2.hal --pangenome --outGFA --outVG --reference $3 --configFile $5

# final step
cactus-graphmap-join ./jobstore_$4 --vg $2.vg --outDir ./$2 --outName $4 --reference $3 --gfa full clip filter --vcf full clip filter --configFile $5