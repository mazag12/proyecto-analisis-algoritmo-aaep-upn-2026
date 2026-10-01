"""
Created on Tue Sep  8 21:07:30 2026

@author: MAZAG
"""
import time
from algoritmos.algoritmo_voraz import planificar_por_prioridad
from algoritmos.busqueda_binaria import buscar_sku_ordenado
from algoritmos.ordenamiento_burbuja import (
    ordenar_equipos_por_sku,
    ordenar_numeros,
    ordenar_prioridad_descendente,
    ordenar_tiempo_ascendente,
)


class CancelarFlujo(Exception):
    """Indica que el usuario desea abandonar la operación actual."""


def leer_input(mensaje=""):
    etiqueta = mensaje.rstrip()
    if etiqueta.endswith(":"):
        etiqueta = etiqueta[:-1]
    prompt = f"{etiqueta} [C=cancelar]: " if etiqueta else "[C=cancelar]: "
    respuesta = input(prompt)

    if respuesta.strip().upper() in ("C", "CANCELAR", "VOLVER"):
        raise CancelarFlujo

    return respuesta


equipos = [
    {
        "id": 1,
        "sku": "PC1001",
        "tipo": "Computadora",
        "marca": "Lenovo",
        "modelo": "ThinkCentre",
        "usuario": "CarlosPerez",
        "equipo": "EquipoAdministrativo01",
        "estado": "Operativo"
    },
    {
        "id": 2,
        "sku": "LAP1002",
        "tipo": "Laptop",
        "marca": "HP",
        "modelo": "ProBook",
        "usuario": "MariaLopez",
        "equipo": "LaptopAdministrativa01",
        "estado": "Operativo"
    },
    {
        "id": 3,
        "sku": "PC1003",
        "tipo": "Computadora",
        "marca": "Dell",
        "modelo": "OptiPlex",
        "usuario": "JuanTorres",
        "equipo": "EquipoContabilidad01",
        "estado": "Operativo"
    },
    {
        "id": 4,
        "sku": "LAP1004",
        "tipo": "Laptop",
        "marca": "Lenovo",
        "modelo": "ThinkPad",
        "usuario": "AnaGarcia",
        "equipo": "LaptopRecursosHumanos01",
        "estado": "Operativo"
    },
    {
        "id": 5,
        "sku": "PC1005",
        "tipo": "Computadora",
        "marca": "HP",
        "modelo": "EliteDesk",
        "usuario": "PedroRamirez",
        "equipo": "EquipoVentas01",
        "estado": "Inoperativo"
    },
    {
        "id": 6,
        "sku": "LAP1006",
        "tipo": "Laptop",
        "marca": "Dell",
        "modelo": "Latitude",
        "usuario": "LuciaMendoza",
        "equipo": "LaptopGerencia01",
        "estado": "Operativo"
    },
    {
        "id": 7,
        "sku": "PC1007",
        "tipo": "Computadora",
        "marca": "Acer",
        "modelo": "Veriton",
        "usuario": "DiegoFlores",
        "equipo": "EquipoSoporte01",
        "estado": "Operativo"
    },
    {
        "id": 8,
        "sku": "LAP1008",
        "tipo": "Laptop",
        "marca": "ASUS",
        "modelo": "VivoBook",
        "usuario": "SofiaCastro",
        "equipo": "LaptopMarketing01",
        "estado": "Operativo"
    },
    {
        "id": 9,
        "sku": "PC1009",
        "tipo": "Computadora",
        "marca": "Dell",
        "modelo": "Vostro",
        "usuario": "LuisQuispe",
        "equipo": "EquipoLogistica01",
        "estado": "Inoperativo"
    },
    {
        "id": 10,
        "sku": "LAP1010",
        "tipo": "Laptop",
        "marca": "HP",
        "modelo": "EliteBook",
        "usuario": "ElenaRojas",
        "equipo": "LaptopDireccion01",
        "estado": "Operativo"
    }
]

# Bubble Sort deja los equipos ordenados para que búsqueda binaria sea válida.
equipos = ordenar_equipos_por_sku(equipos)

