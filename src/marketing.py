import os
import sqlite3
from datetime import date,datetime
from prettytable import PrettyTable
import ast
    
def registrar_nuevos_clientes(cursor, conexion):

    print("\n> Introducir datos del cliente:")
    
    DNI = input("\t- DNI : ")
    while len(DNI) != 9:
        DNI = input(f">> Error. Vuelva a introducir el DNI: ")

    nombre = input("\t- Nombre: ").title()
    apellido1 = input("\t- Primer apellido: ").title()
    apellido2 = input("\t- Segundo apellido: ").title()
    
    while True:
        fecha = input("\t- Fecha de nacimiento (dd-mm-yyyy): ") #TODO: Formato de la feha, cuidado con fehas posteriores a hoy
        try:
            fecha_nacimiento = datetime.strptime(fecha, "%d-%m-%Y").date()
            break

        except ValueError:
            print("\n>>  Formato incorrecto. Por favor ingresa la fecha en formato dd-mm-yyyy.")
        

    # Mostrar los datos que se cargarán
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n> Datos a registrar del cliente:")
    print(f"\t- DNI: {DNI}")
    print(f"\t- Nombre completo: {nombre} {apellido1} {apellido2}")
    print(f"\t- Fecha de nacimiento: {fecha_nacimiento}")

    # Confirmar el registro
    confirmacion = input("¿Desea confirmar el registro? (sí/no): ").lower()
    if confirmacion not in ['sí', 'si', 'yes', 'y', 's']:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Registro cancelado.")
        return
    
    # Coger la fecha automatica
    fecha_alta_cliente = datetime.now()
    fecha_alta_cliente = fecha_alta_cliente.strftime("%Y-%m-%d")
    
    # Inserción en la base de datos
    query = "INSERT INTO Cliente (DNI, nombre, apellido1, apellido2, fecha_nacimiento, fecha_alta_cliente)  VALUES (?,?,?,?,?,?)"
    try:
        cursor.execute(query, (DNI, nombre, apellido1, apellido2, fecha_nacimiento, fecha_alta_cliente))
        conexion.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Cliente registrado con éxito.")
    except sqlite3.IntegrityError as e:
        # Aquí controlamos la excepción y mostramos el mensaje
        if "UNIQUE constraint failed" in str(e):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n>> Error: Ya existe un cliente registrado con el DNI '{DNI}'.")
        else:
            print(f"\n>> Error en la base de datos: {e}")


def visualizar_compras_clientes(cursor):

    DNI = input("Introducir DNI del cliente: ")
    while len(DNI) != 9:
        DNI = input(f">> Error. Vuelva a introducir el DNI: ")

    query = "SELECT * FROM Compra WHERE id_cliente = ?"
    cursor.execute(query, (DNI,))
    registros = cursor.fetchall()

    if registros:
        # Crear una tabla usando PrettyTable
        tabla = PrettyTable()
        tabla.field_names = ["ID Compra", "Fecha", "Productos", "Precio Total (€)"]

        total_precio = 0  # Variable para almacenar la suma total de los precios

        # Añadir cada registro a la tabla
        for registro in registros:
            tabla.add_row([registro[0], registro[2], registro[3], f"{registro[4]:.2f}"])
            total_precio += registro[4]  # Acumular el precio total


        tabla.add_row(["","","",""])
        tabla.add_row(["","","Total",f"{total_precio:.2f}"])

        # Imprimir la tabla
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nRegistro de compras para el cliente con DNI {DNI}:")
        print(tabla)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontraron compras para el cliente con DNI {DNI}.")
    return


def total_ventas_tienda_mes(cursor):
    id_tienda = input("\nIntroducir el ID de la tienda: ")

    while not id_tienda.isdigit():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Error: Debe ingresar un número válido para el ID de la tienda.")
        id_tienda = input("\nIntroducir el ID de la tienda: ")
    id_tienda = int(id_tienda)

    query_tienda = "SELECT nombre FROM Tienda WHERE id_tienda = ?"
    cursor.execute(query_tienda, (id_tienda,))
    nombre_tienda = cursor.fetchone()

    if nombre_tienda is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontró la tienda con ID '{id_tienda}'.")
        return
    else:
        nombre_tienda = nombre_tienda[0] 

    query_poblacion = "SELECT poblacion FROM Tienda WHERE id_tienda = ?"
    cursor.execute(query_poblacion, (id_tienda,))
    poblacion_tienda = cursor.fetchone()

    if poblacion_tienda is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontró la población de la tienda con ID '{id_tienda}'.")
        return
    else:
        poblacion_tienda = poblacion_tienda[0]

    # Query para obtener las ventas de los últimos 30 días de la tienda seleccionada
    query_ventas = """
    SELECT productos, cantidad_vendida 
    FROM Venta 
    WHERE id_tienda = ? 
    AND fecha >= date('now', '-30 days')
    """
    cursor.execute(query_ventas, (id_tienda,))
    ventas = cursor.fetchall()

    total_ventas = 0


    for venta in ventas:
        cantidad_vendida = venta[1]  
        # Separar las cantidades y convertirlas en una lista de enteros
        cantidades = list(map(int, cantidad_vendida.split(',')))
        total_ventas += sum(cantidades)

    os.system('cls' if os.name == 'nt' else 'clear')

    # Mostrar la información
    print("\n>> Información de la tienda:")
    print(f"\t- ID de la tienda: {id_tienda}")
    print(f"\t- Nombre de la tienda: {nombre_tienda}")
    print(f"\t- Población: {poblacion_tienda}")
    print(f"\t- Total de ventas del último mes: {total_ventas} unidades")

    return
