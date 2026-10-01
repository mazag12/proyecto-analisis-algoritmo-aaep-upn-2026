def planificar_por_prioridad(incidencias_pendientes):
    """Devuelve un plan voraz sin modificar la lista recibida.

    En cada paso elige la incidencia con mayor prioridad. Si hay empate,
    elige la de menor duración y después la de menor ID. La decisión local
    es fácil de explicar, pero no garantiza el mejor resultado global.
    """
    candidatas = incidencias_pendientes.copy()
    plan = []

    while candidatas:
        indice_mejor = 0
        clave_mejor = (
            -candidatas[0]["prioridad"],
            candidatas[0]["tiempo_estimado"],
            candidatas[0]["id"],
        )

        for indice in range(1, len(candidatas)):
            incidencia = candidatas[indice]
            clave = (
                -incidencia["prioridad"],
                incidencia["tiempo_estimado"],
                incidencia["id"],
            )

            if clave < clave_mejor:
                indice_mejor = indice
                clave_mejor = clave

        plan.append(candidatas.pop(indice_mejor))

    return plan
