def buscar_sku_ordenado(equipos, sku, recorrido=None):
    """Busca un SKU en equipos ordenados alfabéticamente por SKU.

    Revisa el elemento del centro. Si el SKU buscado es menor, continúa
    por la mitad izquierda; si es mayor, continúa por la derecha.
    Devuelve el equipo encontrado o None cuando no existe.
    """
    if not isinstance(sku, str):
        return None

    sku_buscado = sku.strip().upper()
    izquierda = 0
    derecha = len(equipos) - 1

    while izquierda <= derecha:
        centro = (izquierda + derecha) // 2
        sku_centro = equipos[centro]["sku"].strip().upper()

        if recorrido is not None:
            recorrido.append(sku_centro)

        if sku_centro == sku_buscado:
            return equipos[centro]

        if sku_buscado < sku_centro:
            derecha = centro - 1
        else:
            izquierda = centro + 1

    return None
