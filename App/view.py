import sys
import time
import App.logic as lg
from tabulate import tabulate



def new_logic():
    """
        Se crea una instancia del controlador
    """
    control = lg.new_logic()
    
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")


def load_data(control, archivo_usuarios, archivo_relaciones):
    """
    Carga los datos
    """
    
    try:
        lg.load_data(control, archivo_usuarios, archivo_relaciones)

        friends_graph = control['graph']
        
        user_types = friends_graph.user_types
        
        data_user_types = [
                ["Usuarios básicos", user_types.get('basic', 0)],
                ["Usuarios premium", user_types.get('premium', 0)]
            ]
            

        # Prepare data for tabulation
        data = [
            ["Número total de usuarios", friends_graph.total_users],
            ["Número total de conexiones", friends_graph.total_connections],
            ["Usuarios por tipo",tabulate(data_user_types, tablefmt="grid")],
            ["Número promedio de seguidores", f"{friends_graph.get_average_followers():.2f}"],
            ["Ciudad con más usuarios", f"{friends_graph.get_city_with_most_users()[0]} ({friends_graph.get_city_with_most_users()[1]} usuarios)"]
        ]

        # Print data using tabulate
        print(tabulate(data, headers=["Descripción", "Valor"], tablefmt="grid"))
        
    except Exception as e:
        print(f"An error occurred in the print: {e}")

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    print(lg.get_data(control, id))


def print_req_1(control, id_inicio, id_destino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    start_time = time.time()
    
    red = lg.req_1(control, id_inicio, id_destino)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Prepare data for tabulation
    network_data = [
        [user['id'], user['name'], user['type']]
        for user in red
    ]
    
    # Print execution time
    print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    
    # Print number of elements in the network
    print(f"Número de elementos en la red: {len(red)}")
    
    # Print network data using tabulate
    print(tabulate(network_data, headers=["Id", "Alias", "Tipo"], tablefmt="grid"))
    


def print_req_3(control, id):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    start_time = time.time()
    
    user = lg.req_3(control, id)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Print execution time
    print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    
    # Print the user with the most followers
    if user:
        user_data = [
            ["ID", user],
            ["Alias", control['graph'].node_data[user]['name']],
            ["Tipo", control['graph'].node_data[user]['type']],
            ["Seguidores", control['graph'].node_data[user]['followers']]
        ]
        print("Amigo con más seguidores: ")
        print(tabulate(user_data, headers=["Descripción", "Valor"], tablefmt="grid"))
    else:
        print(f"El usuario {id} no tiene amigos")



def print_req_4(control, user_a, user_b):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    try :
        
        start_time = time.time()
    
        amigos_en_comun = lg.req_4(control, user_a, user_b)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Print execution time
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        
        
        # Prepare data for tabulation
        amigos_data = [
        [user['id'], user['name'], user['type']]
        for user in amigos_en_comun
        ]
        
        # Print number of elements in the network
        if len(amigos_en_comun) > 0:
            print(f"Número de amigos en común: {len(amigos_en_comun)}")
            print(tabulate(amigos_data, headers=["Id", "Alias", "Tipo"], tablefmt="grid"))
        else:
            print("No hay amigos en común")
    
        
        
    except Exception as e:
        print(f"An error occurred in the print: {e}")
    
  


def print_req_5(control, id, n):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    
    try:
        start_time = time.time()
        
        amigos = lg.req_5(control, id, n)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Print execution time
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    
        # Prepare data for tabulation
        amigos_data = [
            [user['id'], user['name'], user['followers']]
            for user in amigos
        ]
        
        # Print network data using tabulate
        print(tabulate(amigos_data, headers=["Id", "Alias", 'Followers'], tablefmt="grid"))
        
    except Exception as e:
        print(f"An error occurred in the print: {e}")


def print_req_6(control, n_users):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    try:
        start_time = time.time()
        
        user, graph, is_tree = lg.req_6(control, n_users)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Print execution time
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")   
        
        
        # Prepare data for tabulation
        user_data = [
            [user_id, control['graph'].node_data[user_id]['name'], control['graph'].node_data[user_id]['followers']]
            for user_id in user
        ]
        
        # Print network data using tabulate
        print(tabulate(user_data, headers=["Id", "Alias", "Followers"], tablefmt="grid"))
        
        if is_tree:
            print("El subgrafo es un árbol")
            print(graph)
        else:
            print("El subgrafo no es un árbol")
    except Exception as e:
        print(f"An error occurred in the print: {e}")
        


def print_req_7(control, user_id):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    sub_red, graph = lg.req_7(control, user_id)

    # Prepare data for tabulation
    print(sub_red)



def print_req_8(control, center_coords, radius_km):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    map_ = lg.req_8(control, center_coords, radius_km)
    
    map_.save("map.html")



# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            load_data(control, "1", "1" )
        elif int(inputs) == 2:
            id_inicio = input("Ingrese el ID del usuario de inicio: ")
            id_destino = input("Ingrese el ID del usuario de destino: ")
            print_req_1(control, id_inicio, id_destino)

        elif int(inputs) == 3:
            print("Nothing here...")

        elif int(inputs) == 4:
            id_user = input("Ingrese el ID del usuario: ")
            print_req_3(control, id_user)

        elif int(inputs) == 5:
            user_a = input("Ingrese el ID del primer usuario: ")
            user_b = input("Ingrese el ID del segundo usuario: ")
            print_req_4(control, user_a, user_b)

        elif int(inputs) == 6:
            user_id = input("Ingrese el ID del usuario: ")
            n = int(input("Ingrese el número de amigos a mostrar: "))
            print_req_5(control, user_id, n)

        elif int(inputs) == 7:
            n_users = int(input("Ingrese el número de usuarios a mostrar: "))
            print_req_6(control, n_users)

        elif int(inputs) == 8:
            user_id = input("Ingrese el ID del usuario: ")
            print_req_7(control, user_id)

        elif int(inputs) == 9:
            latitud = float(input("Ingrese la latitud del centro: "))
            longitud = float(input("Ingrese la longitud del centro: "))
            coordenadas = (latitud, longitud)
            radio = float(input("Ingrese el radio en kilómetros: "))
            print_req_8(control, coordenadas, radio)
            
            
            

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
