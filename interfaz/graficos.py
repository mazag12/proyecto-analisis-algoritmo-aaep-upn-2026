"""Gráficos de resultados reales de planificación de mantenimiento."""


def mostrar_graficos_planificacion(plan_prioridad, plan_menor_tiempo):
    """Muestra cuatro gráficos comparativos para dos planes calculados."""
    import matplotlib.pyplot as plt

    candidatos = plan_prioridad["incidencias_pendientes"]
    prioridad_seleccionada = {
        incidencia["id"] for incidencia in plan_prioridad["seleccionadas"]
    }
    etiquetas = [
        f"#{incidencia['id']} {incidencia['sku_equipo']}"
        for incidencia in candidatos
    ]
    duraciones_seleccionadas = [
        incidencia["tiempo_estimado"]
        if incidencia["id"] in prioridad_seleccionada else 0
        for incidencia in candidatos
    ]
    duraciones_descartadas = [
        incidencia["tiempo_estimado"]
        if incidencia["id"] not in prioridad_seleccionada else 0
        for incidencia in candidatos
    ]

    figura, ejes = plt.subplots(2, 2, figsize=(14, 9))
    figura.suptitle("Planificación de mantenimiento", fontsize=15)

    eje = ejes[0, 0]
    posiciones = list(range(len(candidatos)))
    ancho = 0.38
    eje.bar(
        [posicion - ancho / 2 for posicion in posiciones],
        duraciones_seleccionadas,
        ancho,
        label="Seleccionadas",
        color="#26734d",
    )
    eje.bar(
        [posicion + ancho / 2 for posicion in posiciones],
        duraciones_descartadas,
        ancho,
        label="Descartadas",
        color="#c65d3a",
    )
    eje.set_title("Tiempo estimado por incidencia (Greedy)")
    eje.set_ylabel("Minutos")
    eje.set_xticks(posiciones, etiquetas, rotation=35, ha="right")
    eje.legend()
    if not candidatos:
        eje.text(0.5, 0.5, "Sin incidencias pendientes", ha="center")

    eje = ejes[0, 1]
    eje.pie(
        [plan_prioridad["tiempo_usado"], plan_prioridad["tiempo_restante"]],
        labels=["Utilizado", "Restante"],
        autopct="%1.1f%%",
        colors=["#26734d", "#ded8c8"],
        startangle=90,
    )
    eje.set_title(
        f"Tiempo del técnico ({plan_prioridad['tiempo_disponible']} min)"
    )

    eje = ejes[1, 0]
    prioridades = (1, 2, 3, 4, 5)
    nombres = ("Baja", "Media", "Normal", "Alta", "Crítica")
    ids_prioridad = {
        incidencia["id"]
        for incidencia in plan_prioridad["seleccionadas"]
    }
    ids_tiempo = {
        incidencia["id"]
        for incidencia in plan_menor_tiempo["seleccionadas"]
    }
    total_prioridad = []
    seleccionadas_prioridad = []
    seleccionadas_tiempo = []
    for prioridad in prioridades:
        total = sum(
            incidencia["prioridad"] == prioridad
            for incidencia in candidatos
        )
        total_prioridad.append(total)
        seleccionadas_prioridad.append(sum(
            incidencia["prioridad"] == prioridad
            and incidencia["id"] in ids_prioridad
            for incidencia in candidatos
        ))
        seleccionadas_tiempo.append(sum(
            incidencia["prioridad"] == prioridad
            and incidencia["id"] in ids_tiempo
            for incidencia in candidatos
        ))
    ancho = 0.38
    posiciones_prioridad = [
        posicion - ancho / 2 for posicion in range(len(prioridades))
    ]
    posiciones_tiempo = [
        posicion + ancho / 2 for posicion in range(len(prioridades))
    ]
    eje.bar(
        posiciones_prioridad,
        seleccionadas_prioridad,
        ancho,
        label="Greedy: seleccionadas",
        color="#26734d",
    )
    eje.bar(
        posiciones_prioridad,
        [total - cantidad for total, cantidad in zip(
            total_prioridad,
            seleccionadas_prioridad,
        )],
        ancho,
        bottom=seleccionadas_prioridad,
        label="Greedy: descartadas",
        color="#c65d3a",
    )
    eje.bar(
        posiciones_tiempo,
        seleccionadas_tiempo,
        ancho,
        label="Menor duración: seleccionadas",
        color="#4d83a8",
    )
    eje.bar(
        posiciones_tiempo,
        [total - cantidad for total, cantidad in zip(
            total_prioridad,
            seleccionadas_tiempo,
        )],
        ancho,
        bottom=seleccionadas_tiempo,
        label="Menor duración: descartadas",
        color="#d7a05d",
    )
    eje.set_title("Incidencias pendientes según prioridad")
    eje.set_ylabel("Cantidad")
    eje.set_xticks(list(range(len(prioridades))), nombres)
    eje.legend()

    eje = ejes[1, 1]
    for resultado, etiqueta, color, estilo in (
        (plan_prioridad, "Prioridad y duración", "#26734d", "-"),
        (plan_menor_tiempo, "Menor duración", "#4d83a8", "--"),
    ):
        acumulado = 0
        puntos_x = [0]
        puntos_y = [0]
        for posicion, incidencia in enumerate(resultado["seleccionadas"], 1):
            acumulado += incidencia["tiempo_estimado"]
            puntos_x.append(posicion)
            puntos_y.append(acumulado)
        eje.step(
            puntos_x,
            puntos_y,
            where="post",
            label=etiqueta,
            color=color,
            linestyle=estilo,
            marker="o",
        )
    eje.axhline(
        plan_prioridad["tiempo_disponible"],
        color="#c65d3a",
        linestyle=":",
        label="Tiempo disponible",
    )
    eje.set_title("Tiempo acumulado en orden de atención")
    eje.set_xlabel("Incidencias atendidas")
    eje.set_ylabel("Minutos acumulados")
    eje.legend()

    figura.tight_layout()
    plt.show()