incidencias = [
    {
        "id": 1,
        "sku_equipo": "PC1001",
        "problema": "No enciende correctamente",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 5,
        "tiempo_estimado": 60,
        "estado": "Pendiente"
    },
    {
        "id": 2,
        "sku_equipo": "LAP1002",
        "problema": "Temperatura elevada del equipo",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 4,
        "tiempo_estimado": 45,
        "estado": "Pendiente"
    },
    {
        "id": 3,
        "sku_equipo": "PC1003",
        "problema": "Actualizacion de software pendiente",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 2,
        "tiempo_estimado": 30,
        "estado": "Pendiente"
    },
    {
        "id": 4,
        "sku_equipo": "LAP1004",
        "problema": "Bateria con bajo rendimiento",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 3,
        "tiempo_estimado": 90,
        "estado": "En proceso"
    },
    {
        "id": 5,
        "sku_equipo": "PC1005",
        "problema": "El equipo no inicia el sistema operativo",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 5,
        "tiempo_estimado": 120,
        "estado": "Pendiente"
    },
    {
        "id": 6,
        "sku_equipo": "LAP1006",
        "problema": "Lentitud general durante la ejecucion de programas",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 3,
        "tiempo_estimado": 40,
        "estado": "Pendiente"
    },
    {
        "id": 7,
        "sku_equipo": "PC1007",
        "problema": "Fallas intermitentes en el sistema",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 4,
        "tiempo_estimado": 75,
        "estado": "Finalizado"
    },
    {
        "id": 8,
        "sku_equipo": "LAP1008",
        "problema": "Problemas de conexion a la red corporativa",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 4,
        "tiempo_estimado": 50,
        "estado": "Pendiente"
    },
    {
        "id": 9,
        "sku_equipo": "PC1009",
        "problema": "Pantalla presenta errores durante el uso",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 5,
        "tiempo_estimado": 80,
        "estado": "Pendiente"
    },
    {
        "id": 10,
        "sku_equipo": "LAP1010",
        "problema": "Actualizacion de controladores requerida",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 2,
        "tiempo_estimado": 25,
        "estado": "Finalizado"
    },
    {
        "id": 11,
        "sku_equipo": "PC1001",
        "problema": "Espacio insuficiente en la unidad de almacenamiento",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 2,
        "tiempo_estimado": 35,
        "estado": "Pendiente"
    },
    {
        "id": 12,
        "sku_equipo": "LAP1002",
        "problema": "Teclado presenta algunas teclas sin respuesta",
        "tipo_mantenimiento": "Correctivo",
        "prioridad": 4,
        "tiempo_estimado": 55,
        "estado": "Pendiente"
    },
    {
        "id": 13,
        "sku_equipo": "PC1003",
        "problema": "Se detectaron errores en el disco de almacenamiento",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 5,
        "tiempo_estimado": 100,
        "estado": "Pendiente"
    },
    {
        "id": 14,
        "sku_equipo": "PC1007",
        "problema": "Limpieza interna y mantenimiento preventivo",
        "tipo_mantenimiento": "Preventivo",
        "prioridad": 1,
        "tiempo_estimado": 45,
        "estado": "Pendiente"
    },
    {
        "id": 15,
        "sku_equipo": "LAP1010",
        "problema": "Ventilador genera ruido durante el funcionamiento",
        "tipo_mantenimiento": "Predictivo",
        "prioridad": 3,
        "tiempo_estimado": 65,
        "estado": "En proceso"
    }
]

for equipo_registrado in equipos:
    tiene_incidencia_abierta = any(
        incidencia["sku_equipo"] == equipo_registrado["sku"]
        and incidencia["estado"] in ("Pendiente", "En proceso")
        for incidencia in incidencias
    )
    if tiene_incidencia_abierta:
        equipo_registrado["estado"] = "En mantenimiento"

def buscar_equipo(sku):

    if not isinstance(sku, str):
        return None

    sku = sku.strip().upper()

    # Invocación de búsqueda binaria: equipos se mantiene ordenada por SKU.
    return buscar_sku_ordenado(equipos, sku)


def buscar_incidencia(id_incidencia):

    if (
        not isinstance(id_incidencia, int)
        or isinstance(id_incidencia, bool)
    ):
        return None

    for incidencia in incidencias:

        if incidencia["id"] == id_incidencia:
            return incidencia

    return None

def sku_valido(sku):

    if not isinstance(sku, str):
        return False

    sku = sku.strip()

    if sku == "":
        return False

    if len(sku) < 1 or len(sku) > 20:
        return False


    for caracter in sku:

        if not (
            ("A" <= caracter <= "Z")
            or ("a" <= caracter <= "z")
            or ("0" <= caracter <= "9")
        ):
            return False

    return True

def modelo_valido(modelo):

    if not isinstance(modelo, str):
        return False

    modelo = modelo.strip()

    if modelo == "":
        return False

    if len(modelo) < 1 or len(modelo) > 50:
        return False


    return (
        any(caracter.isalnum() for caracter in modelo)
        and all(
            caracter.isalnum() or caracter in " ._/-"
            for caracter in modelo
        )
    )

def usuario_valido(usuario):

    if not isinstance(usuario, str):
        return False

    usuario = usuario.strip()

    if usuario == "":
        return False

    if len(usuario) < 3 or len(usuario) > 50:
        return False


    if any(
        caracter.isspace()
        for caracter in usuario
    ):
        return False


    return (
        any(caracter.isalnum() for caracter in usuario)
        and all(
            caracter.isalnum() or caracter in "._@-"
            for caracter in usuario
        )
    )


def tipo_valido(tipo):

    if not isinstance(tipo, str):
        return False

    tipo = tipo.strip()

    return (
        3 <= len(tipo) <= 50
        and any(caracter.isalpha() for caracter in tipo)
        and all(
            caracter.isalpha() or caracter in " -'"
            for caracter in tipo
        )
    )


def marca_valida(marca):

    if not isinstance(marca, str):
        return False

    marca = marca.strip()

    return (
        1 <= len(marca) <= 50
        and any(caracter.isalnum() for caracter in marca)
        and all(
            caracter.isalnum() or caracter in " &.-"
            for caracter in marca
        )
    )


def equipo_valido(equipo):

    if not isinstance(equipo, str):
        return False

    equipo = equipo.strip()

    return (
        3 <= len(equipo) <= 50
        and any(caracter.isalnum() for caracter in equipo)
        and all(
            caracter.isalnum() or caracter in " _./-"
            for caracter in equipo
        )
    )

def texto_valido(valor, campo):
    validadores = {
        "tipo": tipo_valido,
        "marca": marca_valida,
        "equipo": equipo_valido,
    }
    validador = validadores.get(campo)

    if validador is None:
        return False

    return validador(valor)

def datos_equipo_validos(
    sku,
    tipo,
    marca,
    modelo,
    usuario,
    equipo
):

    return (
        sku_valido(sku)
        and tipo_valido(tipo)
        and marca_valida(marca)
        and modelo_valido(modelo)
        and usuario_valido(usuario)
        and equipo_valido(equipo)
    )


