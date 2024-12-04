from collections import defaultdict, Counter

class FriendsGraph:
    def __init__(self):
        self.graph = defaultdict(list)  # Diccionario de adyacencia
        self.node_data = {}  # Datos de los usuarios (USER_ID -> Información del usuario)
        self.relationship_data = {}  # Datos de las relaciones (FOLLOWER_ID, FOLLOWED_ID) -> START_DATE
        
        # Métricas a calcular en tiempo real
        self.total_users = 0  # Número total de usuarios
        self.total_connections = 0  # Número total de conexiones
        self.user_types = Counter()  # Contador de tipos de usuario (basic, premium)
        self.city_counts = Counter()  # Contador de usuarios por ciudad
        self.followers_count = defaultdict(int)  # Cantidad de seguidores por usuario

    def add_user(self, user_id, user_info):
        """Agrega un nodo al grafo con su información asociada."""
        if user_id not in self.node_data:  # Asegurarse de no duplicar usuarios
            self.node_data[user_id] = user_info
            self.total_users += 1  # Incrementar el número de usuarios
            self.user_types[user_info["type"]] += 1  # Incrementar el contador del tipo de usuario
            self.city_counts[user_info["city"]] += 1  # Incrementar el contador de la ciudad

    def add_relationship(self, follower_id, followed_id, start_date):
        """Agrega una relación dirigida al grafo."""
        if followed_id not in self.graph[follower_id]:  # Evitar duplicados
            self.graph[follower_id].append(followed_id)
            self.relationship_data[(follower_id, followed_id)] = start_date
            self.total_connections += 1  # Incrementar el número total de conexiones
            self.followers_count[followed_id] += 1  # Incrementar el contador de seguidores del seguido

    def get_average_followers(self):
        """Calcula el número promedio de seguidores por usuario."""
        if self.total_users == 0:
            return 0
        total_followers = sum(self.followers_count.values())
        return total_followers / self.total_users

    def get_city_with_most_users(self):
        """Devuelve la ciudad con más usuarios."""
        if not self.city_counts:
            return None
        return self.city_counts.most_common(1)[0]  # Devuelve (ciudad, número de usuarios)
    
    def get_top_n_users(self, n):
        """
        Encuentra los N usuarios más populares (con más seguidores).
        Args:
            n (int): Número de usuarios más populares a buscar.
        Returns:
            list: Lista de IDs de los N usuarios más populares.
        """
        # Ordenar usuarios por número de seguidores en orden descendente
        sorted_users = sorted(self.node_data.items(), key=lambda x: x[1]['followers'], reverse=True)
        return [user_id for user_id, _ in sorted_users[:n]]
    
    def get_subgraph(self, nodes):
        """
        Retorna el subgrafo dirigido formado por un conjunto de nodos dados.

        Args:
            nodes (set): Conjunto de nodos (USER_IDs) para construir el subgrafo.

        Returns:
            dict: Diccionario de adyacencia del subgrafo dirigido.
        """
        subgraph = defaultdict(list)
        nodes_set = set(nodes)  # Para verificar si un nodo pertenece al subgrafo rápidamente

        for node in nodes:
            if node in self.graph:  # Si el nodo tiene vecinos
                # Agregar solo las relaciones dirigidas hacia los nodos en el conjunto
                subgraph[node] = [neighbor for neighbor in self.graph[node] if neighbor in nodes_set]
        
        return subgraph

    def __repr__(self):
        """Representa el grafo mostrando las relaciones de seguimiento."""
        return str({node: self.graph[node] for node in self.graph})
