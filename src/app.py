from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa CORS
from database import get_db_connection, init_db
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Inicializar la base de datos
init_db()

@app.route('/api/tiendas', methods=['GET'])
def obtener_tiendas():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT nombre FROM Tienda"  # Consulta para obtener solo los nombres de las tiendas
    cursor.execute(query)
    tiendas = cursor.fetchall()  # Recupera todos los resultados de la consulta

    conn.close()

    # Formatear la respuesta como una lista de nombres
    lista_tiendas = [tienda[0] for tienda in tiendas]
    # Devolver la lista de tiendas como
    response = "<br>".join(lista_tiendas)
    return response, 200


@app.route('/api/inventory', methods=['GET'])
def mostrar_inventario_por_tienda():
    nombre_tienda = request.args.get('nombre_tienda')  # Cambiamos a 'nombre_tienda'

    # Validar el nombre de la tienda
    if not nombre_tienda:
        return jsonify({"error": "Nombre de tienda no proporcionado"}), 400  # Código 400 para indicar un mal input

    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para verificar si la tienda existe y obtener su ID
    query_tienda = "SELECT id_tienda FROM Tienda WHERE nombre = ?"
    cursor.execute(query_tienda, (nombre_tienda,))
    id_tienda = cursor.fetchone()

    if id_tienda is None:
        return jsonify({
                           "error": f"No se encontró la tienda con nombre '{nombre_tienda}'"}), 404  # Código 404 para indicar que no se encontró

    id_tienda = id_tienda[0]  # Obtener el ID de la tienda

    # Consulta para obtener los productos y sus cantidades
    query_productos = """
    SELECT nombre_producto, cantidad
    FROM Producto
    WHERE id_tienda = ?
    """
    cursor.execute(query_productos, (id_tienda,))
    productos = cursor.fetchall()  # Obtener todos los productos

    # Construir la respuesta
    inventario = [{"nombre_producto": producto[0], "cantidad": producto[1]} for producto in productos]

    return jsonify(
        {"tienda": nombre_tienda, "inventario": inventario})  # Devolver el nombre de la tienda y el inventario



@app.route('/api/registrar_producto', methods=['POST'])
def registrar_producto_inventario():
    data = request.get_json()
    print(data)  # Para verificar los datos recibidos

    nombre_tienda = data.get("nombre_tienda")
    nombre_producto = data.get("nombre_producto")
    categoria = data.get("categoria")
    fecha_alta = data.get("fecha_alta")  # Se espera formato 'dd-mm-yyyy'
    cantidad = data.get("cantidad")
    precio = data.get("precio")

    # Verificar que todos los campos estén presentes
    if not all([nombre_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        fecha_alta = datetime.strptime(fecha_alta, '%d-%m-%Y').date()
        if fecha_alta != datetime.today().date():
            return jsonify({"error": "La fecha introducida no coincide con la fecha actual"}), 400
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido, debe ser 'dd-mm-yyyy'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Validar que la tienda existe y obtener su ID
    query_tienda = "SELECT id_tienda FROM Tienda WHERE nombre = ?"
    cursor.execute(query_tienda, (nombre_tienda,))
    id_tienda_row = cursor.fetchone()

    if id_tienda_row is None:
        return jsonify({"error": f"No se encontró la tienda con nombre '{nombre_tienda}'"}), 404

    id_tienda = id_tienda_row[0]  # Obtener el ID de la tienda correctamente

    # Insertar el producto en la base de datos
    query_insert = """
    INSERT INTO Producto (id_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query_insert, (id_tienda, nombre_producto, categoria, fecha_alta, cantidad, precio))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Producto registrado con éxito",
        "detalles": {
            "tienda": nombre_tienda,
            "producto": nombre_producto,
            "categoría": categoria,
            "fecha_alta": fecha_alta.strftime('%d-%m-%Y'),
            "cantidad": cantidad,
            "precio": precio
        }
    }), 201  # Cambiado a 201 para indicar creación exitosa


@app.route('/api/registrar_venta', methods=['POST'])
def registrar_venta():
    data = request.get_json()
    print("Datos recibidos:", data)

    # Verificar si se recibió data
    if data is None:
        print("No se recibió ningún dato.")
        return jsonify({"error": "No se recibieron datos."}), 400

    nombre_tienda = data.get("nombre_tienda")
    nombre_producto = data.get("nombre_producto").capitalize()
    cantidad_vendida = data.get("cantidad_vendida")

    print("Nombre de la tienda:", nombre_tienda)
    print("Nombre del producto:", nombre_producto)
    print("Cantidad vendida:", cantidad_vendida)

    # Validar ID de tienda
    if not nombre_tienda:
        print("ID de tienda inválido.")
        return jsonify({"error": "ID de tienda inválido."}), 400

    # Validar nombre del producto y cantidad
    if not nombre_producto or not isinstance(cantidad_vendida, int) or cantidad_vendida <= 0:
        print("Datos de venta inválidos.")
        return jsonify({"error": "Datos de venta inválidos."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si la tienda existe
    query_tienda = "SELECT id_tienda FROM Tienda WHERE nombre = ?"
    cursor.execute(query_tienda, (nombre_tienda,))
    id_tienda_row = cursor.fetchone()

    if id_tienda_row is None:
        print(f"No se encontró la tienda '{nombre_tienda}'.")
        return jsonify({"error": f"No se encontró la tienda '{nombre_tienda}'."}), 404

    id_tienda = id_tienda_row[0]
    print("ID de tienda encontrada:", id_tienda)

    # Verificar si el producto está disponible en la tienda
    query_producto = """
    SELECT cantidad, precio
    FROM Producto
    WHERE id_tienda = ? AND nombre_producto = ?
    """
    cursor.execute(query_producto, (id_tienda, nombre_producto))
    producto_row = cursor.fetchone()

    if producto_row is None:
        print(f"No se encontró el producto '{nombre_producto}' en la tienda '{nombre_tienda}'.")
        return jsonify({"error": f"No se encontró el producto '{nombre_producto}' en la tienda '{nombre_tienda}'."}), 404

    cantidad_disponible, precio_unitario = producto_row
    print("Cantidad disponible:", cantidad_disponible)
    print("Precio unitario:", precio_unitario)

    # Validar que hay suficiente cantidad disponible
    if cantidad_vendida > cantidad_disponible:
        print(f"No hay suficiente cantidad disponible del producto '{nombre_producto}'. Cantidad disponible: {cantidad_disponible}.")
        return jsonify({
            "error": f"No hay suficiente cantidad disponible del producto '{nombre_producto}'. Cantidad disponible: {cantidad_disponible}."
        }), 400

    # Realizar la venta (actualizar la cantidad en la base de datos)
    nueva_cantidad = cantidad_disponible - cantidad_vendida
    update_query = """
    UPDATE Producto
    SET cantidad = ?
    WHERE id_tienda = ? AND nombre_producto = ?
    """
    cursor.execute(update_query, (nueva_cantidad, id_tienda, nombre_producto))
    conn.commit()  # Guardar los cambios

    # Devolver mensaje de éxito
    print(f"Venta registrada con éxito en '{nombre_tienda}' para el producto '{nombre_producto}'.")
    return jsonify({
        "mensaje": f"Venta registrada con éxito en '{nombre_tienda}' para el producto '{nombre_producto}'.",
        "cantidad_vendida": cantidad_vendida,
        "precio_total": cantidad_vendida * precio_unitario  # Precio total de la venta
    }), 200  # Código 200 para éxito


if __name__ == '__main__':
    app.run(debug=True)
