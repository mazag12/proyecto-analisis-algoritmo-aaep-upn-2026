"""
Created on Tue Sep  8 21:07:30 2026

@author: MAZAG
"""
import time

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
    }
]

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
    }
]

def buscar_equipo(sku):

    if not isinstance(sku, str):
        return None

    sku = sku.strip().upper()

    for equipo in equipos:

        if equipo["sku"].upper() == sku:
            return equipo

    return None


def buscar_incidencia(id_incidencia):

    for incidencia in incidencias:

        if incidencia["id"] == id_incidencia:
            return incidencia

    return None

def sku_valido(sku):

    if not isinstance(sku, str):
        return False

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

    if modelo == "":
        return False

    if len(modelo) < 1 or len(modelo) > 50:
        return False


    for caracter in modelo:

        if not (
            ("A" <= caracter <= "Z")
            or ("a" <= caracter <= "z")
            or ("0" <= caracter <= "9")
        ):
            return False

    return True

def usuario_valido(usuario):

    if not isinstance(usuario, str):
        return False

    if usuario == "":
        return False

    if len(usuario) < 3 or len(usuario) > 50:
        return False


    if any(
        caracter.isspace()
        for caracter in usuario
    ):
        return False


    return True

def texto_valido(valor, campo):

    if not isinstance(valor, str):
        return False

    valor = valor.strip()

    if valor == "":
        return False

    if len(valor) < 3:
        return False

    if len(valor) > 50:
        return False

    return True

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
        and texto_valido(tipo, "tipo")
        and texto_valido(marca, "marca")
        and modelo_valido(modelo)
        and usuario_valido(usuario)
        and texto_valido(equipo, "equipo")
    )


def registrar_equipo(
    sku,
    tipo,
    marca,
    modelo,
    usuario,
    equipo
):

    sku = str(sku).strip().upper()
    tipo = str(tipo).strip()
    marca = str(marca).strip()
    modelo = str(modelo).strip()
    usuario = str(usuario).strip()
    equipo = str(equipo).strip()

    if not datos_equipo_validos(
        sku,
        tipo,
        marca,
        modelo,
        usuario,
        equipo
    ):
        return False


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

    return nuevo_equipo


def registrar_incidencia(
    sku,
    problema,
    tipo_mantenimiento,
    prioridad,
    tiempo
):

    equipo = buscar_equipo(sku)

    if equipo is None:
        return False

    if not problema_valido(problema):
        return False

    if tipo_mantenimiento not in (
        "Preventivo",
        "Correctivo",
        "Predictivo"
    ):
        return False

    if not isinstance(prioridad, int):
        return False

    if prioridad < 1 or prioridad > 5:
        return False

    if not isinstance(tiempo, int):
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
        "sku_equipo": sku,
        "problema": problema,
        "tipo_mantenimiento": tipo_mantenimiento,
        "prioridad": prioridad,
        "tiempo_estimado": tiempo,
        "estado": "Pendiente"
    }

    incidencias.append(incidencia)


    equipo["estado"] = "Inoperativo"

    return incidencia


def problema_valido(problema):

    if not isinstance(problema, str):
        return False

    problema = problema.strip()

    if len(problema) < 10:
        return False

    if len(problema) > 250:
        return False

    return True


def actualizar_estado(
    id_incidencia,
    nuevo_estado
):

    incidencia = buscar_incidencia(
        id_incidencia
    )

    if incidencia is None:
        return False

    estados_validos = (
        "Pendiente",
        "En proceso",
        "Finalizado"
    )

    if nuevo_estado not in estados_validos:
        return False

    incidencia["estado"] = nuevo_estado

    equipo = buscar_equipo(
        incidencia["sku_equipo"]
    )

    if equipo:

        if nuevo_estado == "Finalizado":

            equipo["estado"] = "Operativo"

        elif nuevo_estado in (
            "Pendiente",
            "En proceso"
        ):

            equipo["estado"] = "Inoperativo"

    return True


def burbuja_descendente(lista):

    lista = lista.copy()

    n = len(lista)

    for i in range(n):

        for j in range(
            0,
            n - i - 1
        ):

            if (
                lista[j]["prioridad"]
                < lista[j + 1]["prioridad"]
            ):

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


def ordenar_por_tiempo(lista):

    lista = lista.copy()

    n = len(lista)

    for i in range(n):

        for j in range(
            0,
            n - i - 1
        ):

            if (
                lista[j]["tiempo_estimado"]
                > lista[j + 1]["tiempo_estimado"]
            ):

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


