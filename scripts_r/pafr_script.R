setwd("/udd/sidubois/Documents/Code/")


library(pafr)


paffile = read_paf("align_chr3.paf")
#paffile = as_paf(read.table("Consensus.ref.paf",fill=TRUE)[1:12])

head(paffile)

dotplot(paffile)

head(chrom_sizes(paffile))

# filter_secondary_alignments(paffile)

# plot_synteny(paffile)
