"""
Created on Tue Sep  8 21:07:30 2026

@author: MAZAG
"""
import time
from algoritmo_voraz import planificar_por_prioridad
from busqueda_binaria import buscar_sku_ordenado
from ordenamiento_burbuja import (
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


def planificar_voraz(tiempo_disponible):

    pendientes = []

    for incidencia in incidencias:

        if incidencia["estado"] == "Pendiente":
            pendientes.append(incidencia.copy())

    # Ordenar por prioridad descendente
    # y, en caso de empate, por menor tiempo
    n = len(pendientes)

    for i in range(n):

        for j in range(0, n - i - 1):

            prioridad_actual = pendientes[j]["prioridad"]
            prioridad_siguiente = pendientes[j + 1]["prioridad"]

            tiempo_actual = pendientes[j]["tiempo_estimado"]
            tiempo_siguiente = pendientes[j + 1]["tiempo_estimado"]

            if (
                prioridad_actual < prioridad_siguiente
                or (
                    prioridad_actual == prioridad_siguiente
                    and tiempo_actual > tiempo_siguiente
                )
            ):

                pendientes[j], pendientes[j + 1] = (
                    pendientes[j + 1],
                    pendientes[j]
                )

    seleccionadas = []
    tiempo_usado = 0

    for incidencia in pendientes:

        tiempo = incidencia["tiempo_estimado"]

        if tiempo_usado + tiempo <= tiempo_disponible:

            seleccionadas.append(incidencia)

            tiempo_usado += tiempo

    return seleccionadas, tiempo_usado


def backtracking_mantenimiento(
    pendientes,
    tiempo_disponible,
    indice=0,
    seleccion_actual=None,
    tiempo_actual=0,
    prioridad_actual=0
):

    if seleccion_actual is None:
        seleccion_actual = []

    # Caso base
    if indice >= len(pendientes):

        return (
            seleccion_actual.copy(),
            tiempo_actual,
            prioridad_actual
        )

    # Mejor solución encontrada hasta el momento
    mejor_lista = seleccion_actual.copy()
    mejor_tiempo = tiempo_actual
    mejor_prioridad = prioridad_actual

    incidencia = pendientes[indice]

    tiempo = incidencia["tiempo_estimado"]
    prioridad = incidencia["prioridad"]

    # RAMA 1: INCLUIR LA INCIDENCIA

    if tiempo_actual + tiempo <= tiempo_disponible:

        seleccion_actual.append(incidencia)

        lista_incluida, tiempo_incluido, prioridad_incluida = (
            backtracking_mantenimiento(
                pendientes,
                tiempo_disponible,
                indice + 1,
                seleccion_actual,
                tiempo_actual + tiempo,
                prioridad_actual + prioridad
            )
        )

        seleccion_actual.pop()

        if prioridad_incluida > mejor_prioridad:

            mejor_lista = lista_incluida
            mejor_tiempo = tiempo_incluido
            mejor_prioridad = prioridad_incluida


    #RAMA 2: NO INCLUIR LA INCIDENCIA


    lista_sin, tiempo_sin, prioridad_sin = (
        backtracking_mantenimiento(
            pendientes,
            tiempo_disponible,
            indice + 1,
            seleccion_actual,
            tiempo_actual,
            prioridad_actual
        )
    )

    if prioridad_sin > mejor_prioridad:

        mejor_lista = lista_sin
        mejor_tiempo = tiempo_sin
        mejor_prioridad = prioridad_sin

    return (
        mejor_lista,
        mejor_tiempo,
        mejor_prioridad
    )


def planificar_backtracking(tiempo_disponible):

    pendientes = []

    for incidencia in incidencias:

        if incidencia["estado"] == "Pendiente":
            pendientes.append(incidencia.copy())

    return backtracking_mantenimiento(
        pendientes,
        tiempo_disponible
    )

