from Bio import Align


def node_aligner(node: str, nodes_to_align: list) -> list[float]:
    """Given a node and a list of nodes, compules all pairwise alignments and return their scores

    Args:
        node (str): _description_
        nodes_to_align (list): _description_

    Returns:
        list[float]: _description_
    """
    aligner = Align.PairwiseAligner()
    aligner.open_gap_score = -0.5
    aligner.extend_gap_score = -0.1
    aligner.target_end_gap_score = 0.0
    aligner.query_end_gap_score = 0.0

    return [aligner.align(node, query)[0].score for query in nodes_to_align]


print(node_aligner('ATTTTACG', [
      'AGGATC', 'TTTTTTTTTTTTTTTT', 'TACCCCCCCCCCGAT', 'GGGGACCCTTTT']))