def mostrar_graficos_backtracking(
    resultado,
    plan_voraz,
    tiempo_backtracking,
    tiempo_voraz,
    max_nodos=120,
):
    """Grafica árbol limitado, soluciones, exploración y uso de tiempo."""
    import matplotlib.pyplot as plt

    figura, ejes = plt.subplots(2, 2, figsize=(15, 10))
    figura.suptitle("Backtracking y comparación con Greedy", fontsize=15)

    if max_nodos < 1:
        raise ValueError("max_nodos debe ser un entero positivo.")

    nodos = [
        evento for evento in resultado["historial"]
        if evento.get("tipo") == "nodo"
    ]
    camino_solucion = set(resultado["camino_solucion"])
    nodos_camino = [
        nodo for nodo in nodos if nodo["nodo"] in camino_solucion
    ]
    if len(nodos_camino) > max_nodos:
        nodos_camino = nodos_camino[-max_nodos:]
    nodos_visibles = list(nodos_camino)
    ids_visibles = {nodo["nodo"] for nodo in nodos_visibles}
    for nodo in nodos:
        if len(nodos_visibles) >= max_nodos:
            break
        if nodo["nodo"] not in ids_visibles:
            nodos_visibles.append(nodo)
            ids_visibles.add(nodo["nodo"])
    nodos_visibles = nodos_visibles[:max_nodos]

    eje = ejes[0, 0]
    por_nivel = {}
    for nodo in nodos_visibles:
        por_nivel.setdefault(nodo["profundidad"], []).append(nodo)
    posiciones = {}
    for profundidad, nivel in por_nivel.items():
        total = len(nivel)
        for indice, nodo in enumerate(nivel):
            x = 0.5 if total == 1 else indice / (total - 1)
            posiciones[nodo["nodo"]] = (x, -profundidad)

    for nodo in nodos_visibles:
        padre = nodo["padre"]
        if padre not in posiciones:
            continue
        x1, y1 = posiciones[padre]
        x2, y2 = posiciones[nodo["nodo"]]
        eje.plot(
            [x1, x2],
            [y1, y2],
            color="#c65d3a" if nodo["podada"] else "#9a9a92",
            linewidth=1.1,
            zorder=1,
        )
    leyenda = set()
    for nodo in nodos_visibles:
        if nodo["solucion_final"]:
            color, etiqueta, marcador = "#e0a52b", "Solución final", "*"
        elif nodo["podada"]:
            color, etiqueta, marcador = "#c65d3a", "Rama podada", "X"
        else:
            color, etiqueta, marcador = "#26734d", "Explorada", "o"
        eje.scatter(
            *posiciones[nodo["nodo"]],
            color=color,
            marker=marcador,
            s=75 if marcador != "*" else 150,
            label=etiqueta if etiqueta not in leyenda else None,
            zorder=2,
        )
        leyenda.add(etiqueta)
        detalle = nodo["decision"]
        if nodo["id_incidencia"] is not None:
            detalle += f"\nID {nodo['id_incidencia']}"
        eje.annotate(
            detalle,
            posiciones[nodo["nodo"]],
            xytext=(3, 5),
            textcoords="offset points",
            fontsize=6,
        )
    if nodos_visibles:
        eje.set_ylim(-max(n["profundidad"] for n in nodos_visibles) - 1, 1)
    else:
        eje.text(0.5, 0.5, "Sin nodos registrados", ha="center")
    eje.set_title(
        f"Árbol de decisiones: {len(nodos_visibles)} de "
        f"{resultado['nodos_explorados']} nodos"
    )
    eje.axis("off")
    if leyenda:
        eje.legend(loc="lower right", fontsize=7)

    eje = ejes[0, 1]
    soluciones = resultado["soluciones"]
    if soluciones:
        puntos = eje.scatter(
            [solucion["cantidad"] for solucion in soluciones],
            [solucion["tiempo"] for solucion in soluciones],
            c=[solucion["prioridad"] for solucion in soluciones],
            cmap="viridis",
            alpha=0.65,
            label="Combinaciones evaluadas",
        )
        figura.colorbar(puntos, ax=eje, label="Prioridad total")
    else:
        eje.text(0.5, 0.5, "Sin combinaciones evaluadas", ha="center")
    eje.scatter(
        len(resultado["seleccionadas"]),
        resultado["tiempo_usado"],
        marker="*",
        s=220,
        color="#e0a52b",
        edgecolor="black",
        label="Mejor Backtracking",
        zorder=4,
    )
    prioridad_voraz = sum(
        incidencia["prioridad"] for incidencia in plan_voraz["seleccionadas"]
    )
    eje.scatter(
        len(plan_voraz["seleccionadas"]),
        plan_voraz["tiempo_usado"],
        marker="^",
        s=100,
        color="#4d83a8",
        label=f"Greedy ({tiempo_voraz:.6f} s)",
        zorder=3,
    )
    eje.set_title(
        f"Soluciones: muestra {len(soluciones)} de "
        f"{resultado['soluciones_totales']} (Backtracking: "
        f"{tiempo_backtracking:.6f} s)"
    )
    eje.set_xlabel("Incidencias atendidas")
    eje.set_ylabel("Minutos de mantenimiento")
    eje.legend(fontsize=7)
    eje.text(
        0.02,
        0.98,
        f"Prioridad Greedy: {prioridad_voraz}",
        transform=eje.transAxes,
        va="top",
        fontsize=8,
    )

    eje = ejes[1, 0]
    nombres_metricas = ("Nodos", "Podas", "Retrocesos")
    valores_metricas = (
        resultado["nodos_explorados"],
        resultado["ramas_podadas"],
        resultado["retrocesos"],
    )
    barras = eje.bar(
        nombres_metricas,
        valores_metricas,
        color=("#4d83a8", "#c65d3a", "#d7a05d"),
    )
    eje.bar_label(barras, padding=3)
    eje.set_title("Exploración de la búsqueda")
    eje.set_ylabel("Cantidad")

    eje = ejes[1, 1]
    disponible = resultado["tiempo_disponible"]
    usado = resultado["tiempo_usado"]
    restante = resultado["tiempo_restante"]
    if disponible:
        eje.pie(
            [usado, restante],
            labels=["Utilizado", "Restante"],
            autopct="%1.1f%%",
            colors=["#26734d", "#ded8c8"],
            startangle=90,
        )
    else:
        eje.text(0.5, 0.55, "0 min disponibles", ha="center")
        eje.text(0.5, 0.4, "0 min utilizados", ha="center")
    eje.set_title(
        f"Tiempo: {usado} usado / {restante} restante de {disponible} min"
    )

    figura.tight_layout()
    plt.show()