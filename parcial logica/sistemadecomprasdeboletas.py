"""
Sistema de Compra de Boletas - Cine Land
"""

# GENEROS disponibles (tupla, inmutable)
GENEROS = ("Accion", "Comedia", "Drama", "Terror")

# Lista de peliculas (cada una es un diccionario)
peliculas = [
    {"id": 1, "titulo": "Avengers: Doomsday",          "genero": GENEROS[0], "sala": "A1",
     "horarios": ("14:00", "17:30", "21:00"), "precio_normal": 18000, "precio_vip": 28000, "asientos": 80},
    {"id": 2, "titulo": "Scary Movie 5",                "genero": GENEROS[1], "sala": "B2",
     "horarios": ("13:00", "15:30", "18:00"), "precio_normal": 15000, "precio_vip": 24000, "asientos": 60},
    {"id": 3, "titulo": "50 Sombras de Grey",           "genero": GENEROS[2], "sala": "C3",
     "horarios": ("16:00", "19:00", "22:00"), "precio_normal": 16000, "precio_vip": 25000, "asientos": 45},
    {"id": 4, "titulo": "Guardianes de la Galaxia",     "genero": GENEROS[0], "sala": "A2",
     "horarios": ("14:30", "17:00", "20:30"), "precio_normal": 16000, "precio_vip": 26000, "asientos": 70},
    {"id": 5, "titulo": "El Senor de los Anillos",      "genero": GENEROS[2], "sala": "B1",
     "horarios": ("12:00", "15:00", "18:30"), "precio_normal": 14000, "precio_vip": 22000, "asientos": 55},
]

# Historial de compras de la sesion
historial_compras = []
contador_orden = 1


# ── VISUALIZACION ──────────────────────────────────────

def separador():
    print("-" * 50)


def mostrar_cartelera():
    separador()
    print("CARTELERA CINE LAND")
    separador()
    print(f"{'ID':<5} {'Titulo':<32} {'Asientos'}")
    separador()
    for p in peliculas:
        estado = str(p["asientos"]) + " disponibles" if p["asientos"] > 0 else "Agotado"
        print(f"{p['id']:<5} {p['titulo']:<32} {estado}")
    separador()


def mostrar_detalle(pelicula):
    separador()
    print(f"Pelicula : {pelicula['titulo']}")
    print(f"Genero   : {pelicula['genero']}")
    print(f"Sala     : {pelicula['sala']}")
    print(f"Asientos : {pelicula['asientos']} disponibles")
    print("Horarios :")
    for i, h in enumerate(pelicula["horarios"], 1):
        print(f"  {i}. {h}")
    print(f"Precio normal : $ {pelicula['precio_normal']:,} COP")
    print(f"Precio VIP    : $ {pelicula['precio_vip']:,} COP")
    separador()


def mostrar_historial():
    if not historial_compras:
        print("No hay compras registradas.")
        return
    separador()
    print("HISTORIAL DE COMPRAS")
    separador()
    total_sesion = 0
    for c in historial_compras:
        print(f"Orden #{c['orden_id']}")
        print(f"  Pelicula : {c['pelicula']}")
        print(f"  Horario  : {c['horario']}")
        print(f"  Tipo     : {c['tipo']}")
        print(f"  Cantidad : {c['cantidad']}")
        print(f"  Total    : $ {c['total']:,} COP")
        print()
        total_sesion += c["total"]
    print(f"Total gastado en la sesion: $ {total_sesion:,} COP")
    separador()


# ── LOGICA ─────────────────────────────────────────────

def buscar_pelicula(pelicula_id):
    """Retorna la pelicula con el id dado. Lanza ValueError si no existe."""
    for p in peliculas:
        if p["id"] == pelicula_id:
            return p
    raise ValueError(f"No existe una pelicula con ID {pelicula_id}.")


def seleccionar_pelicula():
    mostrar_cartelera()
    while True:
        try:
            pelicula_id = int(input("Ingresa el ID de la pelicula: "))
            pelicula = buscar_pelicula(pelicula_id)
            if pelicula["asientos"] == 0:
                raise RuntimeError("Esa pelicula esta agotada. Elige otra.")
            return pelicula
        except ValueError as e:
            print(f"Entrada invalida: {e}")
        except RuntimeError as e:
            print(e)


def seleccionar_horario(pelicula):
    horarios = pelicula["horarios"]
    while True:
        try:
            opcion = int(input(f"Elige el horario (1-{len(horarios)}): "))
            if not (1 <= opcion <= len(horarios)):
                raise IndexError("Numero de horario fuera de rango.")
            return horarios[opcion - 1]
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")


