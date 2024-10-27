import os
import sqlite3
from datetime import date,datetime 

def registrar_tienda(cursor, conexion):
    # Pedir el nombre de la tienda hasta que no sea vacío
    nombre_tienda = ""
    while not nombre_tienda:
        nombre_tienda = input("Introducir el nombre de la tienda: ").strip().title()
        if not nombre_tienda:
            print("El nombre de la tienda no puede estar vacío. Inténtelo de nuevo.")

    # Pedir la población hasta que no sea vacía
    poblacion = ""
    while not poblacion:
        poblacion = input("Introducir la población: ").strip().title()
        if not poblacion:
            print("La población no puede estar vacía. Inténtelo de nuevo.")

    # La ubicación puede ser opcional
    ubicacion = input("Introducir la ubicación (dejar en blanco si no se conoce): ").strip().title()

    # Mostrar los datos que se cargarán
    print("\n>> Datos a registrar:")
    print(f"Nombre de la tienda: {nombre_tienda}")
    print(f"Población: {poblacion}")
    print(f"Ubicación: {'No especificada' if not ubicacion else ubicacion}")

    # Confirmar el registro
    confirmacion = input("¿Desea continuar con el registro? (sí/no): ").lower()
    if confirmacion not in ['sí', 'si', 'yes', 'y', 's']:  # Acepta varias formas de afirmación
        os.system('cls' if os.name == 'nt' else 'clear')
        print(">> Registro cancelado.")
        return

    # Inserción en la base de datos
    query = "INSERT INTO Tienda (nombre, poblacion, ubicacion) VALUES (?, ?, ?)"
    cursor.execute(query, (nombre_tienda, poblacion, ubicacion if ubicacion else None))
    conexion.commit()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n>> Tienda registrada con éxito.")


def informe_ventas(cursor):
    cursor.execute("SELECT id_tienda, nombre FROM Tienda")
    tiendas = cursor.fetchall()

    # Mostrar tiendas disponibles
    if not tiendas:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> No hay tiendas disponibles para mostrar informe.")
        return

    print("\nTiendas disponibles:")
    for tienda in tiendas:
        id_tienda, nombre = tienda
        print(f"{id_tienda}. {nombre}")
    
    # Elección de tienda
    while True:
        try:
            tienda_elegida_idx = int(input("\nElija el ID de tienda para ver el informe: "))
            if any(tienda[0] == tienda_elegida_idx for tienda in tiendas):
                tienda_elegida = tienda_elegida_idx
                break
            else:
                print("\n>> Error: Elección no válida. Inténtelo de nuevo")
        except ValueError:
            print("\n>> Error: Elección no válida. Inténtelo de nuevo")
    
    # Rango de fechas
    while True:
        fecha_inicio = input("\nIngrese la fecha de inicio (dd-mm-yyyy): ")
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
            if fecha_inicio > datetime.today().date():
                print("\n>> La fecha de inicio no puede ser posterior al día de hoy.")
            else:
                break
        except ValueError:
            print("\n>> Formato incorrecto. Por favor ingresa la fecha en formato dd-mm-yyyy.")
        
    while True:
        fecha_fin = input("Ingrese la fecha de fin (dd-mm-yyyy): ")
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y").date()
            if fecha_fin < fecha_inicio:
                print("\n>> La fecha de fin no puede ser anterior a la fecha de inicio.")
            else:
                break
        except ValueError:
            print("\n>> Formato incorrecto. Por favor ingresa la fecha en formato dd-mm-yyyy.")

    # Convertir las fechas a formato adecuado para SQLite
    fecha_inicio = fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin = fecha_fin.strftime('%Y-%m-%d')
    
    # Generar el informe de ventas
    cursor.execute("""
        SELECT V.fecha, V.productos, V.cantidad_vendida
        FROM Venta V
        WHERE V.id_tienda = ? AND V.fecha BETWEEN ? AND ?
        ORDER BY V.fecha ASC;
    """, (tienda_elegida, fecha_inicio, fecha_fin))
    
    ventas = cursor.fetchall()
    
    # Si no hay ventas en el rango de fechas
    if not ventas:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\nNo hay ventas registradas para la tienda '{tienda_elegida}' en el rango de fechas de {fecha_inicio} hasta {fecha_fin}")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    # Mostrar informe de ventas
    print("_"*70)
    print(f"\nINFORME de ventas para la tienda '{tienda_elegida}' desde {fecha_inicio} hasta {fecha_fin}:")
    print("_"*70)
    for venta in ventas:
        
        fecha = datetime.strptime(venta[0], '%Y-%m-%d').date()
        fecha = fecha.strftime('%d-%m-%Y')
        
        productos = venta[1].replace(" ", "").split(",")
        cantidades  = venta[2].replace(" ", "").split(",")
        cantidades_int = [int(num) for num in cantidades]
        
        print(f"\nVENTA EN LA FECHA: {fecha}")
        for i in range(len(productos)):
            print(f" - Producto: {productos[i]}, Cantidad: {cantidades_int[i]}")
    
    print("-"*50)
    print(f"\nTotal de ventas: {len(ventas)} ")
