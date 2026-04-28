"""
🎬 Sistema de Compra de Boletas - CineMax
==========================================
Utiliza: tuplas, listas, diccionarios, funciones y excepciones.
"""

# ─────────────────────────────────────────
# DATOS DEL CINE  (estructuras de datos)
# ─────────────────────────────────────────

# Tupla de géneros disponibles (inmutable)
GENEROS = ("Acción", "Comedia", "Drama", "Terror", "Animación", "Ciencia Ficción")

# Lista de películas en cartelera
# Cada película es un diccionario con su información
peliculas = [
    {
        "id": 1,
        "titulo": "Guardianes del Cosmos",
        "genero": GENEROS[5],
        "duracion_min": 148,
        "sala": "A1",
        "horarios": ("14:00", "17:30", "21:00"),
        "precio_normal": 18_000,
        "precio_vip": 28_000,
        "asientos_disponibles": 80,
    },
    {
        "id": 2,
        "titulo": "La Gran Aventura",
        "genero": GENEROS[4],
        "duracion_min": 95,
        "sala": "B2",
        "horarios": ("13:00", "15:30", "18:00"),
        "precio_normal": 15_000,
        "precio_vip": 24_000,
        "asientos_disponibles": 60,
    },
    {
        "id": 3,
        "titulo": "Sombras en la Noche",
        "genero": GENEROS[3],
        "duracion_min": 112,
        "sala": "C3",
        "horarios": ("16:00", "19:00", "22:00"),
        "precio_normal": 16_000,
        "precio_vip": 25_000,
        "asientos_disponibles": 45,
    },
    {
        "id": 4,
        "titulo": "Corazones Rotos",
        "genero": GENEROS[2],
        "duracion_min": 105,
        "sala": "A2",
        "horarios": ("14:30", "17:00", "20:30"),
        "precio_normal": 16_000,
        "precio_vip": 26_000,
        "asientos_disponibles": 70,
    },
    {
        "id": 5,
        "titulo": "Locuras en Familia",
        "genero": GENEROS[1],
        "duracion_min": 90,
        "sala": "B1",
        "horarios": ("12:00", "15:00", "18:30"),
        "precio_normal": 14_000,
        "precio_vip": 22_000,
        "asientos_disponibles": 55,
    },
]

# Historial de compras (lista de diccionarios)
historial_compras: list[dict] = []

# Contador global de órdenes
_orden_counter = 1


# ─────────────────────────────────────────
# FUNCIONES DE VISUALIZACIÓN
# ─────────────────────────────────────────

def limpiar_pantalla():
    """Imprime saltos de línea para simular pantalla limpia."""
    print("\n" * 2)


def separador(caracter: str = "─", largo: int = 55):
    print(caracter * largo)


def mostrar_cartelera():
    """Muestra todas las películas disponibles."""
    separador("═")
    print("🎬  CARTELERA CINEMAX  🎬".center(55))
    separador("═")
    print(f"{'ID':<4} {'Título':<28} {'Género':<18} {'Asientos'}")
    separador()
    for p in peliculas:
        estado = f"{p['asientos_disponibles']} disponibles" if p["asientos_disponibles"] > 0 else "❌ Agotado"
        print(f"{p['id']:<4} {p['titulo']:<28} {p['genero']:<18} {estado}")
    separador()


def mostrar_detalle_pelicula(pelicula: dict):
    """Muestra los detalles completos de una película."""
    separador("═")
    print(f"  🎥  {pelicula['titulo'].upper()}")
    separador("═")
    print(f"  Género      : {pelicula['genero']}")
    print(f"  Duración    : {pelicula['duracion_min']} minutos")
    print(f"  Sala        : {pelicula['sala']}")
    print(f"  Disponibles : {pelicula['asientos_disponibles']} asientos")
    print(f"\n  🕐 Horarios disponibles:")
    for i, h in enumerate(pelicula["horarios"], 1):
        print(f"     {i}. {h}")
    print(f"\n  💰 Precios:")
    print(f"     Normal : $ {pelicula['precio_normal']:,.0f} COP")
    print(f"     VIP    : $ {pelicula['precio_vip']:,.0f} COP")
    separador()


