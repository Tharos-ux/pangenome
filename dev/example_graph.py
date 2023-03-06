"Affiche un graphe animé"
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import subplots
from networkx import MultiDiGraph, draw_networkx_edges, draw_networkx_nodes, draw_networkx_labels, fruchterman_reingold_layout
from gfagraphs import Graph


gfa_file: str = '/udd/sidubois/Documents/Code/pangraphs/toy_examples/cactus.gfa'
gfa_ver: str = 'GFA1.1'

# définition du graphe
graph: MultiDiGraph = (pGraph := Graph(
    gfa_file, gfa_ver, False)).compute_networkx()


idx_weights = [3, 2, 1]

fig, ax = subplots(figsize=(10, 10))
# ax.set_xlim((-0.5, 5.5))
# ax.set_ylim((-1.2, 3.2))

# positions pour les noeuds
pos = fruchterman_reingold_layout(graph)

walk = [walk for walk in pGraph.walks if walk.datas['name'] == 'SeqBt1'][0]

nodes_to_highlight = [n for n, _ in walk.datas['path']]


def update(num):
    """Fonction de mise à jour du graphe.
    Y définir les propriétés d'affichage par défaut,
    ainsi que celles des éléments à mettre en valeur

    Args:
        num (int): tick actuel
    """
    ax.clear()  # nettoie les axes de la figure en cours
    ax.axis('off')
    path: list = nodes_to_highlight[:num+1]  # chemin à mettre en valeur

    # formatage par défaut
    draw_networkx_edges(graph, pos=pos, ax=ax, edge_color="gray")
    null_nodes = draw_networkx_nodes(graph, pos=pos, nodelist=set(
        graph.nodes()) - set(path), node_color='#d9b6e3',  ax=ax)
    null_nodes.set_edgecolor("black")

    # formatage des noeuds et arêtes en évidence
    query_nodes = draw_networkx_nodes(
        graph, pos=pos, nodelist=path, node_color="red", ax=ax)
    query_nodes.set_edgecolor("white")
    draw_networkx_labels(graph, pos=pos, labels=dict(
        zip(path, path)),  font_color="white", ax=ax)
    edgelist = [path[k:k+2] for k in range(len(path) - 1)]
    draw_networkx_edges(graph, pos=pos, edgelist=edgelist, width=2, ax=ax)


# Définir l'animation
speed: int = 1  # nombre de secondes avant la prochaine itération
anim = FuncAnimation(
    fig, update, frames=len(nodes_to_highlight), interval=speed*1000, repeat=True)
anim.save('animation.gif', writer='imagemagick', fps=speed)