def registrar_equipo(
    sku,
    tipo,
    marca,
    modelo,
    usuario,
    equipo
):

    if not datos_equipo_validos(
        sku,
        tipo,
        marca,
        modelo,
        usuario,
        equipo,
    ):
        return False

    sku = sku.strip().upper()
    tipo = tipo.strip()
    marca = marca.strip()
    modelo = modelo.strip()
    usuario = usuario.strip()
    equipo = equipo.strip()

    if buscar_equipo(sku) is not None:
        return False


    nuevo_id = 1

    if equipos:

        nuevo_id = max(
            equipo_reg["id"]
            for equipo_reg in equipos
        ) + 1

    nuevo_equipo = {
        "id": nuevo_id,
        "sku": sku,
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "usuario": usuario,
        "equipo": equipo,
        "estado": "Operativo"
    }

    equipos.append(nuevo_equipo)

    # Bubble Sort conserva el orden necesario para las búsquedas binarias.
    equipos[:] = ordenar_equipos_por_sku(equipos)

    return nuevo_equipo


def registrar_incidencia(
    sku,
    problema,
    tipo_mantenimiento,
    prioridad,
    tiempo
):

    if not isinstance(sku, str) or not isinstance(problema, str):
        return False

    equipo = buscar_equipo(sku)

    if equipo is None:
        return False

    if equipo_tiene_incidencia_abierta(equipo["sku"]):
        return False

    if not problema_valido(problema):
        return False

    if tipo_mantenimiento not in (
        "Preventivo",
        "Correctivo",
        "Predictivo"
    ):
        return False

    if (
        not isinstance(prioridad, int)
        or isinstance(prioridad, bool)
    ):
        return False

    if prioridad < 1 or prioridad > 5:
        return False

    if (
        not isinstance(tiempo, int)
        or isinstance(tiempo, bool)
    ):
        return False

    if tiempo < 1:
        return False

    nuevo_id = 1

    if incidencias:

        nuevo_id = max(
            incidencia["id"]
            for incidencia in incidencias
        ) + 1

    incidencia = {
        "id": nuevo_id,
        "sku_equipo": equipo["sku"],
        "problema": problema.strip(),
        "tipo_mantenimiento": tipo_mantenimiento,
        "prioridad": prioridad,
        "tiempo_estimado": tiempo,
        "estado": "Pendiente",
        "historial_mantenimiento": [{
            "estado": "Pendiente",
            "detalle": "Incidencia registrada; pendiente de atención."
        }]
    }

    incidencias.append(incidencia)


    equipo["estado"] = "En mantenimiento"

    return incidencia


def problema_valido(problema):

    if not isinstance(problema, str):
        return False

    problema = problema.strip()

    if len(problema) < 10:
        return False

    if len(problema) > 250:
        return False

    return (
        any(caracter.isalnum() for caracter in problema)
        and all(caracter.isprintable() for caracter in problema)
    )


def equipo_tiene_incidencia_abierta(sku):

    equipo = buscar_equipo(sku)

    if equipo is None:
        return False

    return any(
        incidencia["sku_equipo"] == equipo["sku"]
        and incidencia["estado"] in ("Pendiente", "En proceso")
        for incidencia in incidencias
    )


def actualizar_estado(
    id_incidencia,
    nuevo_estado,
    detalle=""
):

    if (
        not isinstance(id_incidencia, int)
        or isinstance(id_incidencia, bool)
    ):
        return False

    incidencia = buscar_incidencia(
        id_incidencia
    )

    if incidencia is None:
        return False

    siguiente_estado = {
        "Pendiente": "En proceso",
        "En proceso": "Finalizado"
    }.get(incidencia["estado"])

    if nuevo_estado != siguiente_estado:
        return False

    if (
        not isinstance(detalle, str)
        or not 10 <= len(detalle.strip()) <= 500
    ):
        return False

    if nuevo_estado in ("Pendiente", "En proceso") and any(
        otra["id"] != id_incidencia
        and otra["sku_equipo"] == incidencia["sku_equipo"]
        and otra["estado"] in ("Pendiente", "En proceso")
        for otra in incidencias
    ):
        return False

    incidencia["estado"] = nuevo_estado
    incidencia.setdefault("historial_mantenimiento", []).append({
        "estado": nuevo_estado,
        "detalle": detalle.strip()
    })

    equipo = buscar_equipo(
        incidencia["sku_equipo"]
    )

    if equipo:
        # El estado del equipo refleja si su incidencia sigue abierta.
        equipo["estado"] = (
            "En mantenimiento"
            if equipo_tiene_incidencia_abierta(equipo["sku"])
            else "Operativo"
        )

    return True


def burbuja_descendente(lista):
    # Invocación de Bubble Sort para priorizar la incidencia de mayor nivel.
    return ordenar_prioridad_descendente(lista)


def ordenar_por_tiempo(lista):
    # Invocación de Bubble Sort para ordenar la duración de menor a mayor.
    return ordenar_tiempo_ascendente(lista)


def planificar_mantenimiento():

    pendientes = []

    for incidencia in incidencias:

        if incidencia["estado"] == "Pendiente":

            pendientes.append(incidencia)

    # Invocación del algoritmo voraz sobre las incidencias pendientes.
    return planificar_por_prioridad(pendientes)


