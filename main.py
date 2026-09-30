"""
Created on Tue Sep  8 21:08:08 2026

@author: MAZAG
"""

from metodos import *

def mostrar_equipos():

    print("\n")
    print("=" * 80)
    print("LISTA DE EQUIPOS")
    print("=" * 80)

    if not equipos:

        print(
            "\nNo existen equipos registrados."
        )

        return

    for equipo in equipos:

        print(f"""
ID       : {equipo['id']}
SKU      : {equipo['sku']}
Tipo     : {equipo['tipo']}
Marca    : {equipo['marca']}
Modelo   : {equipo['modelo']}
Usuario  : {equipo['usuario']}
Equipo   : {equipo['equipo']}
Estado   : {equipo['estado']}
----------------------------------------
""")


def mostrar_incidencias(lista=None):

    if lista is None:

        lista = incidencias

    print("\n")
    print("=" * 100)
    print("                           INCIDENCIAS")
    print("=" * 100)

    if not lista:

        print(
            "\nNo existen incidencias registradas."
        )

        return

    for incidencia in lista:

        print(f"""
ID                  : {incidencia['id']}
SKU del equipo      : {incidencia['sku_equipo']}
Problema            : {incidencia['problema']}
Tipo mantenimiento  : {incidencia['tipo_mantenimiento']}
Prioridad           : {incidencia['prioridad']}
Tiempo estimado     : {incidencia['tiempo_estimado']} minutos
Estado              : {incidencia['estado']}
----------------------------------------
""")

def menu_registrar_equipo():

    print("\n")
    print("=" * 70)
    print("                         REGISTRAR EQUIPO")
    print("=" * 70)
    
    sku = validar_sku_nuevo()
    tipo = validar_texto_equipo("Tipo: ", "tipo" )
    marca = validar_texto_equipo( "Marca: ", "marca")
    modelo = validar_modelo()
    usuario = validar_usuario()
    equipo = validar_texto_equipo("Equipo: ","equipo")

    print("\n")
    print("=" * 70)
    print("                         RESUMEN DEL EQUIPO")
    print("=" * 70)

    print(f"""
SKU      : {sku}
Tipo     : {tipo}
Marca    : {marca}
Modelo   : {modelo}
Usuario  : {usuario}
Equipo   : {equipo}
Estado   : Operativo
""")

    if not confirmar_accion("¿Confirmar registro del equipo?" ):
        print("\nRegistro cancelado.")

        print("No se guardó el equipo.")

        return

    resultado = registrar_equipo(
        sku,
        tipo,
        marca,
        modelo,
        usuario,
        equipo
    )

    if resultado:

        print(
            "\n✓ Equipo registrado correctamente."
        )

        print(
            f"ID asignado: {resultado['id']}"
        )

    else:

        print(
            "\nERROR: No se pudo registrar "
            "el equipo."
        )

def menu_registrar_incidencia():

    print("\n")
    print("=" * 70)
    print("                       REGISTRAR INCIDENCIA")
    print("=" * 70)

    print("""
ANTES DE COMENZAR

Para registrar una incidencia:

1. Debe seleccionar un SKU existente.
2. Describa el problema.
3. Seleccione el mantenimiento.
4. Seleccione la prioridad.
5. Indique el tiempo estimado.
6. Confirme el registro.
""")

    sku = validar_sku_equipo()

    equipo = buscar_equipo(sku)

    print("\n✓ EQUIPO SELECCIONADO")

    print(
        f"SKU     : {equipo['sku']}"
    )

    print(
        f"Tipo    : {equipo['tipo']}"
    )

    print(
        f"Marca   : {equipo['marca']}"
    )

    print(
        f"Modelo  : {equipo['modelo']}"
    )

    print(
        f"Usuario : {equipo['usuario']}"
    )

    
    problema = validar_problema()

    
    tipo = validar_tipo_mantenimiento()

    
    print("\n")
    print(
        "¿Qué debe ingresar en Prioridad?"
    )

    print(
        "Seleccione una opción:"
    )

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

    
    print("\n")
    print("=" * 70)
    print("                    RESUMEN DE LA INCIDENCIA")
    print("=" * 70)

    print(f"""
SKU equipo : {sku}
Problema   : {problema}
Tipo       : {tipo}
Prioridad  : {prioridad}
Tiempo     : {tiempo // 60} h {tiempo % 60} min
Estado     : Pendiente
""")

    if not confirmar_accion(
        "¿Confirmar registro de la incidencia?"
    ):

        print(
            "\nRegistro cancelado."
        )

        print(
            "No se guardó la incidencia."
        )

        return

    resultado = registrar_incidencia(
        sku,
        problema,
        tipo,
        prioridad,
        tiempo
    )

    if resultado:

        print(
            "\n✓ Incidencia registrada correctamente."
        )

        print(
            f"ID asignado: {resultado['id']}"
        )

    else:

        print(
            "\nERROR: No se pudo registrar "
            "la incidencia."
        )