def mostrar_historial():
    """Muestra el historial de compras de la sesión."""
    if not historial_compras:
        print("\n  📭 No hay compras registradas en esta sesión.\n")
        return
    separador("═")
    print("  📋  HISTORIAL DE COMPRAS".center(55))
    separador("═")
    total_sesion = 0
    for compra in historial_compras:
        print(f"  Orden #{compra['orden_id']}")
        print(f"    Película  : {compra['pelicula']}")
        print(f"    Horario   : {compra['horario']}")
        print(f"    Tipo      : {compra['tipo_boleta']}")
        print(f"    Cantidad  : {compra['cantidad']}")
        print(f"    Total     : $ {compra['total']:,.0f} COP")
        separador("-", 40)
        total_sesion += compra["total"]
    print(f"\n  💵 Total gastado en sesión: $ {total_sesion:,.0f} COP")
    separador()


# ─────────────────────────────────────────
# FUNCIONES DE LÓGICA / NEGOCIO
# ─────────────────────────────────────────

def buscar_pelicula_por_id(pelicula_id: int) -> dict:
    """
    Retorna el diccionario de la película con el id dado.
    Lanza ValueError si no existe.
    """
    for p in peliculas:
        if p["id"] == pelicula_id:
            return p
    raise ValueError(f"No existe una película con ID {pelicula_id}.")


def seleccionar_pelicula() -> dict:
    """Solicita al usuario que elija una película y la retorna."""
    mostrar_cartelera()
    while True:
        try:
            pelicula_id = int(input("\n  👉 Ingresa el ID de la película: "))
            pelicula = buscar_pelicula_por_id(pelicula_id)
            if pelicula["asientos_disponibles"] == 0:
                raise RuntimeError("Lo sentimos, esta película está agotada. Elige otra.")
            return pelicula
        except ValueError as e:
            print(f"  ⚠️  Entrada inválida: {e}")
        except RuntimeError as e:
            print(f"  ⚠️  {e}")


def seleccionar_horario(pelicula: dict) -> str:
    """Solicita al usuario que elija un horario y lo retorna."""
    horarios = pelicula["horarios"]
    while True:
        try:
            opcion = int(input(f"  👉 Elige el horario (1-{len(horarios)}): "))
            if not (1 <= opcion <= len(horarios)):
                raise IndexError("Número de horario fuera de rango.")
            return horarios[opcion - 1]
        except (ValueError, IndexError) as e:
            print(f"  ⚠️  {e} Intenta de nuevo.")


def seleccionar_tipo_boleta(pelicula: dict) -> tuple[str, int]:
    """
    Solicita al usuario el tipo de boleta.
    Retorna una tupla (tipo, precio).
    """
    print("\n  🎟️  Tipo de boleta:")
    print(f"     1. Normal  - $ {pelicula['precio_normal']:,.0f} COP")
    print(f"     2. VIP     - $ {pelicula['precio_vip']:,.0f} COP")
    while True:
        try:
            opcion = int(input("  👉 Selecciona (1 o 2): "))
            if opcion == 1:
                return ("Normal", pelicula["precio_normal"])
            elif opcion == 2:
                return ("VIP", pelicula["precio_vip"])
            else:
                raise ValueError("Opción inválida. Elige 1 o 2.")
        except ValueError as e:
            print(f"  ⚠️  {e}")


def seleccionar_cantidad(pelicula: dict) -> int:
    """Solicita al usuario la cantidad de boletas."""
    disponibles = pelicula["asientos_disponibles"]
    while True:
        try:
            cantidad = int(input(f"  👉 ¿Cuántas boletas? (máx. {disponibles}): "))
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")
            if cantidad > disponibles:
                raise ValueError(f"Solo hay {disponibles} asientos disponibles.")
            if cantidad > 10:
                raise ValueError("No se pueden comprar más de 10 boletas a la vez.")
            return cantidad
        except ValueError as e:
            print(f"  ⚠️  {e}")


def calcular_total(precio_unitario: int, cantidad: int) -> dict:
    """
    Calcula el desglose del total de la compra.
    Aplica descuento del 10 % por 4 o más boletas.
    Retorna un diccionario con el desglose.
    """
    subtotal = precio_unitario * cantidad
    descuento = 0
    if cantidad >= 4:
        descuento = int(subtotal * 0.10)
    total = subtotal - descuento
    return {
        "subtotal": subtotal,
        "descuento": descuento,
        "total": total,
    }