def planificar_mantenimiento():

    pendientes = []

    for incidencia in incidencias:

        if incidencia["estado"] == "Pendiente":

            pendientes.append(incidencia)

    return burbuja_descendente(
        pendientes
    )


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

    resultado = burbuja_descendente(
        lista
    )

    fin = time.perf_counter()

    tiempo = fin - inicio

    return resultado, tiempo


def demostracion_algoritmos():

    lista = [
        44,
        55,
        12,
        42,
        94,
        18,
        6,
        67
    ]

    original = lista.copy()


    ascendente = lista.copy()

    inicio = time.perf_counter()

    n = len(ascendente)

    for i in range(n):

        for j in range(
            0,
            n - i - 1
        ):

            if (
                ascendente[j]
                > ascendente[j + 1]
            ):

                ascendente[j], ascendente[j + 1] = (
                    ascendente[j + 1],
                    ascendente[j]
                )

    fin = time.perf_counter()

    tiempo_ascendente = (
        fin - inicio
    )


    descendente = lista.copy()

    inicio = time.perf_counter()

    descendente = (
        burbuja_descendente_simple(
            descendente
        )
    )

    fin = time.perf_counter()

    tiempo_descendente = (
        fin - inicio
    )

    return (
        original,
        ascendente,
        tiempo_ascendente,
        descendente,
        tiempo_descendente
    )


def burbuja_descendente_simple(lista):

    n = len(lista)

    for i in range(n):

        for j in range(
            0,
            n - i - 1
        ):

            if (
                lista[j]
                < lista[j + 1]
            ):

                lista[j], lista[j + 1] = (
                    lista[j + 1],
                    lista[j]
                )

    return lista


def validar_texto_equipo(
    mensaje,
    campo
):

    while True:

        print()
        print(
            f"¿Qué debe ingresar en {campo}?"
        )

        print(
            "- No puede estar vacío."
        )

        print(
            "- Mínimo: 3 caracteres."
        )

        print(
            "- Máximo: 50 caracteres."
        )

        valor = input(
            f"Ingrese {campo}: "
        ).strip()

        if valor == "":

            print(
                f"\n ALERTA: El campo "
                f"'{campo}' no puede estar vacío."
            )

            continue

        if len(valor) < 3:

            print(
                f"\n ALERTA: El campo "
                f"'{campo}' debe tener mínimo "
                f"3 caracteres."
            )

            continue

        if len(valor) > 50:

            print(
                f"\n ALERTA: El campo "
                f"'{campo}' no puede superar "
                f"los 50 caracteres."
            )

            continue

        if not texto_valido(
            valor,
            campo
        ):

            print(
                f"\n ALERTA: El valor ingresado "
                f"para '{campo}' no es válido."
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

        sku = input(
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
        print("- Letras y números.")
        print("- Sin espacios.")
        print("- Sin caracteres especiales.")

        print()
        print("Ejemplo:")
        print("ThinkCentreM720")

        modelo = input(
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
                "El modelo solo debe contener "
                "letras y números."
            )

            continue

        return modelo


def validar_usuario():

    while True:

        print()
        print("¿Qué debe ingresar en Usuario?")
        print("- Letras.")
        print("- Números.")
        print("- Caracteres especiales.")
        print("- NO se permiten espacios.")

        print()
        print("Ejemplos:")
        print("CarlosPerez")
        print("usuario01")
        print("user@empresa")

        usuario = input(
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

        return usuario


def validar_sku_equipo():

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

        sku = input(
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

        return sku


def validar_problema():

    while True:

        print()
        print("¿Qué debe ingresar en Problema?")
        print("- Describa el problema del equipo.")
        print("- Mínimo: 10 caracteres.")
        print("- Máximo: 250 caracteres.")
        print("- Puede utilizar letras, números, espacios y puntuación.")

        problema = input(
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

        valor = input(mensaje).strip()

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

        respuesta = input(
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

        opcion = input(
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


def validar_estado():

    while True:

        print()
        print(
            "¿Qué estado desea asignar?"
        )

        print("1. Pendiente")
        print("2. En proceso")
        print("3. Finalizado")

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        estados = {
            "1": "Pendiente",
            "2": "En proceso",
            "3": "Finalizado"
        }

        if opcion in estados:

            return estados[opcion]

        print(
            "\n ALERTA: Seleccione "
            "una opción entre 1 y 3."
        )