def seleccionar_tipo(pelicula):
    """Retorna una tupla (tipo, precio)."""
    print("Tipo de boleta:")
    print(f"  1. Normal - $ {pelicula['precio_normal']:,} COP")
    print(f"  2. VIP    - $ {pelicula['precio_vip']:,} COP")
    while True:
        try:
            opcion = int(input("Selecciona (1 o 2): "))
            if opcion == 1:
                return ("Normal", pelicula["precio_normal"])
            elif opcion == 2:
                return ("VIP", pelicula["precio_vip"])
            else:
                raise ValueError("Opcion invalida. Elige 1 o 2.")
        except ValueError as e:
            print(f"Error: {e}")


def seleccionar_cantidad(pelicula):
    disponibles = pelicula["asientos"]
    while True:
        try:
            cantidad = int(input(f"Cuantas boletas? (max {disponibles}): "))
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")
            if cantidad > disponibles:
                raise ValueError(f"Solo hay {disponibles} asientos disponibles.")
            if cantidad > 10:
                raise ValueError("No se pueden comprar mas de 10 boletas a la vez.")
            return cantidad
        except ValueError as e:
            print(f"Error: {e}")


def calcular_total(precio, cantidad):
    """Aplica descuento del 10% por 4 o mas boletas. Retorna diccionario con desglose."""
    subtotal = precio * cantidad
    descuento = int(subtotal * 0.10) if cantidad >= 4 else 0
    return {"subtotal": subtotal, "descuento": descuento, "total": subtotal - descuento}


def confirmar_compra(pelicula, horario, tipo, precio, cantidad, desglose):
    separador()
    print("RESUMEN DE COMPRA")
    separador()
    print(f"Pelicula   : {pelicula['titulo']}")
    print(f"Sala       : {pelicula['sala']}")
    print(f"Horario    : {horario}")
    print(f"Tipo       : {tipo}")
    print(f"Cantidad   : {cantidad}")
    print(f"Precio c/u : $ {precio:,} COP")
    print(f"Subtotal   : $ {desglose['subtotal']:,} COP")
    if desglose["descuento"] > 0:
        print(f"Descuento  : - $ {desglose['descuento']:,} COP (10% por 4+ boletas)")
    print(f"TOTAL      : $ {desglose['total']:,} COP")
    separador()
    while True:
        respuesta = input("Confirmar compra? (s/n): ").strip().lower()
        if respuesta in ("s", "si"):
            return True
        elif respuesta in ("n", "no"):
            return False
        else:
            print("Responde 's' o 'n'.")


def registrar_compra(pelicula, horario, tipo, cantidad, total):
    global contador_orden
    if pelicula["asientos"] < cantidad:
        raise RuntimeError("Error: asientos insuficientes al procesar la compra.")
    pelicula["asientos"] -= cantidad
    compra = {
        "orden_id": contador_orden,
        "pelicula": pelicula["titulo"],
        "horario": horario,
        "tipo": tipo,
        "cantidad": cantidad,
        "total": total,
    }
    historial_compras.append(compra)
    contador_orden += 1
    return compra


# ── FLUJO DE COMPRA ────────────────────────────────────

def flujo_compra():
    print("\nIniciando proceso de compra...\n")
    pelicula = seleccionar_pelicula()
    mostrar_detalle(pelicula)
    horario = seleccionar_horario(pelicula)
    tipo, precio = seleccionar_tipo(pelicula)
    cantidad = seleccionar_cantidad(pelicula)
    desglose = calcular_total(precio, cantidad)

    if not confirmar_compra(pelicula, horario, tipo, precio, cantidad, desglose):
        print("Compra cancelada.\n")
        return

    try:
        compra = registrar_compra(pelicula, horario, tipo, cantidad, desglose["total"])
        print(f"\nCompra exitosa. Orden #{compra['orden_id']}")
        print(f"Disfruta '{pelicula['titulo']}' a las {horario}\n")
    except RuntimeError as e:
        print(f"Error al procesar la compra: {e}\n")


# ── MENU PRINCIPAL ─────────────────────────────────────

def menu_principal():
    while True:
        separador()
        print("CINE LAND - SISTEMA DE BOLETAS")
        separador()
        print("1. Ver cartelera")
        print("2. Comprar boletas")
        print("3. Ver historial")
        print("4. Salir")
        separador()
        try:
            opcion = int(input("Elige una opcion: "))
        except ValueError:
            print("Ingresa un numero valido.\n")
            continue

        if opcion == 1:
            mostrar_cartelera()
        elif opcion == 2:
            flujo_compra()
        elif opcion == 3:
            mostrar_historial()
        elif opcion == 4:
            print("Hasta pronto.")
            break
        else:
            print("Opcion no valida.\n")


if __name__ == "__main__":
    menu_principal()