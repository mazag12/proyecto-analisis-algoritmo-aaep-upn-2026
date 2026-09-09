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
        "codigo": "PC-001",
        "tipo": "Computadora",
        "marca": "Lenovo",
        "modelo": "ThinkCentre",
        "usuario": "Carlos Perez",
        "estado": "Operativo"
    },
    {
        "id": 2,
        "codigo": "LAP-002",
        "tipo": "Laptop",
        "marca": "HP",
        "modelo": "ProBook",
        "usuario": "Maria Lopez",
        "estado": "Operativo"
    },
    {
        "id": 3,
        "codigo": "PC-003",
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
        "codigo_equipo": "PC-001",
        "problema": "No enciende",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 5,
        "tiempo_estimado": 60,
        "estado": "Pendiente"
    },
    {
        "id": 2,
        "codigo_equipo": "LAP-002",
        "problema": "Temperatura elevada",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 4,
        "tiempo_estimado": 45,
        "estado": "Pendiente"
    },
    {
        "id": 3,
        "codigo_equipo": "PC-003",
        "problema": "Actualización de software",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 2,
        "tiempo_estimado": 30,
        "estado": "Pendiente"
    }
]


# BUSQUEDA DE EQUIPO

def buscar_equipo(codigo):

    for equipo in equipos:

        if equipo["codigo"].lower() == codigo.lower():

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

    if equipo is None:

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