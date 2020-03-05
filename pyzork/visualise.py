def visualise_world(world : "World", filepath=None):
    """Allows you to generate a visualisation of the world where the locations are nodes and each
    exit is an edge.
    
    Parameters
    -----------
    world : World
        The world to represent
    filepath : Optional[str]
        Optional filepath to save the image to, if none is provided the world will be shown on an 
        interactive display.
    """
    #TODO: Edge label
    #TODO: Node shape and size
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("Make sure that networkx and matplotlib are installed to use this part of the library")
    
    G = nx.DiGraph()
    G.add_nodes_from([x.name for x in world.locations])

    for location in world.locations:
        for direction, exit in location.exits.items():
            if exit is not None:
                G.add_edge(location.name, exit.name)
                
    nx.draw(G, with_labels=True, font_weight='bold')
    
    if filepath:
        plt.savefig(filepath)
    else:
        plt.show()
        
    plt.clf()
