from fileparsers import subsampling_rgfa, reconstruct_fasta


if __name__ == '__main__':
    # subsampling_rgfa('/udd/sidubois/Documents/Code/datas/rGFA/chr3_haplotypes_on_consensus.gfa','hapl_on_css_toy_graph.gfa', ['488', '489', '490', '491', '492', '493', '1465', '1323'])

    paths: list = [
        ['1', '2', '3', '4', '5', '6'],
        ['1', '2', '3', '8', '4', '5', '6'],
        ['1', '7', '3', '4', '6']
    ]

    reconstruct_fasta('hapl_on_css_toy_graph.gfa', 's3.fasta', paths, [
                      'SeqBt1', 'BtChar.1', 'BtChar.2'])
