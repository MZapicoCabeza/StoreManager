from datetime import datetime, time


def comprueba_fechas(fecha):
    formato = "%d-%m-%Y"
    try:
        fecha = datetime.strptime(fecha, formato).date()
        return fecha

    except ValueError:
        print("\n>> Formato de fecha incorrecto. Debe ser dd-mm-yyyy. Intentelo de nuevo.")
        return None