def menu_buscar():

    print("\n")
    print("=" * 60)
    print("                         BUSCAR EQUIPO")
    print("=" * 60)

    print("""
Ingrese el SKU del equipo que desea buscar.

Ejemplo:
PC1001
""")

    sku = input(
        "SKU: "
    ).strip().upper()

    resultado = buscar_equipo(sku)

    if resultado:

        print("\n✓ Equipo encontrado:")

        print(
            f"ID      : {resultado['id']}"
        )

        print(
            f"SKU     : {resultado['sku']}"
        )

        print(
            f"Tipo    : {resultado['tipo']}"
        )

        print(
            f"Marca   : {resultado['marca']}"
        )

        print(
            f"Modelo  : {resultado['modelo']}"
        )

        print(
            f"Usuario : {resultado['usuario']}"
        )

        print(
            f"Equipo  : {resultado['equipo']}"
        )

        print(
            f"Estado  : {resultado['estado']}"
        )

    else:

        print(
            f"\nALERTA: No existe un equipo "
            f"con SKU '{sku}'."
        )



def menu_ordenar_prioridad():

    resultado, tiempo = medir_ordenamiento()

    print("\n")
    print("=" * 80)
    print(
        "          INCIDENCIAS ORDENADAS POR PRIORIDAD"
    )
    print("=" * 80)

    mostrar_incidencias(resultado)

    print(
        f"\nTiempo de ejecución: "
        f"{tiempo:.8f} segundos"
    )

    print("""
MÉTODO UTILIZADO

Ordenamiento Burbuja (Bubble Sort).

El algoritmo:
1. Compara elementos consecutivos.
2. Compara sus prioridades.
3. Intercambia los elementos cuando corresponde.
4. Repite el proceso hasta ordenar la lista.

Orden utilizado: descendente.
""")



def menu_ordenar_tiempo():

    inicio = __import__(
        "time"
    ).perf_counter()

    resultado = ordenar_por_tiempo(
        incidencias
    )

    fin = __import__(
        "time"
    ).perf_counter()

    tiempo = fin - inicio

    print("\n")
    print("=" * 80)
    print(
        "             INCIDENCIAS ORDENADAS POR TIEMPO"
    )
    print("=" * 80)

    mostrar_incidencias(resultado)

    print(
        f"\nTiempo de ejecución: "
        f"{tiempo:.8f} segundos"
    )

    print("""
MÉTODO UTILIZADO

Ordenamiento Burbuja (Bubble Sort).

Se comparan los tiempos estimados
de dos incidencias consecutivas.

Orden utilizado: ascendente.
""")



def menu_planificar():

    resultado = planificar_mantenimiento()

    print("\n")
    print("=" * 80)
    print(
        "                  PLANIFICACIÓN DE MANTENIMIENTO"
    )
    print("=" * 80)

    if len(resultado) == 0:

        print(
            "\nNo existen incidencias pendientes."
        )

        return

    print(
        "\nOrden de atención:\n"
    )

    posicion = 1

    for incidencia in resultado:

        print(
            f"{posicion}. "
            f"SKU: {incidencia['sku_equipo']} | "
            f"Problema: {incidencia['problema']} | "
            f"Prioridad: {incidencia['prioridad']} | "
            f"Tiempo: {incidencia['tiempo_estimado']} min"
        )

        posicion += 1

    print("""
MÉTODO UTILIZADO

1. Se filtran las incidencias pendientes.
2. Se aplica Ordenamiento Burbuja.
3. Se ordenan por prioridad descendente.
""")



