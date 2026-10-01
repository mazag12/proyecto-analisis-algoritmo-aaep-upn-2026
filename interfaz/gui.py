import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from core import metodos as servicio


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
        self.tab_equipos = ttk.Frame(self.pestanas, padding=12)
        self.tab_nuevo_equipo = ttk.Frame(self.pestanas, padding=18)
        self.tab_nueva_incidencia = ttk.Frame(self.pestanas, padding=18)
        self.pestanas.add(self.tab_incidencias, text="Incidencias")
        self.pestanas.add(self.tab_equipos, text="Equipos")
        self.pestanas.add(self.tab_nuevo_equipo, text="Registrar equipo")
        self.pestanas.add(self.tab_nueva_incidencia, text="Registrar incidencia")

        self._crear_tab_incidencias()
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