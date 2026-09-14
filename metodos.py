# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 21:07:30 2026

@author: MAZAG
"""

import time


# DATOS

equipos = [
    {
        "id": 1,
        "codigo": "1001",
        "tipo": "Computadora",
        "marca": "Lenovo",
        "modelo": "ThinkCentre",
        "usuario": "Carlos Perez",
        "estado": "Operativo"
    },
    {
        "id": 2,
        "codigo": "1002",
        "tipo": "Laptop",
        "marca": "HP",
        "modelo": "ProBook",
        "usuario": "Maria Lopez",
        "estado": "Operativo"
    },
    {
        "id": 3,
        "codigo": "1003",
        "tipo": "Computadora",
        "marca": "Dell",
        "modelo": "OptiPlex",
        "usuario": "Juan Torres",
        "estado": "Operativo"
    }
]


incidencias = [
    {
        "id": 1,
        "codigo_equipo": "1001",
        "problema": "No enciende",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 5,
        "tiempo_estimado": 60,
        "estado": "Pendiente"
    },
    {
        "id": 2,
        "codigo_equipo": "1002",
        "problema": "Temperatura elevada",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 4,
        "tiempo_estimado": 45,
        "estado": "Pendiente"
    },
    {
        "id": 3,
        "codigo_equipo": "1003",
        "problema": "Actualización de software",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 2,
        "tiempo_estimado": 30,
        "estado": "Pendiente"
    }
]


# BUSQUEDA DE EQUIPO

def buscar_equipo(codigo):
    if not isinstance(codigo, str):
        return None

    codigo = codigo.strip().upper()

    for equipo in equipos:
        if equipo["codigo"].upper() == codigo:
            return equipo

    return None


# BUSQUEDA DE INCIDENCIA

def buscar_incidencia(id_incidencia):

    for incidencia in incidencias:

        if incidencia["id"] == id_incidencia:

            return incidencia

    return None


# ORDENAMIENTO BURBUJA DESCENDENTE

def burbuja_descendente(lista):

    lista = lista.copy()

    n = len(lista)

    for i in range(n):

        for j in range(0, n - i - 1):

            if lista[j]["prioridad"] < lista[j + 1]["prioridad"]:

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


# ORDENAMIENTO POR TIEMPO

def ordenar_por_tiempo(lista):

    lista = lista.copy()

    n = len(lista)

    for i in range(n):

        for j in range(0, n - i - 1):

            if lista[j]["tiempo_estimado"] > lista[j + 1]["tiempo_estimado"]:

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


# REGISTRAR EQUIPO

def registrar_equipo(codigo, tipo, marca, modelo, usuario):
    codigo = str(codigo).strip()
    tipo = str(tipo).strip()
    marca = str(marca).strip()
    modelo = str(modelo).strip()
    usuario = str(usuario).strip()

    if (
        not datos_equipo_validos(codigo, tipo, marca, modelo, usuario)
        or buscar_equipo(codigo) is not None
    ):
        return False

    nuevo_id = len(equipos) + 1

    equipo = {
        "id": nuevo_id,
        "codigo": codigo,
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "usuario": usuario,
        "estado": "Operativo"
    }

    equipos.append(equipo)

    return equipo


# REGISTRAR INCIDENCIA

def registrar_incidencia(
    codigo,
    problema,
    tipo_mantenimiento,
    prioridad,
    tiempo
):
    equipo = buscar_equipo(codigo)

    if (
        equipo is None
        or not problema_valido(problema)
        or not isinstance(prioridad, int)
        or prioridad < 1
        or prioridad > 5
        or not isinstance(tiempo, int)
        or tiempo < 1
    ):
        return False

    nuevo_id = len(incidencias) + 1

    incidencia = {
        "id": nuevo_id,
        "codigo_equipo": codigo,
        "problema": problema,
        "tipo_mantenimiento": tipo_mantenimiento,
        "prioridad": prioridad,
        "tiempo_estimado": tiempo,
        "estado": "Pendiente"
    }

    incidencias.append(incidencia)

    equipo["estado"] = "En mantenimiento"

    return incidencia


# ACTUALIZAR ESTADO

def actualizar_estado(id_incidencia, nuevo_estado):

    incidencia = buscar_incidencia(id_incidencia)

    if incidencia is None:

        return False

    incidencia["estado"] = nuevo_estado

    if nuevo_estado == "Finalizado":

        equipo = buscar_equipo(
            incidencia["codigo_equipo"]
        )

        if equipo:

            equipo["estado"] = "Operativo"

    elif nuevo_estado == "En proceso":

        equipo = buscar_equipo(
            incidencia["codigo_equipo"]
        )

        if equipo:

            equipo["estado"] = "En mantenimiento"

    return True


# PLANIFICAR MANTENIMIENTO

def planificar_mantenimiento():

    pendientes = []

    for incidencia in incidencias:

        if incidencia["estado"] == "Pendiente":

            pendientes.append(incidencia)

    return burbuja_descendente(pendientes)


# ESTADISTICAS

def obtener_estadisticas():

    total_equipos = len(equipos)
    total_incidencias = len(incidencias)

    pendientes = 0
    proceso = 0
    finalizadas = 0

    preventivo = 0
    correctivo = 0
    predictivo = 0

    tiempo_total = 0

    for incidencia in incidencias:

        tiempo_total += incidencia["tiempo_estimado"]

        if incidencia["estado"] == "Pendiente":

            pendientes += 1

        elif incidencia["estado"] == "En proceso":

            proceso += 1

        elif incidencia["estado"] == "Finalizado":

            finalizadas += 1

        if incidencia["tipo_mantenimiento"] == "Preventivo":

            preventivo += 1

        elif incidencia["tipo_mantenimiento"] == "Correctivo":

            correctivo += 1

        elif incidencia["tipo_mantenimiento"] == "Predictivo":

            predictivo += 1

    if total_incidencias > 0:

        promedio = tiempo_total / total_incidencias

    else:

        promedio = 0

    return {
        "total_equipos": total_equipos,
        "total_incidencias": total_incidencias,
        "pendientes": pendientes,
        "proceso": proceso,
        "finalizadas": finalizadas,
        "preventivo": preventivo,
        "correctivo": correctivo,
        "predictivo": predictivo,
        "tiempo_total": tiempo_total,
        "promedio": promedio
    }


# MEDIR TIEMPO DEL ALGORITMO

def medir_ordenamiento():

    lista = incidencias.copy()

    inicio = time.perf_counter()

    resultado = burbuja_descendente(lista)

    fin = time.perf_counter()

    tiempo = fin - inicio

    return resultado, tiempo


# DEMOSTRACION DE ALGORITMOS

def demostracion_algoritmos():

    lista = [44, 55, 12, 42, 94, 18, 6, 67]

    original = lista.copy()

    # Ascendente

    ascendente = lista.copy()

    inicio = time.perf_counter()

    n = len(ascendente)

    for i in range(n):

        for j in range(0, n - i - 1):

            if ascendente[j] > ascendente[j + 1]:

                ascendente[j], ascendente[j + 1] = (
                    ascendente[j + 1],
                    ascendente[j]
                )

    fin = time.perf_counter()

    tiempo_ascendente = fin - inicio

    # Descendente

    descendente = lista.copy()

    inicio = time.perf_counter()

    descendente = burbuja_descendente_simple(descendente)

    fin = time.perf_counter()

    tiempo_descendente = fin - inicio

    return (
        original,
        ascendente,
        tiempo_ascendente,
        descendente,
        tiempo_descendente
    )


# BURBUJA SIMPLE DESCENDENTE

#Verificación de datos
def burbuja_descendente_simple(lista):

    n = len(lista)

    for i in range(n):

        for j in range(0, n - i - 1):

            if lista[j] < lista[j + 1]:

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista

def validar_texto(mensaje, campo):
    while True:
        valor = input(mensaje).strip()

        if valor == "":
            print(f"ERROR: El campo {campo} no puede estar vacío.")
            continue

        return valor


def texto_valido(valor, permitir_numeros=False):
    if not isinstance(valor, str):
        return False

    valor = valor.strip()

    if valor == "" or len(valor) > 50:
        return False

    for caracter in valor:
        if caracter == " ":
            continue

        if caracter.isalpha():
            continue

        if permitir_numeros and caracter.isdigit():
            continue

        return False

    return True


def datos_equipo_validos(codigo, tipo, marca, modelo, usuario):
    return (
        isinstance(codigo, str)
        and codigo.isdigit()
        and 1 <= len(codigo) <= 5
        and texto_valido(tipo)
        and texto_valido(marca)
        and texto_valido(modelo, permitir_numeros=True)
        and texto_valido(usuario)
    )


def validar_texto_equipo(mensaje, campo, permitir_numeros=False):
    while True:
        valor = input(mensaje).strip()

        if valor == "":
            print(f"ERROR: El campo {campo} no puede estar vacío.")
            continue

        if len(valor) < 3:
            print(f"ERROR: El campo {campo} no puede ser menor de  3 caracteres.")
            continue

        if len(valor) > 50:
            print(f"ERROR: El campo {campo} no puede superar los 50 caracteres.")
            continue

        if not texto_valido(valor, permitir_numeros):
            if permitir_numeros:
                regla = "solo letras, números y espacios"
            else:
                regla = "solo letras y espacios"

            print(f"ERROR: El campo {campo} debe contener {regla}.")
            continue

        return valor


def problema_valido(problema):
    if not isinstance(problema, str):
        return False

    problema = problema.strip()

    if len(problema) < 10 or len(problema) > 250:
        return False

    signos_permitidos = ",.;:!?¡¿-()/"

    for caracter in problema:
        if (
            caracter.isspace()
            or caracter.isalpha()
            or caracter.isdigit()
            or caracter in signos_permitidos
        ):
            continue

        return False

    return True


def validar_problema():
    while True:
        problema = input(
            "Problema (10-250 caracteres; letras, números y puntuación): "
        ).strip()

        if len(problema) < 10:
            print("ERROR: El problema debe tener mínimo 10 caracteres.")
            continue

        if len(problema) > 250:
            print(
                f"ERROR: El problema tiene {len(problema)} caracteres. "
                "El máximo permitido es de 250 caracteres."
            )
            continue

        if not problema_valido(problema):
            print(
                "ERROR: Use letras, números, espacios y signos "
                "de puntuación."
            )
            continue

        return problema


def validar_tiempo_estimado():
    print("\nTiempo estimado")
    print("Registre el tiempo como horas completas y minutos de 0 a 59.")
    print("Ejemplo: 1 hora y 30 minutos = 90 minutos.")

    while True:
        horas = validar_entero("Horas: ", 0)
        minutos = validar_entero("Minutos (0-59): ", 0, 59)

        if horas == 0 and minutos == 0:
            print("ERROR: El tiempo estimado debe ser mayor que cero.")
            continue

        return horas * 60 + minutos


def confirmar_accion(mensaje):
    while True:
        respuesta = input(f"{mensaje} (S/N): ").strip().upper()

        if respuesta in ("S", "SI", "SÍ"):
            return True

        if respuesta in ("N", "NO"):
            return False

        print("ERROR: Responda S para sí o N para no.")


def validar_entero(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()

        try:
            numero = int(valor)

            if minimo is not None and numero < minimo:
                print(
                    f"ERROR: El valor debe ser mayor o igual a {minimo}."
                )
                continue

            if maximo is not None and numero > maximo:
                print(
                    f"ERROR: El valor debe ser menor o igual a {maximo}."
                )
                continue

            return numero

        except ValueError:
            print("ERROR: Debe ingresar un número entero válido.")


def validar_codigo_equipo(mensaje):
    while True:
        codigo = input(mensaje).strip().upper()

        if codigo == "":
            print("ERROR: El código no puede estar vacío.")
            continue

        equipo = buscar_equipo(codigo)

        if equipo is None:
            print(f"ERROR: No existe el equipo con código '{codigo}'.")
            continue

        return codigo


def validar_codigo_nuevo():
    while True:
        codigo = input("Código: ").strip().upper()

        if codigo == "":
            print("ERROR: El código no puede estar vacío.")
            continue

        if not codigo.isdigit():
            print("ERROR: El código debe contener solo números.")
            continue

        if len(codigo) > 5:
            print("ERROR: El código no puede superar 5 caracteres.")
            continue

        if buscar_equipo(codigo) is not None:
            print(
                f"ERROR: Ya existe un equipo con el código '{codigo}'."
            )
            continue

        return codigo


def validar_tipo_mantenimiento():
    while True:
        print("\nTipo de mantenimiento")
        print("1. Preventivo")
        print("2. Correctivo")
        print("3. Predictivo")

        opcion = input("Seleccione: ").strip()

        tipos = {
            "1": "Preventivo",
            "2": "Correctivo",
            "3": "Predictivo"
        }

        if opcion in tipos:
            return tipos[opcion]

        print("ERROR: Seleccione una opción entre 1 y 3.")


def validar_estado():
    while True:
        print("\nEstado de la incidencia")
        print("1. Pendiente")
        print("2. En proceso")
        print("3. Finalizado")

        opcion = input("Seleccione: ").strip()

        estados = {
            "1": "Pendiente",
            "2": "En proceso",
            "3": "Finalizado"
        }

        if opcion in estados:
            return estados[opcion]

        print("ERROR: Seleccione una opción entre 1 y 3.")