def menu_actualizar_estado():

    print("\n")
    print("=" * 60)
    print("                    ACTUALIZAR ESTADO")
    print("=" * 60)

    id_incidencia = validar_entero(
        "ID de incidencia: ",
        1
    )

    incidencia = buscar_incidencia(
        id_incidencia
    )

    if incidencia is None:

        print(
            f"\nALERTA: No existe una incidencia "
            f"con ID {id_incidencia}."
        )

        return

    print(
        f"\nEstado actual: "
        f"{incidencia['estado']}"
    )

    nuevo_estado = validar_estado()

    resultado = actualizar_estado(
        id_incidencia,
        nuevo_estado
    )

    if resultado:

        print(
            "\n✓ Estado actualizado correctamente."
        )

        print(
            f"Nuevo estado: {nuevo_estado}"
        )

    else:

        print(
            "\nERROR: No se pudo actualizar "
            "el estado."
        )



def menu_estadisticas():

    datos = obtener_estadisticas()

    print("\n")
    print("=" * 70)
    print("                         ESTADÍSTICAS")
    print("=" * 70)

    print(
        f"""
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
        """
    )

    print("""
    MÉTODOS UTILIZADOS

    - Recorrido secuencial de listas.
    - Conteo de registros.
    - Conteo por estado.
    - Conteo por tipo de mantenimiento.
    - Acumulación del tiempo.
    - Cálculo del promedio.
    """)



def menu_demostracion():

    resultado = demostracion_algoritmos()

    original = resultado[0]
    ascendente = resultado[1]
    tiempo_ascendente = resultado[2]
    descendente = resultado[3]
    tiempo_descendente = resultado[4]

    print("\n")
    print("=" * 80)
    print(
        "                    DEMOSTRACIÓN DE ALGORITMOS"
    )
    print("=" * 80)

    print("""
        ALGORITMO UTILIZADO
        ===================

        ORDENAMIENTO BURBUJA
        (BUBBLE SORT)

        El algoritmo compara elementos consecutivos
        y los intercambia cuando están en un orden
        incorrecto.

        Este proceso se repite hasta ordenar
        completamente la lista.
        """)

    print(
        "\nLista original:"
    )

    print(
        original
    )

    print(
        "\nLista ordenada ascendentemente:"
    )

    print(
        ascendente
    )

    print(f"\nTiempo ascendente: "
        f"{tiempo_ascendente:.8f} segundos")

    print("\nLista ordenada descendentemente:")

    print(descendente)

    print(f"\nTiempo descendente: "
        f"{tiempo_descendente:.8f} segundos"
    )

    print("""
        ================================================
        MÉTODOS UTILIZADOS EN EL SISTEMA
        ================================================

        1. BÚSQUEDA SECUENCIAL
        Se utiliza para buscar equipos e incidencias.

        2. ORDENAMIENTO BURBUJA
        Se utiliza para ordenar incidencias
        por prioridad y tiempo.

        3. RECORRIDO DE LISTAS
        Se utiliza para mostrar registros
        y generar estadísticas.

        4. VALIDACIÓN DE DATOS
        Controla los datos ingresados por el usuario.

        5. MEDICIÓN DE TIEMPO
        Se utiliza time.perf_counter()
        para medir la ejecución de los algoritmos.
    """)


def menu_recursivo():

    print("\n")
    print("=" * 80)
    print("                 ALGORITMO RECURSIVO")
    print("=" * 80)

    cantidad = contar_pendientes_recursivo(incidencias)

    print(
        f"\nCantidad de incidencias pendientes: {cantidad}"
    )

    print("""
MÉTODO UTILIZADO

Se utiliza recursividad para recorrer las incidencias.""")


def menu_voraz():

    print("\n")
    print("=" * 80)
    print("                  ALGORITMO VORAZ")
    print("=" * 80)

    print("""
El algoritmo seleccionará las incidencias
de mayor prioridad primero.

Debe indicar el tiempo disponible
para realizar los mantenimientos.
""")

    tiempo_disponible = validar_entero("Tiempo disponible en minutos: ", 1)

    resultado, tiempo_usado = planificar_voraz(tiempo_disponible)

    print("\n")
    print("=" * 80)
    print("              PLANIFICACIÓN VORAZ")
    print("=" * 80)

    if not resultado:

        print(
            "\nNo se encontraron incidencias "
            "que puedan ser atendidas."
        )

    else:

        posicion = 1

        for incidencia in resultado:

            print(
                f"\n{posicion}. "
                f"SKU: {incidencia['sku_equipo']}"
            )

            print(
                f"   Problema: {incidencia['problema']}"
            )

            print(
                f"   Prioridad: {incidencia['prioridad']}"
            )

            print(
                f"   Tiempo: "
                f"{incidencia['tiempo_estimado']} minutos"
            )

            posicion += 1

        print(
            f"\nTiempo utilizado: "
            f"{tiempo_usado} minutos"
        )

        print(
            f"Tiempo disponible: "
            f"{tiempo_disponible} minutos"
        )


def menu_backtracking():

    print("\n")
    print("=" * 80)
    print("                 ALGORITMO BACKTRACKING")
    print("=" * 80)

    print("""
El algoritmo buscará la mejor combinación
de incidencias sin superar el tiempo disponible.

A diferencia del algoritmo voraz,
Backtracking analiza diferentes combinaciones.
""")

    tiempo_disponible = validar_entero("Tiempo disponible en minutos: ",1)

    resultado, tiempo_usado, prioridad_total = (planificar_backtracking(tiempo_disponible))

    print("\n")
    print("=" * 80)
    print("             PLANIFICACIÓN BACKTRACKING")
    print("=" * 80)

    if not resultado:

        print(
            "\nNo se encontraron incidencias "
            "para la planificación."
        )

    else:

        posicion = 1

        for incidencia in resultado:

            print(
                f"\n{posicion}. "
                f"SKU: {incidencia['sku_equipo']}"
            )

            print(
                f"   Problema: {incidencia['problema']}"
            )

            print(
                f"   Prioridad: {incidencia['prioridad']}"
            )

            print(
                f"   Tiempo: "
                f"{incidencia['tiempo_estimado']} minutos"
            )

            posicion += 1

        print(
            f"\nTiempo utilizado: "
            f"{tiempo_usado} minutos"
        )

        print(
            f"Prioridad acumulada: "
            f"{prioridad_total}"
        )

        print(
            f"Tiempo disponible: "
            f"{tiempo_disponible} minutos"
        )

def mostrar_ayuda():

    print("\n")
    print("=" * 80)
    print("                              AYUDA")
    print("=" * 80)

    print("""
REGISTRO DE EQUIPOS
===================
SKU:
- Letras y números.
- Sin espacios.
- Sin guiones.
- Sin tildes.
- Sin caracteres especiales.
- Debe ser único.
Ejemplo:
PC1001
TIPO:
- Campo obligatorio.
- No puede estar vacío.
MARCA:
- Campo obligatorio.
- No puede estar vacío.
MODELO:
- Letras y números.
- Sin espacios.
- Sin caracteres especiales.
USUARIO:
- Letras.
- Números.
- Caracteres especiales.
- Sin espacios.
EQUIPO:
- Identificación o descripción del equipo.
ESTADO DEL EQUIPO:
- Operativo.
- Inoperativo.
REGISTRO DE INCIDENCIAS
=======================
SKU DEL EQUIPO:
- Debe corresponder a un equipo existente.

PROBLEMA:
- Mínimo 10 caracteres.
- Máximo 250 caracteres.

TIPO DE MANTENIMIENTO:
- Preventivo.
- Correctivo.
- Predictivo.

PRIORIDAD:
    1. Baja
    2. Media
    3. Normal
    4. Alta
    5. Crítica


    ESTADO DE INCIDENCIA:
    1. Pendiente
    2. En proceso
    3. Finalizado
    """)
    input("\nPresione ENTER para volver al menú...")



def menu():

    while True:
        print("\n\n")
        print("=" * 80)
        print("SISTEMA DE MANTENIMIENTO DE EQUIPOS INFORMÁTICOS")
        print("=" * 80)
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
            12. Algoritmo recursivo
            13. Algoritmo voraz
            14. Algoritmo Backtracking
            H. Ayuda
            0. Salir
        """)

        opcion = input(
            "Seleccione una opción: "
        ).strip()

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

        elif opcion == "12":
        
            menu_recursivo()
        
        elif opcion == "13":
        
            menu_voraz()
        
        elif opcion == "14":
        
            menu_backtracking()

        elif opcion.upper() == "H":

            mostrar_ayuda()

        elif opcion == "0":

            print("\nSistema finalizado." )

            break

        else:
            print("\nALERTA: Opción inválida." )
            print("Seleccione una opción del 0 al 11 o H para ayuda.")

if __name__ == "__main__":

    menu()