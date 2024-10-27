# src/database.py
import sqlite3
import os

DATABASE = "FIS2425-PL31.db"
TABLAS = "resources\schema.sql"
DATOS = "resources\data.sql"

def init_db():
    # Cargar el esquema y los datos desde los archivos SQL
    with open(TABLAS, 'r') as sqlFile:
        sqlSchema = sqlFile.read()

    with open(DATOS, 'r') as sqlFile:
        sqlData = sqlFile.read()

    # Conectar a la base de datos y ejecutar los scripts
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    cursor.executescript(sqlSchema)
    cursor.executescript(sqlData)

    # Cerrar la conexión
    cursor.close()
    conexion.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn
