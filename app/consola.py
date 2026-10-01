"""
Created on Tue Sep  8 21:08:08 2026

@author: MAZAG
"""

import time

from core.metodos import *
from interfaz.graficos import (
    mostrar_graficos_backtracking,
    mostrar_graficos_planificacion,
)

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
Detalle de mantenimiento:
{chr(10).join(f"  {registro['estado']}: {registro['detalle']}" for registro in incidencia.get('historial_mantenimiento', [])) or '  Sin detalle registrado.'}
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

    sku = validar_sku_equipo(solo_sin_incidencia_abierta=True)

    # Búsqueda binaria confirma el equipo dentro de la lista ordenada por SKU.
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

    print("Pasos de la búsqueda binaria:")
    print("1. Los equipos están ordenados por SKU.")
    print("2. Se revisa el SKU que queda en el centro.")
    print("3. Se conserva solo la mitad donde podría estar el equipo.")
    print("4. Se repite hasta encontrarlo o quedarse sin opciones.")

    sku = validar_sku_busqueda()

    # Búsqueda binaria se invoca a través de buscar_equipo.
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

    # Bubble Sort ordena las incidencias de prioridad más alta a más baja.
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
PASOS DE BUBBLE SORT

1. Se comparan dos incidencias vecinas.
2. Si la de la izquierda tiene menor prioridad, se intercambian.
3. Se repite el recorrido hasta que ya no haya cambios.

Orden utilizado: prioridad más alta primero.
""")



def menu_ordenar_tiempo():

    inicio = time.perf_counter()

    # Bubble Sort ordena el tiempo estimado de menor a mayor.
    resultado = ordenar_por_tiempo(
        incidencias
    )

    fin = time.perf_counter()

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
PASOS DE BUBBLE SORT

1. Se comparan los minutos de dos incidencias vecinas.
2. Si la primera tarda más, se intercambian.
3. Se repite hasta que el menor tiempo quede primero.

Orden utilizado: menor tiempo primero.
""")



def menu_planificar():

    # El algoritmo voraz elige sucesivamente la mejor incidencia pendiente.
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
PASOS DEL ALGORITMO VORAZ

1. Se consideran solo las incidencias pendientes.
2. Se elige la de mayor prioridad disponible.
3. Si empatan, se elige la de menor duración y luego el menor ID.
4. Se repite con las incidencias restantes.

Es una regla práctica de atención; no promete el mejor resultado
posible para todos los escenarios.
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

    textos_apoyo = {
        "Pendiente": "El equipo está en cola. Al iniciar, describa la revisión o tarea realizada.",
        "En proceso": "El mantenimiento ya inició. Al finalizar, indique las tareas y el resultado.",
        "Finalizado": "La incidencia está cerrada y no admite retrocesos."
    }
    print(f"\n{textos_apoyo[incidencia['estado']]}")

    nuevo_estado = validar_estado(incidencia["estado"])
    if nuevo_estado is None:
        print("\nLa incidencia ya está finalizada.")
        return

    detalle = validar_detalle_mantenimiento()

    resultado = actualizar_estado(
        id_incidencia,
        nuevo_estado,
        detalle
    )

    if resultado:

        print(
            "\n✓ Estado actualizado correctamente."
        )

        print(
            f"Nuevo estado: {nuevo_estado}"
        )
        print(f"Detalle registrado: {detalle}")

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

    # Presenta resultados de las invocaciones de los tres algoritmos.
    resultado = demostracion_algoritmos()

    print("\n")
    print("=" * 80)
    print(
        "                    DEMOSTRACIÓN DE ALGORITMOS"
    )
    print("=" * 80)

    print("""
ALGORITMO 1: BUBBLE SORT (ORDENAMIENTO BURBUJA)
1. Se parte de una lista de números.
2. Se comparan dos números vecinos.
3. Si están en el orden equivocado, se cambian de lugar.
4. Se repite hasta que toda la lista queda ordenada.
""")
    print("Lista original:", resultado["numeros_originales"])
    print("De menor a mayor:", resultado["numeros_ascendentes"])
    print("De mayor a menor:", resultado["numeros_descendentes"])
    print(f"Tiempo ascendente: {resultado['tiempo_ascendente']:.8f} segundos")
    print(f"Tiempo descendente: {resultado['tiempo_descendente']:.8f} segundos")

    print("""
ALGORITMO 2: BÚSQUEDA BINARIA
1. La lista de equipos debe estar ordenada por SKU.
2. Se revisa el SKU que queda en el centro.
3. Se descarta la mitad donde no puede estar el buscado.
4. Se repite hasta encontrarlo o terminar la lista.
""")
    print(f"SKU buscado: {resultado['sku_demo']}")
    print(f"SKU revisados: {resultado['recorrido_busqueda']}")
    if resultado["equipo_encontrado"]:
        print(
            "Resultado: equipo encontrado, "
            f"{resultado['equipo_encontrado']['sku']}."
        )
    else:
        print("Resultado: no se encontró el equipo.")

    print("""
ALGORITMO 3: MÉTODO VORAZ
1. Se toman las incidencias pendientes.
2. Se elige la de mayor prioridad disponible.
3. En empate, gana la de menor duración y luego el menor ID.
4. Se repite hasta completar el orden de atención.
""")
    if resultado["plan_voraz"]:
        for posicion, incidencia in enumerate(resultado["plan_voraz"], 1):
            print(
                f"{posicion}. ID {incidencia['id']} | "
                f"prioridad {incidencia['prioridad']} | "
                f"{incidencia['tiempo_estimado']} min"
            )
    else:
        print("No hay incidencias pendientes para planificar.")

    print("""
Estos algoritmos apoyan la búsqueda de equipos, el orden de incidencias
y la propuesta de atención. Cada uno elige o compara datos de una forma
distinta, explicada paso a paso arriba.
""")

    print("COMPARACIÓN DE TIEMPOS DE EJECUCIÓN")
    print(
        f"Promedio de {resultado['repeticiones_comparacion']} repeticiones "
        f"con {resultado['elementos_comparacion']} elementos:"
    )

    for nombre, tiempo in resultado["tiempos_comparacion"].items():
        print(f"- {nombre}: {tiempo:.3f} microsegundos por ejecución")

    print("""
La comparación es orientativa: cada algoritmo realiza una tarea distinta.
Los tiempos pueden variar según el equipo y no demuestran por sí solos
que un algoritmo sea mejor que otro.
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


def _distribucion_prioridades(lista):
    etiquetas = {
        1: "Baja",
        2: "Media",
        3: "Normal",
        4: "Alta",
        5: "Crítica",
    }
    cantidades = {prioridad: 0 for prioridad in etiquetas}
    for incidencia in lista:
        prioridad = incidencia["prioridad"]
        if prioridad in cantidades:
            cantidades[prioridad] += 1
    return ", ".join(
        f"{etiquetas[prioridad]}: {cantidad}"
        for prioridad, cantidad in cantidades.items()
    )


def menu_planificar_graficos():
    print("\nPLANIFICAR MANTENIMIENTO CON ALGORITMO VORAZ")
    print("Prioridad mayor primero; en empate, menor duración e ID.")
    tiempo_disponible = validar_entero(
        "Tiempo disponible del técnico (minutos): ",
        1,
    )

    inicio = time.perf_counter()
    greedy = planificar_voraz_detallado(tiempo_disponible)
    menor_tiempo = planificar_voraz_detallado(
        tiempo_disponible,
        criterio="tiempo",
    )
    duracion_ejecucion = time.perf_counter() - inicio

    print("\nDECISIONES DEL ALGORITMO VORAZ")
    if not greedy["decisiones"]:
        print("No hay incidencias pendientes para planificar.")
    for decision in greedy["decisiones"]:
        incidencia = decision["incidencia"]
        resultado = "SELECCIONADA" if decision["seleccionada"] else "DESCARTADA"
        print(
            f"ID {incidencia['id']} | {incidencia['sku_equipo']} | "
            f"prioridad {incidencia['prioridad']} | "
            f"{incidencia['tiempo_estimado']} min | {resultado}"
        )
        print(f"  Motivo: {decision['motivo']}")

    print("\nORDEN DE ATENCIÓN SELECCIONADO")
    if greedy["seleccionadas"]:
        for posicion, incidencia in enumerate(greedy["seleccionadas"], 1):
            print(
                f"{posicion}. ID {incidencia['id']} | "
                f"{incidencia['sku_equipo']} | {incidencia['problema']} | "
                f"prioridad {incidencia['prioridad']} | "
                f"{incidencia['tiempo_estimado']} min"
            )
    else:
        print("Ninguna incidencia cabe dentro del tiempo disponible.")

    print("\nINCIDENCIAS DESCARTADAS")
    if greedy["descartadas"]:
        for incidencia in greedy["descartadas"]:
            decision = next(
                dato for dato in greedy["decisiones"]
                if dato["incidencia"]["id"] == incidencia["id"]
            )
            print(
                f"ID {incidencia['id']} | {incidencia['sku_equipo']} | "
                f"{incidencia['tiempo_estimado']} min: {decision['motivo']}"
            )
    else:
        print("Ninguna; todas las incidencias pendientes fueron seleccionadas.")

    print("\nRESUMEN DE TIEMPO (mantenimiento, minutos)")
    print(f"Disponible: {greedy['tiempo_disponible']}")
    print(f"Utilizado:  {greedy['tiempo_usado']}")
    print(f"Restante:   {greedy['tiempo_restante']}")
    print(
        f"Ejecución de los algoritmos: {duracion_ejecucion:.8f} segundos "
        "(no es tiempo de mantenimiento)."
    )

    print("\nCOMPARACIÓN DE ESTRATEGIAS")
    for nombre, resultado in (
        ("Prioridad y duración", greedy),
        ("Menor duración primero", menor_tiempo),
    ):
        print(
            f"{nombre}: {len(resultado['seleccionadas'])} seleccionadas, "
            f"{resultado['tiempo_usado']} min usados, "
            f"{resultado['tiempo_restante']} min restantes."
        )
        print(
            "  Prioridades seleccionadas: "
            f"{_distribucion_prioridades(resultado['seleccionadas'])}"
        )

    try:
        mostrar_graficos_planificacion(greedy, menor_tiempo)
    except ImportError:
        print(
            "\nNo se encontró Matplotlib. Instala la dependencia con "
            "'python -m pip install -r requirements.txt'."
        )


def menu_backtracking():
    print("\nPLANIFICAR MANTENIMIENTO CON BACKTRACKING")
    print(
        "Objetivo lexicográfico: más incidencias, mayor prioridad total "
        "(1-5) y menor tiempo total."
    )
    tiempo_disponible = validar_entero(
        "Tiempo disponible del técnico (minutos): ",
        0,
    )

    inicio = time.perf_counter()
    resultado = planificar_backtracking_detallado(tiempo_disponible)
    tiempo_backtracking = time.perf_counter() - inicio
    inicio = time.perf_counter()
    voraz = planificar_voraz_detallado(
        tiempo_disponible,
        pendientes=resultado["incidencias_pendientes"],
    )
    tiempo_voraz = time.perf_counter() - inicio

    print("\nINCIDENCIAS SELECCIONADAS")
    if resultado["seleccionadas"]:
        for posicion, incidencia in enumerate(resultado["seleccionadas"], 1):
            print(
                f"{posicion}. ID {incidencia['id']} | "
                f"{incidencia.get('sku_equipo', 'Sin SKU')} | "
                f"{incidencia.get('problema', 'Sin descripción')} | "
                f"Prioridad {incidencia['prioridad']} | "
                f"{incidencia['tiempo_estimado']} min"
            )
    else:
        print("Ninguna incidencia seleccionada.")

    print("\nINCIDENCIAS NO SELECCIONADAS")
    if resultado["no_seleccionadas"]:
        for incidencia in resultado["no_seleccionadas"]:
            print(
                f"ID {incidencia['id']} | "
                f"{incidencia.get('sku_equipo', 'Sin SKU')} | "
                f"Prioridad {incidencia['prioridad']} | "
                f"{incidencia['tiempo_estimado']} min"
            )
    else:
        print("Ninguna.")

    print("\nCOMPARACIÓN DE ESTRATEGIAS")
    print(
        f"{'Método':<22} {'Cantidad':>8} {'Prioridad':>10} "
        f"{'Usado':>8} {'Restante':>9} {'Ejecución':>14}"
    )
    for nombre, plan, duracion in (
        ("Backtracking", resultado, tiempo_backtracking),
        ("Greedy", voraz, tiempo_voraz),
    ):
        seleccionadas = plan["seleccionadas"]
        prioridad_total = sum(item["prioridad"] for item in seleccionadas)
        print(
            f"{nombre:<22} {len(seleccionadas):>8} "
            f"{prioridad_total:>10} {plan['tiempo_usado']:>8} "
            f"{tiempo_disponible - plan['tiempo_usado']:>9} "
            f"{duracion:>11.8f} s"
        )
        print(f"  Prioridades: {_distribucion_prioridades(seleccionadas)}")

    print(
        f"\nNodos: {resultado['nodos_explorados']} | "
        f"Soluciones evaluadas: {resultado['soluciones_evaluadas']} | "
        f"Retrocesos: {resultado['retrocesos']} | "
        f"Ramas podadas: {resultado['ramas_podadas']} "
        f"(por tiempo: {resultado['podas_por_tiempo']}, "
        f"por cota: {resultado['podas_por_cota']})"
    )
    print(
        "Prioridad total = suma directa de los valores existentes: "
        "1 (Baja) a 5 (Crítica)."
    )
    print(
        "Peor caso: O(2^n) tiempo y O(n) de pila recursiva; la poda puede "
        "reducir nodos en esta ejecución, pero no cambia el peor caso."
    )

    if resultado["historial"] and confirmar_accion(
        "¿Consultar una muestra del historial de decisiones?"
    ):
        limite = min(60, len(resultado["historial"]))
        cantidad = validar_entero(
            f"Cantidad de eventos a mostrar (1-{limite}): ",
            1,
            limite,
        )
        for evento in resultado["historial"][:cantidad]:
            if evento["tipo"] == "nodo":
                print(
                    f"Nodo {evento['nodo']} | profundidad {evento['profundidad']} | "
                    f"{evento['decision']} | tiempo {evento['tiempo_acumulado']} | "
                    f"seleccionadas {evento['seleccionadas']} | mejor "
                    f"{evento['mejor_cantidad']}/{evento['mejor_prioridad']}/"
                    f"{evento['mejor_tiempo']}"
                    + (
                        f" | PODA: {evento.get('motivo_poda')}"
                        if evento.get("podada") else ""
                    )
                )
            else:
                print(
                    f"Retroceso en nodo {evento['nodo']} tras incidencia "
                    f"{evento['id_incidencia']}"
                )
        if resultado["historial_truncado"]:
            print(
                f"Historial limitado a {len(resultado['historial'])} eventos "
                f"de {resultado['eventos_totales']} generados."
            )

    if confirmar_accion("¿Mostrar los gráficos de esta ejecución?"):
        try:
            mostrar_graficos_backtracking(
                resultado,
                voraz,
                tiempo_backtracking,
                tiempo_voraz,
            )
        except ImportError:
            print(
                "No se encontró Matplotlib. Instala con "
                "'python -m pip install -r requirements.txt'."
            )

def mostrar_ayuda():

    print("""
AYUDA Y REGLAS DE INGRESO

EQUIPOS
- SKU: letras y números, de 1 a 20 caracteres, único.
- Tipo: de 3 a 50 letras; puede incluir espacios y guion.
- Marca: de 1 a 50 letras o números; puede incluir espacios, &, punto y guion.
- Modelo: de 1 a 50 letras o números; puede incluir espacios, punto, _, / y -.
- Usuario: de 3 a 50 caracteres, sin espacios; letras, números, ., _, @ y -.
- Identificación del equipo: de 3 a 50 letras o números; admite espacios y _ . / -.
- El equipo queda Operativo o En mantenimiento.

INCIDENCIAS
- Deben apuntar a un SKU existente sin otra incidencia abierta.
- El problema debe tener entre 10 y 250 caracteres.
- Mantenimiento: Preventivo, Correctivo o Predictivo.
- Prioridad: un número entero del 1 al 5.
- Tiempo: horas y minutos; los minutos van de 0 a 59 y el total debe ser mayor que cero.
- Estado: Pendiente, En proceso o Finalizado.
""")
    leer_input("\nPresione ENTER para volver al menú")


def ejecutar_accion(accion):

    try:
        accion()
    except CancelarFlujo:
        print("\nOperación cancelada. Volviendo al menú principal.")



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
            14. Planificar mantenimiento con Backtracking
            15. Planificar mantenimiento con algoritmo voraz
            H. Ayuda
            0. Salir
        """)

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "1":

            ejecutar_accion(menu_registrar_equipo)

        elif opcion == "2":

            ejecutar_accion(menu_registrar_incidencia)

        elif opcion == "3":

            ejecutar_accion(mostrar_equipos)

        elif opcion == "4":

            ejecutar_accion(mostrar_incidencias)

        elif opcion == "5":

            ejecutar_accion(menu_buscar)

        elif opcion == "6":

            ejecutar_accion(menu_ordenar_prioridad)

        elif opcion == "7":

            ejecutar_accion(menu_ordenar_tiempo)

        elif opcion == "8":

            ejecutar_accion(menu_planificar)

        elif opcion == "9":

            ejecutar_accion(menu_actualizar_estado)

        elif opcion == "10":

            ejecutar_accion(menu_estadisticas)

        elif opcion == "11":

            ejecutar_accion(menu_demostracion)

        elif opcion == "12":
        
            menu_recursivo()
        
        elif opcion == "13":
        
            menu_voraz()
        
        elif opcion == "14":
        
            menu_backtracking()

        elif opcion == "15":

            ejecutar_accion(menu_planificar_graficos)

        elif opcion.upper() == "H":

            ejecutar_accion(mostrar_ayuda)

        elif opcion == "0":

            print("\nSistema finalizado." )

            break

        else:
            print("\nALERTA: Opción inválida." )
            print("Seleccione una opción del 0 al 15 o H para ayuda.")

if __name__ == "__main__":

    menu()