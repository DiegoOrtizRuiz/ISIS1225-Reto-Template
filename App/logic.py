import ast
from collections import defaultdict
import time
import os
import csv
from datetime import datetime
import traceback
import DataStructures.friendsGraph as fg
import Algorithms.bsf_find_path as bfs
from collections import deque
from math import radians, sin, cos, sqrt, atan2
import folium



def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "graph": fg.FriendsGraph()
    }
    return catalog


# Funciones para la carga de datos



def replace_if_empty(value, default='Unknown'):
    return value if value else default

def load_data(catalog, filename_1, filename_2):
    user_data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/users_info_' + filename_1 + ".csv"
    relationships_data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/relationships_' + filename_2 + ".csv"
    
    users = csv.DictReader(open(user_data_dir), delimiter=';')
    relationships = csv.DictReader(open(relationships_data_dir), delimiter=';')
    
    try:
        for user in users:
            user_id = replace_if_empty(user['USER_ID'])
            user_info = {
                'id': user_id,
                'name': replace_if_empty(user['USER_NAME']),
                'type': replace_if_empty(user['USER_TYPE']),
                'age': replace_if_empty(user['AGE']),
                'join_date': datetime.strptime(replace_if_empty(user['JOIN_DATE'], '01/01/2000' ), '%d/%m/%Y'),
                'photo': replace_if_empty(user['PHOTO']),
                'hobbies': ast.literal_eval(replace_if_empty(user['HOBBIES'], '[]')),
                'city': replace_if_empty(user['CITY']),
                'location': (float(replace_if_empty(user["LATITUDE"], '0.0')), float(replace_if_empty(user["LONGITUDE"], '0.0'))),
                'followers': 0,
                'followed': 0,
                'followed_lista': [],
                'followers_lista': [],
                'amigos_lista': []
                
            }
            catalog["graph"].add_user(user_id, user_info)
        
        for relationship in relationships:
            follower_id = replace_if_empty(relationship['FOLLOWER_ID'])
            followed_id = replace_if_empty(relationship['FOLLOWED_ID'])
            start_date = datetime.strptime(replace_if_empty(relationship['START_DATE'], '2000-01-01').split()[0], '%Y-%m-%d')
            catalog["graph"].add_relationship(follower_id, followed_id, start_date)
            catalog['graph'].node_data[follower_id]['followed'] += 1
            catalog['graph'].node_data[followed_id]['followers'] += 1
            catalog['graph'].node_data[followed_id]['followers_lista'].append(follower_id)
            catalog['graph'].node_data[follower_id]['followed_lista'].append(followed_id)
            
            amigos_follower = set(catalog['graph'].node_data[follower_id]['followers_lista']).intersection(
                set(catalog['graph'].node_data[follower_id]['followed_lista'])
            )
            
            amigos_followed = set(catalog['graph'].node_data[followed_id]['followers_lista']).intersection(
                set(catalog['graph'].node_data[followed_id]['followed_lista'])
            )
            
            catalog['graph'].node_data[follower_id]['amigos_lista'] = list(set(catalog['graph'].node_data[follower_id]['amigos_lista']).union(amigos_follower))
            catalog['graph'].node_data[followed_id]['amigos_lista'] = list(set(catalog['graph'].node_data[followed_id]['amigos_lista']).union(amigos_followed))
            
                
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        
        
    

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    user_info = catalog["graph"].node_data[id]
    
    return user_info


