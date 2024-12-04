from collections import deque

def bfs_find_path(graph, start, target):
    """
    Encuentra el camino más corto entre dos nodos en un grafo no ponderado,
    guardando los IDs de los usuarios que conforman la red.
    
    Args:
        graph (dict): Grafo representado como lista de adyacencia.
        start (int): Nodo inicial (ID de usuario).
        target (int): Nodo destino (ID de usuario).
    
    Returns:
        list: Camino más corto como lista de IDs de usuarios, o None si no hay camino.
    """
    if start == target:
        return [start]
    
    visited = set()  # Conjunto de nodos ya visitados
    queue = deque([(start, [start])])  # Cola: (nodo_actual, camino_hasta_ese_nodo)
    
    while queue:
        current_node, path = queue.popleft()  # Nodo actual y camino hasta él
        
        if current_node in visited:
            continue  # Saltar si ya fue visitado
        
        visited.add(current_node)
        
        # Explorar los vecinos del nodo actual
        for neighbor in graph[current_node]:
            if neighbor == target:
                return path + [neighbor]  # Retornar camino completo si se alcanza el destino
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))  # Agregar vecino y camino actualizado
    
    return None  # Retornar None si no hay camino entre start y target
