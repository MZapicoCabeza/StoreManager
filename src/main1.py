import os
import sqlite3
import gerente
import administrador
import marketing

DATABASE = "FIS2425-PL31.db"
Tablas = "\resources\schema.sql"
Datos = "\resources\data.sql"

# """
with open(Tablas, 'r') as sqlFile:
        sqlSchema = sqlFile.read() 

with open(Datos, 'r') as sqlFile:
        sqlData = sqlFile.read()


conexion = sqlite3.connect(DATABASE)

cursor = conexion.cursor()
cursor.executescript (sqlSchema)
cursor.executescript (sqlData)
cursor.close()
# """

##################################
print("\nBIENVENIDO/A")
conexion = sqlite3.connect(DATABASE)

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    in_ses = int(input("\n¿Como desea iniciar sesión? \n(1) Administrador de tienda  \n(2) Gerente de tienda \n(3) Responsable de marketing \n(4) Salir\n> "))

    while in_ses not in (1, 2, 3, 4):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n>> Error: Entrada no válida. Inténtelo de nuevo")
        in_ses = int(input("\n¿Como desea iniciar sesión? \n(1) Administrador de tienda  \n(2) Gerente de tienda \n(3) Responsable de marketing \n(4) Salir\n> "))


    os.system('cls' if os.name == 'nt' else 'clear')
    # Modo ADMINISTRADOR DE TIENDA
    if in_ses == 1:
        while True:
            #print("\n-----------------------------------------------------")
            print("\n-- ADMINISTRADOR DE TIENDA --")
            print('\n¿Qué función quiere realizar? \n (1) Registrar producto en el inventario \n (2) Mostrar el nivel de inventario de los productos por tienda \n (3) Registrar una venta \n (4) Menú de Inicio de Sesión')
            accion=int(input('> '))
            if accion not in (1,2,3,4):
                print("\n>> Error: Entrada no válida. Inténtelo de nuevo")
                continue
            elif accion==1:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                administrador.registrar_producto_inventario(cursor, conexion)
            elif accion==2:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                administrador.mostrar_inventario_por_tienda(cursor)
            elif accion ==3:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                administrador.registrar_venta_en_tienda(cursor, conexion)
            elif accion ==4:
                break

    # Modo GERENTE DE TIENDA
    elif in_ses == 2:
        while True:
            #print("\n-----------------------------------------------------")
            print("\n-- GERENTE DE TIENDA --")
            print('\n¿Qué función quiere realizar? \n (1) Registrar tienda \n (2) Informe de ventas en rango de fechas \n (3) Menú de Inicio de Sesión')
            accion=int(input('Accion: '))
            if accion not in (1,2,3):
                print("\n>> Error: Entrada no válida. Inténtelo de nuevo")
                continue
            elif accion==1:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                gerente.registrar_tienda(cursor, conexion)
            elif accion==2:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                gerente.informe_ventas(cursor)
            elif accion ==3:
                break   

    # Modo RESPONSABLE DE MARKETING
    elif in_ses == 3:
        while True:
            #print("\n-----------------------------------------------------")
            print("\n-- RESPONSABLE DE MARKETING --")
            print('\n¿Qué función quiere realizar? \n (1) Registrar cliente \n (2) Visualizar compras por cliente \n (3) Visualizar el total de ventas por tienda en los últimos 30 días \n (4) Menú de Inicio de Sesión')
            accion=int(input('Accion: '))
            if accion not in (1,2,3,4):
                print("\n>> Error: Entrada no válida. Inténtelo de nuevo")
                continue
            elif accion==1:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                marketing.registrar_nuevos_clientes(cursor, conexion)
            elif accion==2:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                marketing.visualizar_compras_clientes(cursor)
            elif accion ==3:
                os.system('cls' if os.name == 'nt' else 'clear')
                cursor = conexion.cursor()
                marketing.total_ventas_tienda_mes(cursor)
            elif accion ==4:
                break
    elif in_ses == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n¡Adiós!\n")
        break
