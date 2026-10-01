import tkinter as tk
import time
from tkinter import messagebox, simpledialog, ttk

from core import metodos as servicio
from interfaz.graficos import (
    mostrar_graficos_backtracking,
    mostrar_graficos_planificacion,
)


AYUDA_ESTADOS = {
    "Pendiente": "Pendiente: el equipo espera atención. Al iniciar, registra la revisión o tarea que realizaste.",
    "En proceso": "En proceso: el mantenimiento está en curso. Al finalizar, describe las tareas realizadas y el resultado.",
    "Finalizado": "Finalizado: mantenimiento cerrado. El estado no puede retroceder."
}


class MantenimientoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de mantenimiento de equipos")
        self.root.geometry("1120x760")
        self.root.minsize(900, 620)

        estilo = ttk.Style(root)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=27)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))

        encabezado = ttk.Frame(root, padding=(18, 14, 18, 8))
        encabezado.pack(fill="x")
        ttk.Label(
            encabezado,
            text="Mantenimiento de equipos",
            style="Title.TLabel"
        ).pack(side="left")
        ttk.Button(
            encabezado,
            text="Actualizar listas",
            command=self.actualizar_listas
        ).pack(side="right")

        self.pestanas = ttk.Notebook(root)
        self.pestanas.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.tab_incidencias = ttk.Frame(self.pestanas, padding=12)
        self.tab_planificacion = ttk.Frame(self.pestanas, padding=18)
        self.tab_backtracking = ttk.Frame(self.pestanas, padding=18)
        self.tab_equipos = ttk.Frame(self.pestanas, padding=12)
        self.tab_nuevo_equipo = ttk.Frame(self.pestanas, padding=18)
        self.tab_nueva_incidencia = ttk.Frame(self.pestanas, padding=18)
        self.pestanas.add(self.tab_incidencias, text="Incidencias")
        self.pestanas.add(self.tab_planificacion, text="Planificación voraz")
        self.pestanas.add(self.tab_backtracking, text="Backtracking")
        self.pestanas.add(self.tab_equipos, text="Equipos")
        self.pestanas.add(self.tab_nuevo_equipo, text="Registrar equipo")
        self.pestanas.add(self.tab_nueva_incidencia, text="Registrar incidencia")

        self._crear_tab_incidencias()
        self._crear_tab_planificacion()
        self._crear_tab_backtracking()
        self._crear_tab_equipos()
        self._crear_formulario_equipo()
        self._crear_formulario_incidencia()
        self.actualizar_listas()

    def _crear_tab_incidencias(self):
        barra = ttk.Frame(self.tab_incidencias)
        barra.pack(fill="x", pady=(0, 8))
        ttk.Label(barra, text="Filtrar incidencias").pack(side="left")
        self.filtro = tk.StringVar()
        entrada = ttk.Entry(barra, textvariable=self.filtro, width=32)
        entrada.pack(side="left", padx=8)
        self.filtro.trace_add("write", lambda *_: self._cargar_incidencias())
        ttk.Button(
            barra,
            text="Avanzar estado",
            command=self.avanzar_estado
        ).pack(side="right")

        columnas = ("id", "sku", "problema", "tipo", "prioridad", "estado")
        self.tabla_incidencias = ttk.Treeview(
            self.tab_incidencias,
            columns=columnas,
            show="headings",
            height=12
        )
        nombres = {
            "id": ("ID", 55),
            "sku": ("SKU", 100),
            "problema": ("Problema", 380),
            "tipo": ("Mantenimiento", 130),
            "prioridad": ("Prioridad", 75),
            "estado": ("Estado", 110)
        }
        for columna, (titulo, ancho) in nombres.items():
            self.tabla_incidencias.heading(columna, text=titulo)
            self.tabla_incidencias.column(columna, width=ancho, anchor="w")
        self.tabla_incidencias.pack(fill="both", expand=True)
        self.tabla_incidencias.bind(
            "<<TreeviewSelect>>",
            lambda _evento: self._mostrar_detalle()
        )

        ttk.Label(
            self.tab_incidencias,
            text="Historial del mantenimiento",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(12, 5))
        self.detalle = tk.Text(
            self.tab_incidencias,
            height=8,
            wrap="word",
            font=("Segoe UI", 9),
            state="disabled"
        )
        self.detalle.pack(fill="x")
        self.ayuda_estado = ttk.Label(
            self.tab_incidencias,
            text="El flujo avanza: Pendiente → En proceso → Finalizado.",
            wraplength=900
        )
        self.ayuda_estado.pack(anchor="w", pady=(8, 0))

    def _crear_tab_equipos(self):
        columnas = ("id", "sku", "tipo", "marca", "modelo", "usuario", "estado")
        self.tabla_equipos = ttk.Treeview(
            self.tab_equipos,
            columns=columnas,
            show="headings"
        )
        for columna, titulo, ancho in (
            ("id", "ID", 55),
            ("sku", "SKU", 100),
            ("tipo", "Tipo", 130),
            ("marca", "Marca", 100),
            ("modelo", "Modelo", 150),
            ("usuario", "Usuario", 140),
            ("estado", "Estado", 130)
        ):
            self.tabla_equipos.heading(columna, text=titulo)
            self.tabla_equipos.column(columna, width=ancho, anchor="w")
        self.tabla_equipos.pack(fill="both", expand=True)

    def _crear_tab_planificacion(self):
        ttk.Label(
            self.tab_planificacion,
            text="Planificar mantenimiento con algoritmo voraz",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(
            self.tab_planificacion,
            text=(
                "Ordena por prioridad descendente; para prioridades iguales, "
                "usa menor duración e ID. Solo selecciona trabajos que caben "
                "en el tiempo disponible."
            ),
            wraplength=900
        ).pack(anchor="w", pady=(0, 12))

        controles = ttk.Frame(self.tab_planificacion)
        controles.pack(fill="x", pady=(0, 12))
        ttk.Label(controles, text="Tiempo del técnico (minutos)").pack(side="left")
        self.tiempo_disponible_plan = tk.StringVar(value="120")
        ttk.Spinbox(
            controles,
            from_=1,
            to=100000,
            textvariable=self.tiempo_disponible_plan,
            width=10
        ).pack(side="left", padx=8)
        ttk.Button(
            controles,
            text="Calcular plan",
            command=self.calcular_plan_voraz
        ).pack(side="left", padx=(0, 8))
        self.boton_graficos = ttk.Button(
            controles,
            text="Ver gráficos",
            command=self.mostrar_graficos_plan,
            state="disabled"
        )
        self.boton_graficos.pack(side="left")

        self.resultado_plan = tk.Text(
            self.tab_planificacion,
            height=24,
            wrap="word",
            font=("Consolas", 9),
            state="disabled"
        )
        self.resultado_plan.pack(fill="both", expand=True)
        self.planes_calculados = None

    def _crear_tab_backtracking(self):
        ttk.Label(
            self.tab_backtracking,
            text="Planificar mantenimiento con Backtracking",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 8))
        ttk.Label(
            self.tab_backtracking,
            text=(
                "Busca la combinación que atiende más incidencias; desempata "
                "por prioridad total (suma de valores 1-5) y luego menor "
                "tiempo de mantenimiento. Peor caso O(2^n); la poda puede "
                "reducir nodos, pero no elimina ese peor caso."
            ),
            wraplength=900
        ).pack(anchor="w", pady=(0, 12))

        controles = ttk.Frame(self.tab_backtracking)
        controles.pack(fill="x", pady=(0, 12))
        ttk.Label(controles, text="Tiempo del técnico (minutos)").pack(side="left")
        self.tiempo_disponible_backtracking = tk.StringVar(value="120")
        ttk.Spinbox(
            controles,
            from_=0,
            to=100000,
            textvariable=self.tiempo_disponible_backtracking,
            width=10
        ).pack(side="left", padx=8)
        ttk.Button(
            controles,
            text="Calcular solución",
            command=self.calcular_plan_backtracking
        ).pack(side="left", padx=(0, 8))
        self.boton_historial_backtracking = ttk.Button(
            controles,
            text="Ver historial",
            command=self.mostrar_historial_backtracking,
            state="disabled"
        )
        self.boton_historial_backtracking.pack(side="left", padx=(0, 8))
        self.boton_graficos_backtracking = ttk.Button(
            controles,
            text="Ver gráficos",
            command=self.mostrar_graficos_backtracking_gui,
            state="disabled"
        )
        self.boton_graficos_backtracking.pack(side="left")

        self.resultado_backtracking = tk.Text(
            self.tab_backtracking,
            height=24,
            wrap="word",
            font=("Consolas", 9),
            state="disabled"
        )
        self.resultado_backtracking.pack(fill="both", expand=True)
        self.resultados_backtracking = None

    def calcular_plan_backtracking(self):
        try:
            tiempo_disponible = int(
                self.tiempo_disponible_backtracking.get()
            )
            if tiempo_disponible < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Tiempo inválido",
                "Ingresa un número entero de minutos igual o mayor que cero."
            )
            return

        inicio = time.perf_counter()
        backtracking = servicio.planificar_backtracking_detallado(
            tiempo_disponible
        )
        tiempo_backtracking = time.perf_counter() - inicio
        inicio = time.perf_counter()
        voraz = servicio.planificar_voraz_detallado(
            tiempo_disponible,
            pendientes=backtracking["incidencias_pendientes"],
        )
        tiempo_voraz = time.perf_counter() - inicio
        self.resultados_backtracking = (
            backtracking,
            voraz,
            tiempo_backtracking,
            tiempo_voraz,
        )

        seleccionadas = backtracking["seleccionadas"]
        prioridades_backtracking = sum(
            incidencia["prioridad"] for incidencia in seleccionadas
        )
        prioridades_voraz = sum(
            incidencia["prioridad"]
            for incidencia in voraz["seleccionadas"]
        )
        lineas = ["MEJOR COMBINACIÓN ENCONTRADA"]
        if seleccionadas:
            for posicion, incidencia in enumerate(seleccionadas, 1):
                lineas.append(
                    f"{posicion}. ID {incidencia['id']} | "
                    f"{incidencia.get('sku_equipo', 'Sin SKU')} | "
                    f"{incidencia.get('problema', 'Sin descripción')} | "
                    f"Prioridad {incidencia['prioridad']} | "
                    f"{incidencia['tiempo_estimado']} min"
                )
        else:
            lineas.append("Ninguna incidencia cabe en el tiempo disponible.")

        lineas.extend(("", "NO SELECCIONADAS"))
        lineas.extend(
            f"ID {incidencia['id']} | "
            f"{incidencia.get('sku_equipo', 'Sin SKU')} | "
            f"{incidencia['tiempo_estimado']} min"
            for incidencia in backtracking["no_seleccionadas"]
        )
        if not backtracking["no_seleccionadas"]:
            lineas.append("Ninguna.")

        lineas.extend(("", "COMPARACIÓN CON GREEDY"))
        lineas.append(
            f"Backtracking: {len(seleccionadas)} incidencias, "
            f"prioridad {prioridades_backtracking}, "
            f"{backtracking['tiempo_usado']} min usados, "
            f"{backtracking['tiempo_restante']} min restantes, "
            f"{tiempo_backtracking:.8f} s de ejecución."
        )
        lineas.append(
            f"  Distribución de prioridades: "
            f"{self._resumen_prioridades(seleccionadas)}"
        )
        lineas.append(
            f"Greedy: {len(voraz['seleccionadas'])} incidencias, "
            f"prioridad {prioridades_voraz}, {voraz['tiempo_usado']} min usados, "
            f"{voraz['tiempo_restante']} min restantes, "
            f"{tiempo_voraz:.8f} s de ejecución."
        )
        lineas.append(
            f"  Distribución de prioridades: "
            f"{self._resumen_prioridades(voraz['seleccionadas'])}"
        )
        lineas.extend(("", "EXPLORACIÓN"))
        lineas.append(
            f"Nodos: {backtracking['nodos_explorados']} | "
            f"Soluciones: {backtracking['soluciones_evaluadas']} | "
            f"Retrocesos: {backtracking['retrocesos']} | "
            f"Podas: {backtracking['ramas_podadas']} "
            f"(tiempo {backtracking['podas_por_tiempo']}, "
            f"cota {backtracking['podas_por_cota']})."
        )
        if backtracking["historial_truncado"]:
            lineas.append(
                f"Historial limitado a {len(backtracking['historial'])} de "
                f"{backtracking['eventos_totales']} eventos."
            )
        lineas.append(
            "La búsqueda puede explorar O(2^n) nodos en el peor caso; "
            "Backtracking optimiza la función objetivo, no garantiza menor "
            "tiempo de ejecución que Greedy."
        )

        self.resultado_backtracking.configure(state="normal")
        self.resultado_backtracking.delete("1.0", "end")
        self.resultado_backtracking.insert("end", "\n".join(lineas))
        self.resultado_backtracking.configure(state="disabled")
        self.boton_historial_backtracking.configure(state="normal")
        self.boton_graficos_backtracking.configure(state="normal")

    def mostrar_historial_backtracking(self):
        if self.resultados_backtracking is None:
            return
        resultado = self.resultados_backtracking[0]
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Backtracking")
        ventana.geometry("850x560")
        texto = tk.Text(ventana, wrap="none", font=("Consolas", 9))
        texto.pack(fill="both", expand=True)
        for evento in resultado["historial"][:200]:
            if evento["tipo"] == "nodo":
                texto.insert(
                    "end",
                    f"Nodo {evento['nodo']} | padre {evento['padre']} | "
                    f"profundidad {evento['profundidad']} | "
                    f"ID {evento['id_incidencia']} | {evento['decision']} | "
                    f"tiempo {evento['tiempo_acumulado']} | "
                    f"seleccionadas {evento['seleccionadas']} | "
                    f"mejor {evento['mejor_cantidad']}/"
                    f"{evento['mejor_prioridad']}/{evento['mejor_tiempo']}"
                    + (
                        f" | PODA: {evento.get('motivo_poda')}"
                        if evento.get("podada") else ""
                    )
                    + "\n"
                )
            else:
                texto.insert(
                    "end",
                    f"Retroceso en nodo {evento['nodo']} tras ID "
                    f"{evento['id_incidencia']}\n"
                )
        if resultado["historial_truncado"] or len(resultado["historial"]) > 200:
            texto.insert(
                "end",
                "\nDetalle limitado; el resumen conserva los totales de toda la búsqueda.\n"
            )
        texto.configure(state="disabled")

    def mostrar_graficos_backtracking_gui(self):
        if self.resultados_backtracking is None:
            return
        try:
            mostrar_graficos_backtracking(*self.resultados_backtracking)
        except ImportError:
            messagebox.showerror(
                "Falta Matplotlib",
                "Instala las dependencias con: python -m pip install -r requirements.txt"
            )

    @staticmethod
    def _resumen_prioridades(incidencias):
        nombres = {
            1: "Baja",
            2: "Media",
            3: "Normal",
            4: "Alta",
            5: "Crítica",
        }
        cantidades = {prioridad: 0 for prioridad in nombres}
        for incidencia in incidencias:
            prioridad = incidencia["prioridad"]
            if prioridad in cantidades:
                cantidades[prioridad] += 1
        return ", ".join(
            f"{nombres[prioridad]}: {cantidad}"
            for prioridad, cantidad in cantidades.items()
        )

    def calcular_plan_voraz(self):
        try:
            tiempo_disponible = int(self.tiempo_disponible_plan.get())
            if tiempo_disponible < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Tiempo inválido",
                "Ingresa un número entero de minutos mayor que cero."
            )
            return

        inicio = time.perf_counter()
        plan_prioridad = servicio.planificar_voraz_detallado(tiempo_disponible)
        plan_menor_tiempo = servicio.planificar_voraz_detallado(
            tiempo_disponible,
            criterio="tiempo"
        )
        tiempo_ejecucion = time.perf_counter() - inicio
        self.planes_calculados = (plan_prioridad, plan_menor_tiempo)

        lineas = ["DECISIONES DEL PLAN VORAZ"]
        if not plan_prioridad["decisiones"]:
            lineas.append("No hay incidencias pendientes.")
        for decision in plan_prioridad["decisiones"]:
            incidencia = decision["incidencia"]
            estado = "SELECCIONADA" if decision["seleccionada"] else "DESCARTADA"
            lineas.append(
                f"ID {incidencia['id']} | {incidencia['sku_equipo']} | "
                f"Prioridad {incidencia['prioridad']} | "
                f"{incidencia['tiempo_estimado']} min | {estado}"
            )
            lineas.append(f"  {decision['motivo']}")

        lineas.extend(("", "ORDEN DE ATENCIÓN"))
        for posicion, incidencia in enumerate(
            plan_prioridad["seleccionadas"],
            1
        ):
            lineas.append(
                f"{posicion}. ID {incidencia['id']} | "
                f"{incidencia['sku_equipo']} | {incidencia['problema']} | "
                f"{incidencia['tiempo_estimado']} min"
            )
        if not plan_prioridad["seleccionadas"]:
            lineas.append("Ninguna incidencia cabe en el tiempo disponible.")

        lineas.extend(("", "RESUMEN DE TIEMPO DE MANTENIMIENTO"))
        lineas.append(f"Disponible: {tiempo_disponible} min")
        lineas.append(f"Utilizado: {plan_prioridad['tiempo_usado']} min")
        lineas.append(f"Restante: {plan_prioridad['tiempo_restante']} min")
        lineas.append(
            f"Ejecución de los algoritmos: {tiempo_ejecucion:.8f} s "
            "(no es tiempo de mantenimiento)."
        )
        lineas.extend(("", "COMPARACIÓN DE ESTRATEGIAS"))
        for nombre, resultado in (
            ("Prioridad y duración", plan_prioridad),
            ("Menor duración primero", plan_menor_tiempo),
        ):
            lineas.append(
                f"{nombre}: {len(resultado['seleccionadas'])} seleccionadas, "
                f"{resultado['tiempo_usado']} min usados, "
                f"{resultado['tiempo_restante']} min restantes."
            )
            lineas.append(
                "  Prioridades: "
                f"{self._resumen_prioridades(resultado['seleccionadas'])}"
            )

        self.resultado_plan.configure(state="normal")
        self.resultado_plan.delete("1.0", "end")
        self.resultado_plan.insert("end", "\n".join(lineas))
        self.resultado_plan.configure(state="disabled")
        self.boton_graficos.configure(state="normal")

    def mostrar_graficos_plan(self):
        if self.planes_calculados is None:
            messagebox.showinfo("Primero calcula el plan", "Calcula una planificación antes de ver sus gráficos.")
            return
        mostrar_graficos_planificacion(*self.planes_calculados)

    def _crear_formulario_equipo(self):
        ttk.Label(
            self.tab_nuevo_equipo,
            text="Registrar equipo",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 18))
        self.campos_equipo = {}
        for clave, etiqueta in (
            ("sku", "SKU"),
            ("tipo", "Tipo de equipo"),
            ("marca", "Marca"),
            ("modelo", "Modelo"),
            ("usuario", "Usuario asignado"),
            ("equipo", "Identificación del equipo")
        ):
            self.campos_equipo[clave] = self._campo(
                self.tab_nuevo_equipo,
                etiqueta
            )
        ttk.Button(
            self.tab_nuevo_equipo,
            text="Guardar equipo",
            command=self.registrar_equipo
        ).pack(anchor="w", pady=14)

    def _crear_formulario_incidencia(self):
        ttk.Label(
            self.tab_nueva_incidencia,
            text="Registrar incidencia",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 18))
        self.sku_incidencia = tk.StringVar()
        fila_sku = ttk.Frame(self.tab_nueva_incidencia)
        fila_sku.pack(fill="x", pady=6)
        ttk.Label(fila_sku, text="SKU del equipo", width=25).pack(side="left")
        self.selector_sku = ttk.Combobox(
            fila_sku,
            textvariable=self.sku_incidencia,
            state="readonly",
            width=45
        )
        self.selector_sku.pack(side="left", fill="x", expand=True)
        self.problema = self._campo(
            self.tab_nueva_incidencia,
            "Problema detectado"
        )
        fila = ttk.Frame(self.tab_nueva_incidencia)
        fila.pack(fill="x", pady=6)
        ttk.Label(fila, text="Tipo de mantenimiento", width=25).pack(side="left")
        self.tipo_mantenimiento = tk.StringVar(value="Correctivo")
        ttk.Combobox(
            fila,
            textvariable=self.tipo_mantenimiento,
            values=("Preventivo", "Correctivo", "Predictivo"),
            state="readonly",
            width=28
        ).pack(side="left")

        fila = ttk.Frame(self.tab_nueva_incidencia)
        fila.pack(fill="x", pady=6)
        ttk.Label(fila, text="Prioridad", width=25).pack(side="left")
        self.prioridad = tk.StringVar(value="3")
        ttk.Combobox(
            fila,
            textvariable=self.prioridad,
            values=("1 - Baja", "2 - Media", "3 - Normal", "4 - Alta", "5 - Crítica"),
            state="readonly",
            width=28
        ).pack(side="left")
        self.prioridad.set("3 - Normal")

        fila = ttk.Frame(self.tab_nueva_incidencia)
        fila.pack(fill="x", pady=6)
        ttk.Label(fila, text="Tiempo estimado", width=25).pack(side="left")
        self.horas = tk.StringVar(value="0")
        self.minutos = tk.StringVar(value="30")
        ttk.Spinbox(fila, from_=0, to=999, textvariable=self.horas, width=6).pack(side="left")
        ttk.Label(fila, text="horas").pack(side="left", padx=(5, 14))
        ttk.Spinbox(fila, from_=0, to=59, textvariable=self.minutos, width=6).pack(side="left")
        ttk.Label(fila, text="minutos").pack(side="left", padx=5)
        ttk.Label(
            self.tab_nueva_incidencia,
            text="La incidencia inicia Pendiente; registra el trabajo realizado al avanzar cada estado.",
            wraplength=800
        ).pack(anchor="w", pady=(12, 4))
        ttk.Button(
            self.tab_nueva_incidencia,
            text="Guardar incidencia",
            command=self.registrar_incidencia
        ).pack(anchor="w", pady=10)

    @staticmethod
    def _campo(contenedor, etiqueta, variable=None):
        fila = ttk.Frame(contenedor)
        fila.pack(fill="x", pady=6)
        ttk.Label(fila, text=etiqueta, width=25).pack(side="left")
        entrada = ttk.Entry(fila, textvariable=variable, width=48)
        entrada.pack(side="left", fill="x", expand=True)
        return entrada

    def actualizar_listas(self):
        self._cargar_incidencias()
        self._cargar_equipos()
        disponibles = [
            equipo["sku"]
            for equipo in servicio.equipos
            if not servicio.equipo_tiene_incidencia_abierta(equipo["sku"])
        ]
        self.selector_sku.configure(values=disponibles)

    def _cargar_incidencias(self):
        if not hasattr(self, "tabla_incidencias"):
            return
        filtro = self.filtro.get().strip().casefold()
        self.tabla_incidencias.delete(*self.tabla_incidencias.get_children())
        for incidencia in servicio.incidencias:
            valores = (
                incidencia["id"],
                incidencia["sku_equipo"],
                incidencia["problema"],
                incidencia["tipo_mantenimiento"],
                incidencia["prioridad"],
                incidencia["estado"]
            )
            if filtro and filtro not in " ".join(map(str, valores)).casefold():
                continue
            self.tabla_incidencias.insert("", "end", iid=str(incidencia["id"]), values=valores)

    def _cargar_equipos(self):
        self.tabla_equipos.delete(*self.tabla_equipos.get_children())
        for equipo in servicio.equipos:
            self.tabla_equipos.insert(
                "",
                "end",
                values=(
                    equipo["id"], equipo["sku"], equipo["tipo"],
                    equipo["marca"], equipo["modelo"], equipo["usuario"],
                    equipo["estado"]
                )
            )

    def _mostrar_detalle(self):
        seleccion = self.tabla_incidencias.selection()
        if not seleccion:
            return
        incidencia = servicio.buscar_incidencia(int(seleccion[0]))
        self.detalle.configure(state="normal")
        self.detalle.delete("1.0", "end")
        self.detalle.insert(
            "end",
            f"{incidencia['sku_equipo']} · {incidencia['problema']}\n"
            f"Estado actual: {incidencia['estado']}\n\n"
        )
        historial = incidencia.get("historial_mantenimiento", [])
        if not historial:
            self.detalle.insert("end", "Sin detalle de mantenimiento registrado.\n")
        for registro in historial:
            self.detalle.insert(
                "end",
                f"{registro['estado']}: {registro['detalle']}\n"
            )
        self.detalle.configure(state="disabled")
        self.ayuda_estado.configure(text=AYUDA_ESTADOS[incidencia["estado"]])

    def avanzar_estado(self):
        seleccion = self.tabla_incidencias.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona una incidencia", "Selecciona una fila para continuar.")
            return
        incidencia = servicio.buscar_incidencia(int(seleccion[0]))
        siguiente = {
            "Pendiente": "En proceso",
            "En proceso": "Finalizado"
        }.get(incidencia["estado"])
        if siguiente is None:
            messagebox.showinfo("Incidencia finalizada", AYUDA_ESTADOS["Finalizado"])
            return

        detalle = simpledialog.askstring(
            f"Avanzar a {siguiente}",
            f"{AYUDA_ESTADOS[incidencia['estado']]}\n\n"
            "Describe el mantenimiento realizado (10 a 500 caracteres):",
            parent=self.root
        )
        if detalle is None:
            return
        if not 10 <= len(detalle.strip()) <= 500:
            messagebox.showerror("Detalle inválido", "Escribe entre 10 y 500 caracteres.")
            return
        if not servicio.actualizar_estado(incidencia["id"], siguiente, detalle):
            messagebox.showerror("No se pudo actualizar", "La transición o el detalle no son válidos.")
            return
        self.actualizar_listas()
        self.tabla_incidencias.selection_set(str(incidencia["id"]))
        self._mostrar_detalle()

    def registrar_equipo(self):
        datos = [self.campos_equipo[clave].get().strip() for clave in (
            "sku", "tipo", "marca", "modelo", "usuario", "equipo"
        )]
        if not servicio.datos_equipo_validos(*datos):
            messagebox.showerror("Datos inválidos", "Revisa los campos y sus longitudes/formato.")
            return
        resultado = servicio.registrar_equipo(*datos)
        if not resultado:
            messagebox.showerror("No se pudo registrar", "El SKU ya existe o los datos no son válidos.")
            return
        for entrada in self.campos_equipo.values():
            entrada.delete(0, "end")
        self.actualizar_listas()
        messagebox.showinfo("Equipo registrado", f"Equipo {resultado['sku']} guardado.")

    def registrar_incidencia(self):
        sku = self.sku_incidencia.get().strip()
        problema = self.problema.get().strip()
        if not servicio.problema_valido(problema):
            messagebox.showerror("Problema inválido", "Describe el problema en 10 a 250 caracteres.")
            return
        try:
            prioridad = int(self.prioridad.get().split(" - ", 1)[0])
            tiempo = int(self.horas.get()) * 60 + int(self.minutos.get())
        except ValueError:
            messagebox.showerror("Datos inválidos", "Prioridad y tiempo deben ser números enteros.")
            return
        resultado = servicio.registrar_incidencia(
            sku,
            problema,
            self.tipo_mantenimiento.get(),
            prioridad,
            tiempo
        )
        if not resultado:
            messagebox.showerror(
                "No se pudo registrar",
                "Verifica que el SKU exista, no tenga una incidencia abierta y el tiempo sea mayor que cero."
            )
            return
        self.problema.delete(0, "end")
        self.actualizar_listas()
        self.pestanas.select(self.tab_incidencias)
        self.tabla_incidencias.selection_set(str(resultado["id"]))
        self._mostrar_detalle()
        messagebox.showinfo("Incidencia registrada", f"Incidencia {resultado['id']} guardada como Pendiente.")


def iniciar_gui():
    root = tk.Tk()
    MantenimientoGUI(root)
    root.mainloop()