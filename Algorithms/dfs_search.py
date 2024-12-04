def dfs_search(graph, node, visited, parent=None):
    """
    Realiza una búsqueda en profundidad en un grafo.

    Args:
        graph (dict): Grafo representado como un diccionario de listas de adyacencia.
                      {node: [neighbor1, neighbor2, ...]}.
        node (int): Nodo actual que se está visitando.
        visited (set): Conjunto de nodos visitados.
        parent (int, optional): Nodo padre del nodo actual en la DFS. Default: None.

    Returns:
        bool: True si no se detectan ciclos, False si se detecta un ciclo.
    """
    if node in visited:
        return False  # Se detectó un ciclo
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor != parent:  # Evitar retroceder al nodo padre
            if not dfs(graph, neighbor, visited, node):
                return False

    return True