def req_1(catalog, id_inicio, id_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    red = bfs.bfs_find_path(catalog["graph"].graph, id_inicio, id_destino)
    
    red_datos = []
    
    for usuario in red:
        red_datos.append(catalog["graph"].node_data[usuario])
        
    
    return red_datos


def req_3(catalog, id_user):
    """
    Retorna el resultado del requerimiento 3
    """
    amigos_user = catalog["graph"].node_data[id_user]['amigos_lista']
    
    
    max_followers = -1
    user_with_max_followers = None

    for amigo in amigos_user:
        num_followers = catalog["graph"].node_data[amigo]['followers']
        if num_followers > max_followers:
            max_followers = num_followers
            user_with_max_followers = amigo

    return user_with_max_followers




def req_4(catalog, user_a, user_b):
    """
    Retorna el resultado del requerimiento 4
    """
    amigos_user_a = catalog["graph"].node_data[user_a]['amigos_lista']
    amigos_user_b = catalog["graph"].node_data[user_b]['amigos_lista']
    
    print(amigos_user_a)
    print(amigos_user_b)
    
    amigos_comunes = list(set(amigos_user_a).intersection(set(amigos_user_b)))
    
    amigos_comunes_datos = []
    
    for amigo in amigos_comunes:
        amigos_comunes_datos.append(catalog["graph"].node_data[amigo])
        
    return amigos_comunes_datos


def req_5(catalog, id_user, n):
    """
    Retorna el resultado del requerimiento 5
    """
    amigos_user = catalog["graph"].node_data[id_user]['amigos_lista']
    
    n_amigos = []
    
    amigos_user_sorted = sorted(amigos_user, key=lambda x: catalog["graph"].node_data[x]['followers'], reverse=True)
    n_amigos = amigos_user_sorted[:n]
    
    n_amigos_datos = []
    for amigo in n_amigos:
        n_amigos_datos.append(catalog["graph"].node_data[amigo])
    
    return n_amigos_datos

def req_6(catalog, n_users):
    """
    Retorna el resultado del requerimiento 6
    """
    top_n_users = catalog['graph'].get_top_n_users(n_users)
    
    grafo = catalog['graph'].get_subgraph(top_n_users)
    
    es_arbol = is_tree(grafo)
    return top_n_users, grafo, es_arbol
    

def req_7(catalog,user_id):
    """
    Obtiene la sub-red de amigos (explícitos e implícitos) de un usuario basado en hobbies similares usando DFS.

    Args:
        graph (FriendsGraph): El grafo que contiene la red social.
        user_id (str): ID del usuario inicial.

    Returns:
        dict: Subgrafo dirigido que representa la sub-red.
        dict: Información adicional de cada amigo encontrado.
              Cada entrada tiene la forma {user_id: {'depth': nivel de profundidad, 'common_hobbies': [lista de hobbies en común]}}
    """
    
    graph = catalog['graph']
    
    if user_id not in graph.node_data:
        raise ValueError(f"El usuario {user_id} no existe en el grafo.")

    # Información del usuario inicial
    user_hobbies = set(graph.node_data[user_id]["hobbies"])

    # Subgrafo y estructura de información adicional
    subgraph = defaultdict(list)
    friends_info = {}

    def dfs(current_user, depth, visited):
        """
        Función recursiva para recorrer los amigos usando DFS.
        """
        visited.add(current_user)

        # Revisar cada amigo explícito del usuario actual
        for friend in graph.node_data[current_user]["amigos_lista"]:
            if friend not in visited:
                friend_hobbies = set(graph.node_data[friend]["hobbies"])
                common_hobbies = user_hobbies & friend_hobbies
                if common_hobbies:  # Si tienen hobbies en común
                    subgraph[current_user].append(friend)  # Agregar al subgrafo
                    friends_info[friend] = {
                        'depth': depth + 1,
                        'common_hobbies': list(common_hobbies)
                    }
                    # Llamada recursiva para los amigos de este amigo
                    dfs(friend, depth + 1, visited)

    # Llamada inicial a DFS
    visited = set()
    dfs(user_id, 0, visited)

    return dict(subgraph), friends_info



def req_8(catalog, center_coords, radius_km):
    """
    Retorna el resultado del requerimiento 8
    """
    visualize_users_in_radius(catalog['graph'], center_coords, radius_km)


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

#  Otras funciones



def is_tree(subgraph):
    """
    Verifica si un subgrafo dirigido es un árbol.

    Args:
        subgraph (dict): Diccionario de adyacencia que representa el subgrafo dirigido.

    Returns:
        bool: True si el subgrafo es un árbol, False en caso contrario.
    """
    def dfs(node, visited, stack):
        """Realiza un DFS para detectar ciclos y verificar conectividad."""
        if node in stack:  # Si el nodo está en el stack actual, hay un ciclo
            return False
        if node in visited:  # Nodo ya visitado
            return True
        
        visited.add(node)
        stack.add(node)
        
        for neighbor in subgraph.get(node, []):
            if not dfs(neighbor, visited, stack):
                return False
        
        stack.remove(node)
        return True

    # Condición 1: Debe haber exactamente un nodo raíz (nodo sin predecesores)
    in_degree = {node: 0 for node in subgraph}
    for node in subgraph:
        for neighbor in subgraph[node]:
            in_degree[neighbor] += 1
    
    roots = [node for node, degree in in_degree.items() if degree == 0]
    if len(roots) != 1:  # Si hay más de un nodo raíz o ninguno, no es un árbol
        return False

    # Condición 2: Realizar un DFS para verificar conectividad y aciclicidad
    root = roots[0]
    visited = set()
    stack = set()
    
    if not dfs(root, visited, stack):
        return False

    # Condición 3: Todos los nodos del subgrafo deben ser alcanzados desde el nodo raíz
    if len(visited) != len(subgraph):
        return False

    return True

def haversine(coord1, coord2):
    """
    Calcula la distancia en kilómetros entre dos coordenadas geográficas usando la fórmula de Haversine.
    Args:
        coord1 (tuple): Coordenada 1 (latitud, longitud).
        coord2 (tuple): Coordenada 2 (latitud, longitud).
    Returns:
        float: Distancia entre las coordenadas en kilómetros.
    """
    R = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def get_users_within_radius(graph, center_coords, radius_km):
    """
    Obtiene los usuarios dentro de un radio específico basado en coordenadas geográficas.
    Args:
        graph (FriendsGraph): Grafo que contiene la red social.
        center_coords (tuple): Coordenadas del centro (latitud, longitud).
        radius_km (float): Radio en kilómetros.
    Returns:
        dict: Subgrafo dirigido con usuarios dentro del radio.
        dict: Coordenadas de los usuarios seleccionados.
    """
    selected_users = {}
    for user_id, user_data in graph.node_data.items():
        user_coords = user_data["location"]
        distance = haversine(center_coords, user_coords)
        if distance <= radius_km:
            selected_users[user_id] = user_data

    # Crear subgrafo con los usuarios seleccionados
    subgraph = {}
    for user_id in selected_users:
        subgraph[user_id] = [
            friend for friend in graph.graph[user_id] if friend in selected_users
        ]

    return subgraph, {user_id: user_data["location"] for user_id, user_data in selected_users.items()}


def plot_graph_on_map(subgraph, user_locations, center_coords, radius_km):
    """
    Grafica un subgrafo en un mapa interactivo usando folium.
    Args:
        subgraph (dict): Subgrafo con las relaciones entre los usuarios.
        user_locations (dict): Coordenadas de los usuarios seleccionados.
        center_coords (tuple): Coordenadas del centro del área de interés.
        radius_km (float): Radio del área de interés.
    Returns:
        folium.Map: Mapa con los usuarios y relaciones.
    """
    # Crear un mapa centrado en las coordenadas dadas
    map_ = folium.Map(location=center_coords, zoom_start=13)

    # Agregar un círculo para representar el radio
    folium.Circle(
        location=center_coords,
        radius=radius_km * 1000,  # Convertir a metros
        color="blue",
        fill=True,
        fill_opacity=0.1,
    ).add_to(map_)

    # Agregar marcadores para cada usuario
    for user_id, coords in user_locations.items():
        folium.Marker(location=coords, popup=f"User ID: {user_id}").add_to(map_)

    # Agregar líneas para las relaciones entre usuarios
    for user_id, friends in subgraph.items():
        for friend_id in friends:
            folium.PolyLine(
                [user_locations[user_id], user_locations[friend_id]],
                color="green",
                weight=2,
                opacity=0.6,
            ).add_to(map_)

    return map_

def visualize_users_in_radius(graph, center_coords, radius_km):
    """
    Filtra usuarios dentro de un radio específico y grafica sus relaciones en un mapa.
    Args:
        graph (FriendsGraph): Grafo que contiene la red social.
        center_coords (tuple): Coordenadas del centro (latitud, longitud).
        radius_km (float): Radio en kilómetros.
    Returns:
        folium.Map: Mapa interactivo con usuarios y relaciones.
    """
    subgraph, user_locations = get_users_within_radius(graph, center_coords, radius_km)
    return plot_graph_on_map(subgraph, user_locations, center_coords, radius_km)

