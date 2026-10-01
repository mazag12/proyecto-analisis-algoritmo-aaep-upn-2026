def ordenar_prioridad_descendente(lista):
    """Devuelve una copia ordenada por prioridad, de mayor a menor.

    Compara incidencias vecinas y las intercambia cuando la primera
    tiene menor prioridad. Repite las pasadas hasta ordenar la lista.
    """
    resultado = lista.copy()
    cantidad = len(resultado)

    for pasada in range(cantidad):
        hubo_intercambio = False

        for indice in range(cantidad - pasada - 1):
            if resultado[indice]["prioridad"] < resultado[indice + 1]["prioridad"]:
                resultado[indice], resultado[indice + 1] = (
                    resultado[indice + 1],
                    resultado[indice],
                )
                hubo_intercambio = True

        if not hubo_intercambio:
            break

    return resultado


def ordenar_tiempo_ascendente(lista):
    """Devuelve una copia ordenada por tiempo estimado, de menor a mayor."""
    resultado = lista.copy()
    cantidad = len(resultado)

    for pasada in range(cantidad):
        hubo_intercambio = False

        for indice in range(cantidad - pasada - 1):
            if (
                resultado[indice]["tiempo_estimado"]
                > resultado[indice + 1]["tiempo_estimado"]
            ):
                resultado[indice], resultado[indice + 1] = (
                    resultado[indice + 1],
                    resultado[indice],
                )
                hubo_intercambio = True

        if not hubo_intercambio:
            break

    return resultado


def ordenar_numeros(lista, ascendente=True):
    """Ordena una copia de números mediante Bubble Sort."""
    resultado = lista.copy()
    cantidad = len(resultado)

    for pasada in range(cantidad):
        hubo_intercambio = False

        for indice in range(cantidad - pasada - 1):
            valores_fuera_de_orden = (
                resultado[indice] > resultado[indice + 1]
                if ascendente
                else resultado[indice] < resultado[indice + 1]
            )

            if valores_fuera_de_orden:
                resultado[indice], resultado[indice + 1] = (
                    resultado[indice + 1],
                    resultado[indice],
                )
                hubo_intercambio = True

        if not hubo_intercambio:
            break

    return resultado


def ordenar_equipos_por_sku(equipos):
    """Devuelve una copia de equipos ordenada por SKU ascendente."""
    resultado = equipos.copy()
    cantidad = len(resultado)

    for pasada in range(cantidad):
        hubo_intercambio = False

        for indice in range(cantidad - pasada - 1):
            sku_actual = resultado[indice]["sku"].upper()
            sku_siguiente = resultado[indice + 1]["sku"].upper()

            if sku_actual > sku_siguiente:
                resultado[indice], resultado[indice + 1] = (
                    resultado[indice + 1],
                    resultado[indice],
                )
                hubo_intercambio = True

        if not hubo_intercambio:
            break

    return resultado
