import os
import sqlite3
import Extra
from datetime import date

def mostrar_inventario_por_tienda(cursor):
    # Selección de la tienda
    id_tienda = input("\nIntroducir el ID de la tienda: ")

    while not id_tienda.isdigit():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Error: Debe ingresar un número válido para el ID de la tienda.")
        id_tienda = input("\nIntroducir el ID de la tienda: ")
    id_tienda = int(id_tienda)

    # Verificar si la tienda existe
    query_tienda = "SELECT nombre FROM Tienda WHERE id_tienda = ?"
    cursor.execute(query_tienda, (id_tienda,))
    nombre_tienda = cursor.fetchone()

    if nombre_tienda == None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontró la tienda con ID '{id_tienda}'.")
        return
    else:
        nombre_tienda = nombre_tienda[0]  # seleccionar solo el nombre

    # Consulta para obtener el nombre del producto y el nivel de inventario de esa tienda
    query_productos = """
    SELECT nombre_producto, cantidad
    FROM Producto
    WHERE id_tienda = ?
    """
    
    cursor.execute(query_productos, (id_tienda,))
    productos = cursor.fetchall()

    # Verificar si se encontraron productos
    if productos:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> Inventario de productos para '{nombre_tienda}':")
        for producto in productos:
            nombre_producto, cantidad = producto
            print(f"\t- Producto: {nombre_producto}, Cantidad en inventario: {cantidad}")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontraron productos para '{nombre_tienda}'.")


def registrar_producto_inventario(cursor, conexion):
    # Selección de la tienda
    id_tienda = input("\nIntroducir el ID de la tienda: ")

    while not id_tienda.isdigit():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Error: Debe ingresar un número válido para el ID de la tienda.")
        id_tienda = input("\nIntroducir el ID de la tienda: ")
    id_tienda = int(id_tienda)

    query_productos = """SELECT nombre FROM Tienda WHERE id_tienda = ?"""    
    cursor.execute(query_productos, (id_tienda,))
    nombre_tienda = cursor.fetchone()   

    if nombre_tienda == None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontró la tienda con ID '{id_tienda}'.")
        return
    else:
        tienda = nombre_tienda[0]  # seleccionar solo el nombre

    print(f"\n> Tienda Seleccionada: {tienda}")

    nombre_producto = input("\nIntroducir el nombre del producto: ").strip().title()
    categoria = input(f"Introducir categoría a la que pertenece '{nombre_producto}': ").strip().title()

    fecha_alta = None
    while fecha_alta is None:
        fecha = input("Introducir la fecha de alta en formato dd-mm-yyyy: ")
        fecha_alta = Extra.comprueba_fechas(fecha)
        if fecha_alta == date.today():
            continue
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n>> La fecha introducida ({fecha_alta}) no coincide con la fecha actual ({date.today()}).")
            return

    cantidad = int(input("Introducir la cantidad de producto adquirida: "))

    precio = int(input("Introducir el precio del producto: "))

    query = "INSERT INTO Producto (id_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio) VALUES (?,?,?,?,?,?)"

    cursor.execute(query, (id_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio))
    conexion.commit()

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n> Pedido registrado con éxito")   
    print(f"\t- Tienda: {nombre_tienda[0]} \n\t- Producto: {nombre_producto} \n\t- Categoría: {categoria} \n\t- Fecha: {fecha_alta} \n\t- Cantidad: {cantidad} unidades \n\t- Precio: {precio} €")  # Cambio aquí
    return

