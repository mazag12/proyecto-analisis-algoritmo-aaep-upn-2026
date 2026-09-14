# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 21:08:08 2026

@author: MAZAG
"""

from metodos import *


# MOSTRAR EQUIPOS


def mostrar_equipos():

    print("\n")
    print("=" * 70)
    print("                 LISTA DE EQUIPOS")
    print("=" * 70)

    for equipo in equipos:

        print(f"""
ID       : {equipo['id']}
Código   : {equipo['codigo']}
Tipo     : {equipo['tipo']}
Marca    : {equipo['marca']}
Modelo   : {equipo['modelo']}
Usuario  : {equipo['usuario']}
Estado   : {equipo['estado']}
----------------------------------------
""")


# MOSTRAR INCIDENCIAS


def mostrar_incidencias(lista=None):

    if lista is None:

        lista = incidencias

    print("\n")
    print("=" * 90)
    print("                    INCIDENCIAS")
    print("=" * 90)

    for incidencia in lista:

        print(
            f"ID: {incidencia['id']} | "
            f"Equipo: {incidencia['codigo_equipo']} | "
            f"Problema: {incidencia['problema']} | "
            f"Mantenimiento: {incidencia['tipo_mantenimiento']} | "
            f"Prioridad: {incidencia['prioridad']} | "
            f"Tiempo: {incidencia['tiempo_estimado']} min | "
            f"Estado: {incidencia['estado']}"
        )


# MENU REGISTRAR EQUIPO


def menu_registrar_equipo():
    print("\n")
    print("=" * 50)
    print("             REGISTRAR EQUIPO")
    print("=" * 50)
    print("Ingrese los datos del equipo. El código debe tener de 1 a 5 dígitos.")

    codigo = validar_codigo_nuevo()

    tipo = validar_texto_equipo(
        "Tipo: ",
        "tipo"
    )

    marca = validar_texto_equipo(
        "Marca: ",
        "marca"
    )

    modelo = validar_texto_equipo(
        "Modelo: ",
        "modelo",
        permitir_numeros=True
    )

    usuario = validar_texto_equipo(
        "Usuario: ",
        "usuario"
    )

    equipo = registrar_equipo(
        codigo,
        tipo,
        marca,
        modelo,
        usuario
    )

    if equipo and confirmar_accion("¿Confirmar registro del equipo?"):
        print("\nEquipo registrado correctamente.")
        print(f"ID asignado: {equipo['id']}")
    elif equipo:
        equipos.remove(equipo)
        print("\nRegistro cancelado. No se guardó el equipo.")
    else:
        print("\nERROR: Los datos del equipo no son válidos.")


# MENU REGISTRAR INCIDENCIA


def menu_registrar_incidencia():
    print("\n")
    print("=" * 50)
    print("            REGISTRAR INCIDENCIA")
    print("=" * 50)
    print("Complete los datos en orden. Puede cancelar antes de confirmar.")

    codigo = validar_codigo_equipo(
        "Código del equipo (ejemplo: 1001): "
    )
    equipo = buscar_equipo(codigo)
    print(f"Equipo seleccionado: {equipo['tipo']} {equipo['marca']} - "
          f"{equipo['usuario']}")

    problema = validar_problema()

    tipo = validar_tipo_mantenimiento()

    print("\nPrioridad")
    print("1. Baja")
    print("2. Media")
    print("3. Normal")
    print("4. Alta")
    print("5. Crítica")

    prioridad = validar_entero(
        "Seleccione prioridad: ",
        1,
        5
    )

    tiempo = validar_tiempo_estimado()

    print("\nResumen de la incidencia")
    print(f"Equipo    : {codigo}")
    print(f"Problema  : {problema}")
    print(f"Tipo      : {tipo}")
    print(f"Prioridad : {prioridad}")
    print(f"Tiempo    : {tiempo // 60} h {tiempo % 60} min")

    if not confirmar_accion("¿Confirmar registro de la incidencia?"):
        print("\nRegistro cancelado. No se guardó la incidencia.")
        return

    resultado = registrar_incidencia(
        codigo,
        problema,
        tipo,
        prioridad,
        tiempo
    )

    if resultado:
        print("\nIncidencia registrada correctamente.")
        print(f"ID asignado: {resultado['id']}")
    else:
        print("\nERROR: No se pudo registrar la incidencia.")


def mostrar_ayuda():
    print("\n")
    print("=" * 70)
    print("                         AYUDA")
    print("=" * 70)
    print("1. Registrar equipo: código numérico de hasta 5 dígitos.")
    print("2. Tipo, marca y usuario: letras, espacios y tildes; máximo 50.")
    print("3. Modelo: letras, números y espacios; máximo 50.")
    print("4. Registrar incidencia: primero seleccione un equipo existente.")
    print("5. Problema: entre 10 y 250 caracteres, con puntuación común.")
    print("6. Tiempo: indique horas y minutos. Ejemplo: 1 h y 30 min.")
    print("7. En los resúmenes, responda S para guardar o N para cancelar.")
    input("\nPresione ENTER para volver al menú...")


# BUSCAR EQUIPO


def menu_buscar():

    print("\n")
    print("=" * 50)
    print("               BUSCAR EQUIPO")
    print("=" * 50)

    codigo = input("Código del equipo: ")

    resultado = buscar_equipo(codigo)

    if resultado:

        print("\nEquipo encontrado:")

        print(f"ID      : {resultado['id']}")
        print(f"Código  : {resultado['codigo']}")
        print(f"Tipo    : {resultado['tipo']}")
        print(f"Marca   : {resultado['marca']}")
        print(f"Modelo  : {resultado['modelo']}")
        print(f"Usuario : {resultado['usuario']}")
        print(f"Estado  : {resultado['estado']}")

    else:

        print("\nEquipo no encontrado.")


# ORDENAR POR PRIORIDAD

def menu_ordenar_prioridad():

    resultado, tiempo = medir_ordenamiento()

    print("\n")
    print("=" * 80)
    print("          INCIDENCIAS ORDENADAS POR PRIORIDAD")
    print("=" * 80)

    mostrar_incidencias(resultado)

    print(
        f"\nTiempo de ejecución: "
        f"{tiempo:.8f} segundos"
    )


# ORDENAR POR TIEMPO

def menu_ordenar_tiempo():

    inicio = __import__("time").perf_counter()

    resultado = ordenar_por_tiempo(incidencias)

    fin = __import__("time").perf_counter()

    tiempo = fin - inicio

    print("\n")
    print("=" * 80)
    print("          INCIDENCIAS ORDENADAS POR TIEMPO")
    print("=" * 80)

    mostrar_incidencias(resultado)

    print(
        f"\nTiempo de ejecución: "
        f"{tiempo:.8f} segundos"
    )


# PLANIFICAR

def menu_planificar():

    resultado = planificar_mantenimiento()

    print("\n")
    print("=" * 80)
    print("             PLANIFICACIÓN DE MANTENIMIENTO")
    print("=" * 80)

    if len(resultado) == 0:

        print("\nNo existen incidencias pendientes.")

        return

    print("\nOrden recomendado de atención:\n")

    posicion = 1

    for incidencia in resultado:

        print(
            f"{posicion}. "
            f"Equipo: {incidencia['codigo_equipo']} | "
            f"Problema: {incidencia['problema']} | "
            f"Prioridad: {incidencia['prioridad']} | "
            f"Tiempo: {incidencia['tiempo_estimado']} min"
        )

        posicion += 1


# ACTUALIZAR ESTADO

def menu_actualizar_estado():
    print("\n")
    print("=" * 50)
    print("             ACTUALIZAR ESTADO")
    print("=" * 50)

    id_incidencia = validar_entero(
        "ID de incidencia: ",
        1
    )

    incidencia = buscar_incidencia(id_incidencia)

    if incidencia is None:
        print(
            f"\nERROR: No existe una incidencia con ID "
            f"{id_incidencia}."
        )
        return

    nuevo_estado = validar_estado()

    resultado = actualizar_estado(
        id_incidencia,
        nuevo_estado
    )

    if resultado:
        print("\nEstado actualizado correctamente.")
        print(f"Nuevo estado: {nuevo_estado}")
    else:
        print("\nERROR: No se pudo actualizar el estado.")


# ESTADISTICAS

def menu_estadisticas():

    datos = obtener_estadisticas()

    print("\n")
    print("=" * 60)
    print("                  ESTADÍSTICAS")
    print("=" * 60)

    print(f"""
