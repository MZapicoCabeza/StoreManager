from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa CORS
from database import get_db_connection, init_db

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


if __name__ == '__main__':
    app.run(debug=True)
