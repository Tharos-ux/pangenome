from BubbleGun.bfs import bfs
from BubbleGun.Graph import Graph

# STEP1 => BubbleGun BFS
if args.starting_nodes is not None:
            if args.bfs_len is not None:
                if args.output_neighborhood is not None:

                    logging.info("Reading Graph...")
                    graph = Graph(args.in_graph)

                    for n in args.starting_nodes:
                        logging.info(
                            "extracting neighborhood around node {}".format(n))
                        set_of_nodes = bfs(graph, n, args.bfs_len)
                        if not graph.compacted:
                            graph.write_graph(set_of_nodes=set_of_nodes,
                                              output_file=args.output_neighborhood, append=True, optional_info=True)
                        else:
                            graph.write_graph(set_of_nodes=set_of_nodes,
                                              output_file=args.output_neighborhood, append=True, optional_info=False)
                        logging.info("finished successfully...")
                else:
                    print("You need to give an output file name --output_neighborhood")
                    sys.exit()
            else:
                print("You did not give the neighborhood size")
                sys.exit(1)
        else:
            print("You did not give the starting node(s)")
        logging.info("Done...")

# STEP2 => path subsampling

"""
    
Récupérer la liste des noeuds, trouver les sous-chemins correspondant dans chaque W/P-line




"""