def obtener_estadisticas():

    total_equipos = len(equipos)

    total_incidencias = len(
        incidencias
    )

    pendientes = 0
    proceso = 0
    finalizadas = 0

    preventivo = 0
    correctivo = 0
    predictivo = 0

    tiempo_total = 0

    for incidencia in incidencias:

        tiempo_total += (
            incidencia["tiempo_estimado"]
        )

        if incidencia["estado"] == "Pendiente":

            pendientes += 1

        elif incidencia["estado"] == "En proceso":

            proceso += 1

        elif incidencia["estado"] == "Finalizado":

            finalizadas += 1

        if (
            incidencia["tipo_mantenimiento"]
            == "Preventivo"
        ):

            preventivo += 1

        elif (
            incidencia["tipo_mantenimiento"]
            == "Correctivo"
        ):

            correctivo += 1

        elif (
            incidencia["tipo_mantenimiento"]
            == "Predictivo"
        ):

            predictivo += 1

    if total_incidencias > 0:

        promedio = (
            tiempo_total
            / total_incidencias
        )

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


def medir_ordenamiento():

    lista = incidencias.copy()

    inicio = time.perf_counter()

    # Invocación de Bubble Sort para medir el orden por prioridad.
    resultado = burbuja_descendente(
        lista
    )

    fin = time.perf_counter()

    tiempo = fin - inicio

    return resultado, tiempo


def _medir_promedio_microsegundos(funcion, repeticiones):
    inicio = time.perf_counter()

    for _ in range(repeticiones):
        funcion()

    duracion_total = time.perf_counter() - inicio
    return duracion_total * 1_000_000 / repeticiones


def demostracion_algoritmos():
    numeros = [44, 55, 12, 42, 94, 18, 6, 67]

    inicio = time.perf_counter()
    # Bubble Sort se invoca para mostrar el orden ascendente de números.
    ascendente = ordenar_numeros(numeros, ascendente=True)
    tiempo_ascendente = time.perf_counter() - inicio

    inicio = time.perf_counter()
    # Bubble Sort se invoca para mostrar el orden descendente de números.
    descendente = ordenar_numeros(numeros, ascendente=False)
    tiempo_descendente = time.perf_counter() - inicio

    recorrido_busqueda = []
    sku_demo = equipos[-1]["sku"] if equipos else ""

    if equipos:
        # Búsqueda binaria registra los SKU centrales revisados en la demo.
        encontrado = buscar_sku_ordenado(
            equipos,
            sku_demo,
            recorrido_busqueda,
        )
    else:
        encontrado = None

    # El algoritmo voraz arma un plan real con las incidencias pendientes.
    plan_voraz = planificar_mantenimiento()

    elementos_comparacion = 8
    repeticiones_comparacion = 1000
    equipos_comparacion = [
        {"sku": f"EQ{indice:04d}"}
        for indice in range(1, elementos_comparacion + 1)
    ]
    incidencias_comparacion = [
        {
            "id": indice,
            "prioridad": indice % 5 + 1,
            "tiempo_estimado": indice * 7 + 10,
        }
        for indice in range(1, elementos_comparacion + 1)
    ]

    # Se mide Bubble Sort con una lista de ocho números.
    tiempo_comparacion_burbuja = _medir_promedio_microsegundos(
        lambda: ordenar_numeros(numeros),
        repeticiones_comparacion,
    )
    # Se mide búsqueda binaria con ocho SKU ordenados.
    tiempo_comparacion_binaria = _medir_promedio_microsegundos(
        lambda: buscar_sku_ordenado(equipos_comparacion, "EQ0008"),
        repeticiones_comparacion,
    )
    # Se mide el plan voraz con ocho incidencias.
    tiempo_comparacion_voraz = _medir_promedio_microsegundos(
        lambda: planificar_por_prioridad(incidencias_comparacion),
        repeticiones_comparacion,
    )

    return {
        "numeros_originales": numeros,
        "numeros_ascendentes": ascendente,
        "tiempo_ascendente": tiempo_ascendente,
        "numeros_descendentes": descendente,
        "tiempo_descendente": tiempo_descendente,
        "sku_demo": sku_demo,
        "recorrido_busqueda": recorrido_busqueda,
        "equipo_encontrado": encontrado,
        "plan_voraz": plan_voraz,
        "tiempos_comparacion": {
            "Bubble Sort": tiempo_comparacion_burbuja,
            "Búsqueda binaria": tiempo_comparacion_binaria,
            "Algoritmo voraz": tiempo_comparacion_voraz,
        },
        "elementos_comparacion": elementos_comparacion,
        "repeticiones_comparacion": repeticiones_comparacion,
    }


def burbuja_descendente_simple(lista):
    # Bubble Sort conserva esta función pública de compatibilidad.
    return ordenar_numeros(lista, ascendente=False)

def validar_texto_equipo(
    mensaje,
    campo
):

    instrucciones = {
        "tipo": (
            "Use 3-50 letras; se permiten espacios, guion y apóstrofo."
        ),
        "marca": (
            "Use hasta 50 letras o números; se permiten espacios, &, punto y guion."
        ),
        "equipo": (
            "Use 3-50 letras o números; se permiten espacios, _, punto, / y guion."
        ),
    }

    while True:

        print()
        print(f"Reglas para {campo}:")
        print(f"- {instrucciones.get(campo, 'Ingrese un valor válido.')}")

        valor = leer_input(
            f"Ingrese {campo}: "
        ).strip()

        if not texto_valido(
            valor,
            campo
        ):

            print(
                f"\n ALERTA: '{campo}' no cumple "
                "el formato indicado. Intente nuevamente."
            )

            continue

        return valor


def validar_sku_nuevo():

    while True:

        print()
        print("¿Qué debe ingresar en SKU?")
        print("- Letras y números.")
        print("- Sin espacios.")
        print("- Sin guiones.")
        print("- Sin tildes.")
        print("- Sin caracteres especiales.")
        print("- Debe ser único.")

        print()
        print("Ejemplos válidos:")
        print("PC1001")
        print("LAP2026")
        print("EQABC01")

        sku = leer_input(
            "\nIngrese SKU: "
        ).strip().upper()

        if sku == "":

            print(
                "\n ALERTA: El SKU "
                "no puede estar vacío."
            )

            continue

        if not sku_valido(sku):

            print(
                "\n ALERTA: SKU inválido."
            )

            print(
                "Solo se permiten letras y números."
            )

            print(
                "No se permiten espacios, "
                "guiones ni caracteres especiales."
            )

            continue

        if buscar_equipo(sku) is not None:

            print(
                f"\n ALERTA: El SKU '{sku}' "
                "ya existe."
            )

            print(
                "Debe ingresar un SKU diferente."
            )

            continue

        return sku


def validar_modelo():

    while True:

        print()
        print("¿Qué debe ingresar en Modelo?")
        print("- De 1 a 50 caracteres.")
        print("- Letras, números, espacios y . _ / -")

        print()
        print("Ejemplo:")
        print("ThinkCentre M720")

        modelo = leer_input(
            "\nIngrese Modelo: "
        ).strip()

        if modelo == "":

            print(
                "\n ALERTA: El modelo "
                "no puede estar vacío."
            )

            continue

        if not modelo_valido(modelo):

            print(
                "\n ALERTA: Modelo inválido."
            )

            print(
                "Use letras o números y, si hace falta, "
                "espacios o los signos . _ / - ."
            )

            continue

        return modelo


def validar_usuario():

    while True:

        print()
        print("¿Qué debe ingresar en Usuario?")
        print("- De 3 a 50 caracteres, sin espacios.")
        print("- Letras, números y los signos . _ @ -")

        print()
        print("Ejemplos:")
        print("CarlosPerez")
        print("usuario01")
        print("user@empresa")

        usuario = leer_input(
            "\nIngrese Usuario: "
        ).strip()

        if usuario == "":

            print(
                "\n ALERTA: El usuario "
                "no puede estar vacío."
            )

            continue

        if any(
            caracter.isspace()
            for caracter in usuario
        ):

            print(
                "\n ALERTA: El usuario "
                "no puede contener espacios."
            )

            continue

        if len(usuario) < 3:

            print(
                "\n ALERTA: El usuario debe "
                "tener mínimo 3 caracteres."
            )

            continue

        if len(usuario) > 50:

            print(
                "\n ALERTA: El usuario no puede "
                "superar los 50 caracteres."
            )

            continue

        if not usuario_valido(usuario):

            print(
                "\n ALERTA: Use solo letras, números y "
                "los signos . _ @ - ."
            )

            continue

        return usuario


def validar_sku_equipo(solo_sin_incidencia_abierta=False):

    while True:

        print()
        print(
            "¿Qué debe ingresar?"
        )

        print(
            "- Ingrese el SKU de un equipo existente."
        )

        print(
            "- Ejemplo: PC1001"
        )

        sku = leer_input(
            "\nIngrese SKU del equipo: "
        ).strip().upper()

        if sku == "":

            print(
                "\n ALERTA: El SKU "
                "no puede estar vacío."
            )

            continue

        if not sku_valido(sku):

            print(
                "\n ALERTA: El SKU "
                "no tiene un formato válido."
            )

            continue

        equipo = buscar_equipo(sku)

        if equipo is None:

            print(
                f"\n ALERTA: No existe un equipo "
                f"con SKU '{sku}'."
            )

            continue

        if (
            solo_sin_incidencia_abierta
            and equipo_tiene_incidencia_abierta(sku)
        ):
            print(
                f"\n ALERTA: El equipo '{sku}' ya tiene "
                "una incidencia pendiente o en proceso."
            )
            print("Finalícela antes de registrar otra.")
            continue

        return sku


def validar_sku_busqueda():

    while True:
        sku = leer_input("Ingrese SKU para buscar (ejemplo PC1001): ").strip().upper()

        if sku_valido(sku):
            return sku

        print(
            "\n ALERTA: El SKU debe tener entre 1 y 20 caracteres "
            "y usar solo letras y números."
        )


def validar_problema():

    while True:

        print()
        print("¿Qué debe ingresar en Problema?")
        print("- Describa el problema del equipo.")
        print("- Mínimo: 10 caracteres.")
        print("- Máximo: 250 caracteres.")
        print("- Puede utilizar letras, números, espacios y puntuación.")

        problema = leer_input(
            "\nIngrese Problema: "
        ).strip()

        if len(problema) < 10:

            print(
                "\n ALERTA: El problema debe "
                "tener mínimo 10 caracteres."
            )

            continue

        if len(problema) > 250:

            print(
                "\n ALERTA: El problema no puede "
                "superar los 250 caracteres."
            )

            continue

        if not problema_valido(problema):

            print(
                "\n ALERTA: El problema "
                "no tiene un formato válido."
            )

            continue

        return problema


def validar_tiempo_estimado():

    print()
    print(
        "¿Qué debe ingresar en Tiempo estimado?"
    )

    print(
        "- Ingrese las horas."
    )

    print(
        "- Ingrese los minutos."
    )

    print(
        "- Los minutos deben estar entre 0 y 59."
    )

    print(
        "- El tiempo debe ser mayor a cero."
    )

    while True:

        horas = validar_entero(
            "Horas: ",
            0
        )

        minutos = validar_entero(
            "Minutos (0-59): ",
            0,
            59
        )

        if horas == 0 and minutos == 0:

            print(
                "\n ALERTA: El tiempo estimado "
                "debe ser mayor que cero."
            )

            continue

        return horas * 60 + minutos


def validar_entero(
    mensaje,
    minimo=None,
    maximo=None
):

    while True:

        valor = leer_input(mensaje).strip()

        if valor == "":

            print(
                "\n ALERTA: El campo "
                "no puede estar vacío."
            )

            continue

        try:

            numero = int(valor)

            if (
                minimo is not None
                and numero < minimo
            ):

                print(
                    f"\n ALERTA: El valor debe "
                    f"ser mayor o igual a {minimo}."
                )

                continue

            if (
                maximo is not None
                and numero > maximo
            ):

                print(
                    f"\n ALERTA: El valor debe "
                    f"ser menor o igual a {maximo}."
                )

                continue

            return numero

        except ValueError:

            print(
                "\n ALERTA: Debe ingresar "
                "un número entero válido."
            )


def confirmar_accion(mensaje):

    while True:

        respuesta = leer_input(
            f"{mensaje} (S/N): "
        ).strip().upper()

        if respuesta in (
            "S",
            "SI",
            "SÍ"
        ):

            return True

        if respuesta in (
            "N",
            "NO"
        ):

            return False

        print(
            "\n ALERTA: Responda "
            "S para sí o N para no."
        )


def validar_tipo_mantenimiento():

    while True:

        print()
        print(
            "¿Qué tipo de mantenimiento "
            "corresponde?"
        )

        print("1. Preventivo")
        print("2. Correctivo")
        print("3. Predictivo")

        opcion = leer_input(
            "\nSeleccione una opción: "
        ).strip()

        tipos = {
            "1": "Preventivo",
            "2": "Correctivo",
            "3": "Predictivo"
        }

        if opcion in tipos:

            return tipos[opcion]

        print(
            "\n ALERTA: Seleccione "
            "una opción entre 1 y 3."
        )


def validar_estado(estado_actual):
    siguiente_estado = {
        "Pendiente": "En proceso",
        "En proceso": "Finalizado"
    }.get(estado_actual)

    if siguiente_estado is None:
        return None

    print("\nSiguiente estado disponible:")
    print(f"1. {siguiente_estado}")
    print("El estado solo puede avanzar, no retroceder.")

    while True:
        opcion = leer_input("\nSeleccione 1 para continuar: ").strip()
        if opcion == "1":
            return siguiente_estado
        print("\nALERTA: Seleccione la única transición disponible.")


def validar_detalle_mantenimiento():
    while True:
        detalle = leer_input(
            "Detalle realizado (10 a 500 caracteres): "
        ).strip()
        if 10 <= len(detalle) <= 500:
            return detalle
        print("\nALERTA: El detalle debe tener entre 10 y 500 caracteres.")
        
        
def contar_pendientes_recursivo(lista, indice=0):

    if indice >= len(lista):
        return 0

    if lista[indice]["estado"] == "Pendiente":
        return 1 + contar_pendientes_recursivo(
            lista,
            indice + 1
        )

    return contar_pendientes_recursivo(
        lista,
        indice + 1
    )


def planificar_voraz_detallado(
    tiempo_disponible,
    pendientes=None,
    criterio="prioridad",
):
    """Planifica incidencias y conserva el motivo de cada decisión.

    El criterio voraz ordena por prioridad descendente y, en empate, por
    duración ascendente e ID. El criterio ``tiempo`` permite comparar una
    estrategia que atiende primero las incidencias de menor duración.
    """
    if (
        not isinstance(tiempo_disponible, int)
        or isinstance(tiempo_disponible, bool)
        or tiempo_disponible < 0
    ):
        raise ValueError("El tiempo disponible debe ser un entero no negativo.")

    if criterio not in ("prioridad", "tiempo"):
        raise ValueError("El criterio debe ser 'prioridad' o 'tiempo'.")

    fuente = incidencias if pendientes is None else pendientes
    candidatas = [
        incidencia.copy()
        for incidencia in fuente
        if incidencia.get("estado", "Pendiente") == "Pendiente"
    ]

    if criterio == "prioridad":
        ordenadas = planificar_por_prioridad(candidatas)
    else:
        ordenadas = ordenar_por_tiempo(candidatas)

    seleccionadas = []
    descartadas = []
    decisiones = []
    tiempo_usado = 0

    for incidencia in ordenadas:
        tiempo_restante = tiempo_disponible - tiempo_usado
        duracion = incidencia["tiempo_estimado"]
        cabe_en_tiempo = duracion <= tiempo_restante

        if cabe_en_tiempo:
            seleccionadas.append(incidencia)
            tiempo_usado += duracion
            motivo = (
                f"Seleccionada: requiere {duracion} min y caben "
                f"en los {tiempo_restante} min restantes."
            )
        else:
            descartadas.append(incidencia)
            motivo = (
                f"Descartada: requiere {duracion} min y solo quedan "
                f"{tiempo_restante} min."
            )

        decisiones.append({
            "incidencia": incidencia,
            "seleccionada": cabe_en_tiempo,
            "motivo": motivo,
            "tiempo_restante": tiempo_disponible - tiempo_usado,
        })

    return {
        "criterio": criterio,
        "tiempo_disponible": tiempo_disponible,
        "incidencias_pendientes": candidatas,
        "seleccionadas": seleccionadas,
        "descartadas": descartadas,
        "decisiones": decisiones,
        "tiempo_usado": tiempo_usado,
        "tiempo_restante": tiempo_disponible - tiempo_usado,
    }


def planificar_voraz(tiempo_disponible):
    """Conserva la interfaz histórica de lista seleccionada y tiempo usado."""
    resultado = planificar_voraz_detallado(tiempo_disponible)
    return resultado["seleccionadas"], resultado["tiempo_usado"]


def planificar_backtracking_detallado(
    tiempo_disponible,
    pendientes=None,
    max_historial=5000,
):
    """Busca la mejor combinación factible y registra la exploración.

    Función objetivo lexicográfica: primero maximiza la cantidad de
    incidencias; luego la suma de prioridades (ponderación existente 1-5);
    finalmente minimiza los minutos de mantenimiento. Solo usa incidencias
    Pendientes y la suma de sus duraciones no supera el presupuesto.
    """
    if (
        not isinstance(tiempo_disponible, int)
        or isinstance(tiempo_disponible, bool)
        or tiempo_disponible < 0
    ):
        raise ValueError("El tiempo disponible debe ser un entero no negativo.")
    if (
        not isinstance(max_historial, int)
        or isinstance(max_historial, bool)
        or max_historial < 1
    ):
        raise ValueError("El límite del historial debe ser un entero positivo.")

    fuente = incidencias if pendientes is None else pendientes
    candidatas = [
        incidencia.copy()
        for incidencia in fuente
        if incidencia.get("estado", "Pendiente") == "Pendiente"
    ]
    for incidencia in candidatas:
        if (
            not isinstance(incidencia.get("tiempo_estimado"), int)
            or isinstance(incidencia.get("tiempo_estimado"), bool)
            or incidencia["tiempo_estimado"] < 1
            or not isinstance(incidencia.get("prioridad"), int)
            or isinstance(incidencia.get("prioridad"), bool)
            or not 1 <= incidencia["prioridad"] <= 5
            or "id" not in incidencia
        ):
            raise ValueError("Hay una incidencia pendiente con datos inválidos.")

    contexto = {
        "nodos_explorados": 0,
        "ramas_podadas": 0,
        "podas_por_tiempo": 0,
        "podas_por_cota": 0,
        "retrocesos": 0,
        "soluciones_evaluadas": 0,
        "historial": [],
        "eventos_totales": 0,
        "soluciones": [],
        "soluciones_totales": 0,
        "siguiente_nodo": 0,
        "max_historial": max_historial,
        "mejor": {
            "seleccionadas": [],
            "tiempo": 0,
            "prioridad": 0,
            "nodo": None,
            "camino": [],
        },
    }

    def registrar(evento):
        contexto["eventos_totales"] += 1
        if len(contexto["historial"]) < max_historial:
            contexto["historial"].append(evento)

    def clave_solucion(seleccionadas, tiempo, prioridad):
        return len(seleccionadas), prioridad, -tiempo

    def registrar_nodo(
        indice,
        seleccionadas,
        tiempo,
        prioridad,
        padre,
        decision,
        camino,
        incidencia=None,
        tiempo_excedido=False,
    ):
        contexto["siguiente_nodo"] += 1
        contexto["nodos_explorados"] += 1
        nodo = {
            "tipo": "nodo",
            "nodo": contexto["siguiente_nodo"],
            "padre": padre,
            "profundidad": indice,
            "id_incidencia": incidencia["id"] if incidencia else None,
            "decision": decision,
            "tiempo_acumulado": tiempo,
            "seleccionadas": [item["id"] for item in seleccionadas],
            "mejor_cantidad": len(contexto["mejor"]["seleccionadas"]),
            "mejor_prioridad": contexto["mejor"]["prioridad"],
            "mejor_tiempo": contexto["mejor"]["tiempo"],
            "podada": tiempo_excedido,
            "solucion_final": False,
        }
        registrar(nodo)
        return nodo

    def buscar(indice, seleccionadas, tiempo, prioridad, padre, decision, camino):
        nodo = registrar_nodo(
            indice,
            seleccionadas,
            tiempo,
            prioridad,
            padre,
            decision,
            camino,
            candidatas[indice] if indice < len(candidatas) else None,
        )
        camino_actual = camino + [nodo["nodo"]]

        if indice == len(candidatas):
            contexto["soluciones_evaluadas"] += 1
            contexto["soluciones_totales"] += 1
            mejor = contexto["mejor"]
            actual = clave_solucion(seleccionadas, tiempo, prioridad)
            if mejor["nodo"] is None or actual > clave_solucion(
                mejor["seleccionadas"],
                mejor["tiempo"],
                mejor["prioridad"],
            ):
                mejor.update({
                    "seleccionadas": seleccionadas.copy(),
                    "tiempo": tiempo,
                    "prioridad": prioridad,
                    "nodo": nodo["nodo"],
                    "camino": camino_actual.copy(),
                })
                nodo.update({
                    "solucion_final": True,
                    "mejor_cantidad": len(seleccionadas),
                    "mejor_prioridad": prioridad,
                    "mejor_tiempo": tiempo,
                })
            if len(contexto["soluciones"]) < max_historial:
                contexto["soluciones"].append({
                    "cantidad": len(seleccionadas),
                    "prioridad": prioridad,
                    "tiempo": tiempo,
                    "ids": [item["id"] for item in seleccionadas],
                })
            return

        restantes = candidatas[indice:]
        cantidad_maxima = len(seleccionadas) + len(restantes)
        mejor_cantidad = len(contexto["mejor"]["seleccionadas"])
        motivo_poda = None

        if cantidad_maxima < mejor_cantidad:
            motivo_poda = "poda-cantidad"
        elif cantidad_maxima == mejor_cantidad:
            necesarias = mejor_cantidad - len(seleccionadas)
            prioridades_optimistas = sorted(
                (item["prioridad"] for item in restantes),
                reverse=True,
            )
            prioridad_maxima = prioridad + sum(
                prioridades_optimistas[:necesarias]
            )
            mejor_prioridad = contexto["mejor"]["prioridad"]
            if prioridad_maxima < mejor_prioridad:
                motivo_poda = "poda-prioridad"
            elif prioridad_maxima == mejor_prioridad:
                duraciones_optimistas = sorted(
                    item["tiempo_estimado"] for item in restantes
                )
                tiempo_minimo = tiempo + sum(
                    duraciones_optimistas[:necesarias]
                )
                if tiempo_minimo >= contexto["mejor"]["tiempo"]:
                    motivo_poda = "poda-tiempo-minimo"

        if motivo_poda:
            nodo["podada"] = True
            nodo["motivo_poda"] = motivo_poda
            contexto["ramas_podadas"] += 1
            contexto["podas_por_cota"] += 1
            return

        incidencia = candidatas[indice]
        nuevo_tiempo = tiempo + incidencia["tiempo_estimado"]
        if nuevo_tiempo <= tiempo_disponible:
            seleccionadas.append(incidencia)
            buscar(
                indice + 1,
                seleccionadas,
                nuevo_tiempo,
                prioridad + incidencia["prioridad"],
                nodo["nodo"],
                f"incluir ID {incidencia['id']}",
                camino_actual,
            )
            seleccionadas.pop()
            contexto["retrocesos"] += 1
            registrar({
                "tipo": "retroceso",
                "nodo": nodo["nodo"],
                "id_incidencia": incidencia["id"],
                "tiempo_acumulado": tiempo,
                "seleccionadas": [item["id"] for item in seleccionadas],
            })
        else:
            podado = registrar_nodo(
                indice + 1,
                seleccionadas + [incidencia],
                nuevo_tiempo,
                prioridad + incidencia["prioridad"],
                nodo["nodo"],
                f"poda-tiempo al incluir ID {incidencia['id']}",
                camino_actual,
                incidencia,
                tiempo_excedido=True,
            )
            podado["motivo_poda"] = "supera el presupuesto disponible"
            contexto["ramas_podadas"] += 1
            contexto["podas_por_tiempo"] += 1

        buscar(
            indice + 1,
            seleccionadas,
            tiempo,
            prioridad,
            nodo["nodo"],
            f"excluir ID {incidencia['id']}",
            camino_actual,
        )
        contexto["retrocesos"] += 1
        registrar({
            "tipo": "retroceso",
            "nodo": nodo["nodo"],
            "id_incidencia": incidencia["id"],
            "tiempo_acumulado": tiempo,
            "seleccionadas": [item["id"] for item in seleccionadas],
        })

    buscar(0, [], 0, 0, None, "inicio", [])
    mejor = contexto["mejor"]
    ids_seleccionadas = {item["id"] for item in mejor["seleccionadas"]}
    nodos_historial = {
        evento["nodo"]: evento
        for evento in contexto["historial"]
        if evento.get("tipo") == "nodo"
    }
    for nodo_id in mejor["camino"]:
        if nodo_id in nodos_historial:
            nodos_historial[nodo_id]["solucion_final"] = True

    return {
        "tiempo_disponible": tiempo_disponible,
        "incidencias_pendientes": candidatas,
        "seleccionadas": mejor["seleccionadas"],
        "no_seleccionadas": [
            incidencia for incidencia in candidatas
            if incidencia["id"] not in ids_seleccionadas
        ],
        "tiempo_usado": mejor["tiempo"],
        "tiempo_restante": tiempo_disponible - mejor["tiempo"],
        "prioridad_total": mejor["prioridad"],
        "nodos_explorados": contexto["nodos_explorados"],
        "ramas_podadas": contexto["ramas_podadas"],
        "podas_por_tiempo": contexto["podas_por_tiempo"],
        "podas_por_cota": contexto["podas_por_cota"],
        "retrocesos": contexto["retrocesos"],
        "soluciones_evaluadas": contexto["soluciones_evaluadas"],
        "soluciones_totales": contexto["soluciones_totales"],
        "soluciones": contexto["soluciones"],
        "historial": contexto["historial"],
        "eventos_totales": contexto["eventos_totales"],
        "historial_truncado": contexto["eventos_totales"] > max_historial,
        "nodo_solucion": mejor["nodo"],
        "camino_solucion": mejor["camino"],
        "ponderacion_prioridad": "Suma de los valores existentes: 1=Baja a 5=Crítica.",
        "funcion_objetivo": (
            "Maximizar cantidad; luego suma de prioridades; "
            "finalmente minimizar duración total."
        ),
    }


def backtracking_mantenimiento(
    pendientes,
    tiempo_disponible,
    indice=0,
    seleccion_actual=None,
    tiempo_actual=0,
    prioridad_actual=0,
):
    """Mantiene el retorno histórico usando el motor optimizador actualizado."""
    seleccion_inicial = list(seleccion_actual or [])
    candidatas = pendientes[indice:]
    presupuesto_restante = tiempo_disponible - tiempo_actual
    if presupuesto_restante < 0:
        return seleccion_inicial, tiempo_actual, prioridad_actual
    resultado = planificar_backtracking_detallado(
        presupuesto_restante,
        candidatas,
    )
    seleccion_final = seleccion_inicial + resultado["seleccionadas"]
    return (
        seleccion_final,
        tiempo_actual + resultado["tiempo_usado"],
        prioridad_actual + resultado["prioridad_total"],
    )


def planificar_backtracking(tiempo_disponible):
    """Conserva el retorno histórico: incidencias, minutos y prioridad total."""
    resultado = planificar_backtracking_detallado(tiempo_disponible)
    return (
        resultado["seleccionadas"],
        resultado["tiempo_usado"],
        resultado["prioridad_total"],
    )