def confirmar_compra(pelicula: dict, horario: str, tipo: str,
                     precio: int, cantidad: int, desglose: dict) -> bool:
    """Muestra el resumen y solicita confirmación al usuario."""
    separador("═")
    print("  📋  RESUMEN DE COMPRA")
    separador("═")
    print(f"  Película   : {pelicula['titulo']}")
    print(f"  Sala       : {pelicula['sala']}")
    print(f"  Horario    : {horario}")
    print(f"  Tipo       : {tipo}")
    print(f"  Cantidad   : {cantidad} boleta(s)")
    print(f"  Precio c/u : $ {precio:,.0f} COP")
    separador("-", 40)
    print(f"  Subtotal   : $ {desglose['subtotal']:,.0f} COP")
    if desglose["descuento"] > 0:
        print(f"  Descuento  : - $ {desglose['descuento']:,.0f} COP  (10% por 4+ boletas)")
    print(f"  TOTAL      : $ {desglose['total']:,.0f} COP")
    separador()

    while True:
        respuesta = input("  ✅ ¿Confirmar compra? (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí", "y", "yes"):
            return True
        elif respuesta in ("n", "no"):
            return False
        else:
            print("  ⚠️  Responde 's' para sí o 'n' para no.")


def registrar_compra(pelicula: dict, horario: str, tipo: str,
                     cantidad: int, total: int):
    """
    Registra la compra en el historial y actualiza los asientos.
    Lanza RuntimeError si no hay suficientes asientos (condición de carrera simulada).
    """
    global _orden_counter

    if pelicula["asientos_disponibles"] < cantidad:
        raise RuntimeError("Error inesperado: asientos insuficientes al procesar la compra.")

    # Actualizar disponibilidad
    pelicula["asientos_disponibles"] -= cantidad

    # Guardar en historial
    compra = {
        "orden_id": _orden_counter,
        "pelicula": pelicula["titulo"],
        "horario": horario,
        "tipo_boleta": tipo,
        "cantidad": cantidad,
        "total": total,
    }
    historial_compras.append(compra)
    _orden_counter += 1
    return compra


# ─────────────────────────────────────────
# FLUJO PRINCIPAL
# ─────────────────────────────────────────

def flujo_compra():
    """Ejecuta el flujo completo de compra de una boleta."""
    limpiar_pantalla()
    print("\n  🎟️  Iniciando proceso de compra...\n")

    # 1. Seleccionar película
    pelicula = seleccionar_pelicula()

    # 2. Mostrar detalle
    limpiar_pantalla()
    mostrar_detalle_pelicula(pelicula)

    # 3. Seleccionar horario
    horario = seleccionar_horario(pelicula)

    # 4. Tipo de boleta → tupla (tipo, precio)
    tipo, precio = seleccionar_tipo_boleta(pelicula)

    # 5. Cantidad
    cantidad = seleccionar_cantidad(pelicula)

    # 6. Calcular total
    desglose = calcular_total(precio, cantidad)

    # 7. Confirmar
    if not confirmar_compra(pelicula, horario, tipo, precio, cantidad, desglose):
        print("\n  ❌ Compra cancelada.\n")
        return

    # 8. Registrar
    try:
        compra = registrar_compra(pelicula, horario, tipo, cantidad, desglose["total"])
        print(f"\n  ✅ ¡Compra exitosa! Orden #{compra['orden_id']}")
        print(f"     Disfruta '{pelicula['titulo']}' a las {horario} 🎉\n")
    except RuntimeError as e:
        print(f"\n  ❌ Error al procesar la compra: {e}\n")


def menu_principal():
    """Menú principal del sistema."""
    while True:
        separador("═")
        print("  🎬  CINEMAX - SISTEMA DE BOLETAS  🎬".center(55))
        separador("═")
        print("  1. Ver cartelera")
        print("  2. Comprar boletas")
        print("  3. Ver historial de compras")
        print("  4. Salir")
        separador()

        try:
            opcion = int(input("  👉 Elige una opción: "))
        except ValueError:
            print("  ⚠️  Por favor ingresa un número válido.\n")
            continue

        if opcion == 1:
            limpiar_pantalla()
            mostrar_cartelera()
            input("  Presiona Enter para continuar...")
        elif opcion == 2:
            flujo_compra()
            input("  Presiona Enter para continuar...")
        elif opcion == 3:
            limpiar_pantalla()
            mostrar_historial()
            input("  Presiona Enter para continuar...")
        elif opcion == 4:
            separador()
            print("  👋 ¡Gracias por usar CineMax! Hasta pronto.")
            separador()
            break
        else:
            print("  ⚠️  Opción no válida. Elige entre 1 y 4.\n")


# ─────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────

if __name__ == "__main__":
    menu_principal()