Total de equipos       : {datos['total_equipos']}
Total de incidencias   : {datos['total_incidencias']}

Pendientes             : {datos['pendientes']}
En proceso             : {datos['proceso']}
Finalizadas            : {datos['finalizadas']}

Preventivo             : {datos['preventivo']}
Correctivo             : {datos['correctivo']}
Predictivo             : {datos['predictivo']}

Tiempo total           : {datos['tiempo_total']} minutos
Tiempo promedio        : {datos['promedio']:.2f} minutos
""")


# DEMOSTRACION

def menu_demostracion():

    resultado = demostracion_algoritmos()

    original = resultado[0]
    ascendente = resultado[1]
    tiempo_ascendente = resultado[2]
    descendente = resultado[3]
    tiempo_descendente = resultado[4]

    print("\n")
    print("=" * 70)
    print("              DEMOSTRACIÓN DE ALGORITMOS")
    print("=" * 70)

    print("\nLista original:")
    print(original)

    print("\nOrdenamiento ascendente:")
    print(ascendente)

    print(
        f"Tiempo: {tiempo_ascendente:.8f} segundos"
    )

    print("\nOrdenamiento descendente:")
    print(descendente)

    print(
        f"Tiempo: {tiempo_descendente:.8f} segundos"
    )


# MENU PRINCIPAL

def menu():

    while True:

        print("\n\n")

        print("=" * 70)
        print("       SISTEMA DE MANTENIMIENTO DE EQUIPOS INFORMÁTICOS")
        print("=" * 70)

        print("""
1. Registrar equipo
2. Registrar incidencia
3. Mostrar equipos
4. Mostrar incidencias
5. Buscar equipo
6. Ordenar incidencias por prioridad
7. Ordenar incidencias por tiempo
8. Planificar mantenimiento
9. Actualizar estado
10. Mostrar estadísticas
11. Demostración de algoritmos
H. Ayuda
0. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":

            menu_registrar_equipo()

        elif opcion == "2":

            menu_registrar_incidencia()

        elif opcion == "3":

            mostrar_equipos()

        elif opcion == "4":

            mostrar_incidencias()

        elif opcion == "5":

            menu_buscar()

        elif opcion == "6":

            menu_ordenar_prioridad()

        elif opcion == "7":

            menu_ordenar_tiempo()

        elif opcion == "8":

            menu_planificar()

        elif opcion == "9":

            menu_actualizar_estado()

        elif opcion == "10":

            menu_estadisticas()

        elif opcion == "11":

            menu_demostracion()

        elif opcion.upper() == "H":

            mostrar_ayuda()

        elif opcion == "0":

            print("\nSistema finalizado.")

            break

        else:

            print(
            "\nERROR: Opción inválida. "
            "Debe seleccionar una opción del 0 al 11."
            )


# EJECUTAR

if __name__ == "__main__":

    menu()