def registrar_venta_en_tienda(cursor, conexion):
    # Selección de la tienda
    id_tienda = input("\nIntroducir el ID de la tienda: ")

    while not id_tienda.isdigit():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Error: Debe ingresar un número válido para el ID de la tienda.")
        id_tienda = input("\nIntroducir el ID de la tienda: ")
    id_tienda = int(id_tienda)

    # Se verifica si la tienda existe
    query_tienda = "SELECT nombre FROM Tienda WHERE id_tienda = ?"
    cursor.execute(query_tienda, (id_tienda,))
    nombre_tienda = cursor.fetchone()

    if nombre_tienda is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n>> No se encontró la tienda con ID '{id_tienda}'.")
        return
    else:
        nombre_tienda = nombre_tienda[0]  # seleccionar solo el nombre

    # print(f"\n> Tienda Seleccionada: {nombre_tienda}")

    # Mostramos los productos disponibles en la tienda
    query_productos_disponibles = """
    SELECT nombre_producto, cantidad
    FROM Producto
    WHERE id_tienda = ?
    """
    cursor.execute(query_productos_disponibles, (id_tienda,))
    productos = cursor.fetchall()

    if not productos:
        print(f"\n>> No hay productos disponibles en la tienda '{nombre_tienda}'.")
        return

    # print(f"\nProductos disponibles en la tienda {nombre_tienda}:")
    # for producto, cantidad in productos:
    #     print(f" - {producto}: {cantidad} unidades")

    # Variables que acumularán productos y cantidades vendidas
    productos_vendidos = []
    cantidades_vendidas = []
    fecha_venta = date.today()  # Asumimos que todas las ventas se realizan en la misma fecha(hoy)

    # Bucle de ventas
    precio_total = 0.0
    while True:
        print(f"\n> Tienda Seleccionada: {nombre_tienda}")
        print(f"\nProductos disponibles en la tienda {nombre_tienda}:")
        for producto, cantidad in productos:
            print(f" - {producto}: {cantidad} unidades")


        nombre_producto = input("\nIntroducir el nombre del producto (o '0' para salir): ").strip().title()

        if nombre_producto == '0':
            if not productos_vendidos:
                print("\n>> No se registraron ventas. Saliendo...")
            else:
                print("\n>> Registro completado. Registrando todas las ventas...")
            break

        # Obtenemos la cantidad actual del producto en la tienda
        query_cantidad_producto = """
        SELECT cantidad, precio
        FROM Producto
        WHERE id_tienda = ? AND nombre_producto = ?
        """
        cursor.execute(query_cantidad_producto, (id_tienda, nombre_producto))
        resultado = cursor.fetchone()

        if resultado is None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n>> No se encontró el producto '{nombre_producto}' en la tienda '{nombre_tienda}'.")
            continue  # Se vuelve a pedir el nombre del evento
        else:
            cantidad_disponible = resultado[0]
            precio = resultado[1]


        # Se verifica que la cantidad vendida sea un número válido
        while True:
            try:
                cantidad_vendida = int(input(f"Introducir cantidad vendida de '{nombre_producto}' (disponible: {cantidad_disponible}) o '0' para salir: ").strip())
                if cantidad_vendida == 0:
                    print("\n>> Operación cancelada para este producto. Volviendo al menú principal.")
                    break  # Rompe y vuelve a preguntar por el producto
                elif cantidad_vendida < 0:
                    print("\n>> La cantidad debe ser un número positivo.")
                elif cantidad_vendida > cantidad_disponible:
                    print(f"\n>> No hay suficiente inventario de '{nombre_producto}' para vender {cantidad_vendida} unidades. Disponibles: {cantidad_disponible}.")
                else:
                    # Registramos el producto y cantidad para la venta
                    precio_total += cantidad_vendida*precio

                    productos_vendidos.append(nombre_producto)
                    cantidades_vendidas.append(cantidad_vendida)
                    # Actualizamos el inventario del producto
                    nueva_cantidad = cantidad_disponible - cantidad_vendida
                    query_update_producto = """
                    UPDATE Producto
                    SET cantidad = ?
                    WHERE id_tienda = ? AND nombre_producto = ?
                    """
                    cursor.execute(query_update_producto, (nueva_cantidad, id_tienda, nombre_producto))
                    conexion.commit()

                    os.system('cls' if os.name == 'nt' else 'clear')   
                    print(f"\n>> '{nombre_producto}' registrado con éxito. Cantidad vendida: {cantidad_vendida}.")
                    break
            except ValueError:
                print("\n>> Por favor, introduzca un número válido.")

    if productos_vendidos:
        productos_str = ', '.join(productos_vendidos)
        cantidades_str = ', '.join(map(str, cantidades_vendidas))

        query_insert_venta = """
        INSERT INTO Venta (id_tienda, fecha, productos, cantidad_vendida)
        VALUES (?,?,?,?)
        """
        cursor.execute(query_insert_venta, (id_tienda, fecha_venta, productos_str, cantidades_str))
        conexion.commit()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n> Todas las ventas han sido registradas con éxito") 
        print(f"\t- Fecha: {fecha_venta}")  
        print(f"\t- Tienda: {nombre_tienda}")
        print(f"\t- Productos vendidos: {productos_str}")
        print(f"\t- Cantidades vendidas: {cantidades_str}")
        print(f"\t- Precio total: {precio_total:.2f}€")

    return




