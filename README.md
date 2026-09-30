# 🖥️ Sistema de Mantenimiento de Equipos Informáticos

Sistema desarrollado en **Python** para gestionar equipos informáticos y controlar las incidencias relacionadas con su mantenimiento.

El proyecto permite registrar equipos, registrar incidencias, consultar información, ordenar incidencias según diferentes criterios, planificar mantenimientos, actualizar estados y obtener estadísticas generales del sistema.

Además, el proyecto tiene como propósito aplicar conceptos de **programación estructurada, validación de datos, funciones, listas, diccionarios, búsqueda, ordenamiento y medición de tiempos de ejecución mediante algoritmos**.

---

## 🎯 Propósito del sistema

El propósito principal del sistema es proporcionar una herramienta sencilla para llevar el control de los equipos informáticos y las incidencias de mantenimiento que presentan.

El sistema busca facilitar:

* El registro y consulta de equipos.
* La identificación de equipos mediante códigos únicos.
* El registro de problemas o incidencias.
* La clasificación de los mantenimientos.
* La asignación de prioridades.
* La estimación del tiempo necesario para atender una incidencia.
* La planificación del orden de atención.
* El seguimiento del estado de las incidencias.
* La generación de estadísticas.
* La demostración y comparación de algoritmos de ordenamiento.

Este proyecto también sirve como práctica para comprender cómo pueden aplicarse algoritmos y estructuras de datos a un problema real de gestión.

---

## 🚀 Funcionalidades

El sistema dispone de un menú principal con las siguientes opciones:

### 1. Registrar equipo

Permite registrar un nuevo equipo informático solicitando:

* SKU
* Tipo
* Marca
* Modelo
* Usuario
* Identificación del equipo

El sistema asigna automáticamente:

* ID del equipo.
* Estado inicial: `Operativo`.

También se verifica que el SKU no esté registrado previamente, sin distinguir mayúsculas y minúsculas.

### 2. Registrar incidencia

Permite registrar una incidencia asociada a un equipo existente.

Para cada incidencia se registra:

* SKU del equipo.
* Problema detectado.
* Tipo de mantenimiento.
* Prioridad.
* Tiempo estimado de atención.

Los tipos de mantenimiento disponibles son:

* **Preventivo**
* **Correctivo**
* **Predictivo**

Las prioridades disponibles son:

| Nivel | Prioridad |
| ----: | --------- |
|     1 | Baja      |
|     2 | Media     |
|     3 | Normal    |
|     4 | Alta      |
|     5 | Crítica   |

Al registrar una incidencia, el estado inicial es:

`Pendiente`

Además, el estado del equipo pasa a:

`En mantenimiento`

Un equipo solo puede tener una incidencia pendiente o en proceso a la vez.

---

### 3. Mostrar equipos

Muestra todos los equipos registrados junto con su información:

* ID
* SKU
* Tipo
* Marca
* Modelo
* Usuario
* Identificación del equipo
* Estado

---

### 4. Mostrar incidencias

Muestra todas las incidencias registradas indicando:

* ID
* Equipo afectado
* Problema
* Tipo de mantenimiento
* Prioridad
* Tiempo estimado
* Estado

---

### 5. Buscar equipo

Permite buscar un equipo mediante su SKU.

Si el equipo existe, se muestra toda su información.

Si no existe, el sistema informa que no se encontró ningún equipo con ese código.

---

### 6. Ordenar incidencias por prioridad

Utiliza el algoritmo de **ordenamiento burbuja (Bubble Sort)** para ordenar las incidencias desde la prioridad más alta hasta la más baja.

Ejemplo:

```text
Prioridad 5
Prioridad 4
Prioridad 3
Prioridad 2
Prioridad 1
```

También se mide el tiempo de ejecución del algoritmo utilizando:

```python
time.perf_counter()
```

---

### 7. Ordenar incidencias por tiempo

Ordena las incidencias según el tiempo estimado de atención, desde el menor hasta el mayor.

Ejemplo:

```text
30 minutos
45 minutos
60 minutos
```

También se calcula el tiempo de ejecución del algoritmo.

---

### 8. Planificar mantenimiento

Genera un orden recomendado para atender las incidencias que se encuentran en estado:

`Pendiente`

La planificación utiliza un **algoritmo voraz**. En cada paso elige la incidencia pendiente con mayor prioridad; si hay empate, prefiere la de menor duración y luego el menor ID.

Es una regla práctica para decidir qué atender primero, no una promesa de que el resultado sea el mejor posible para cualquier escenario.

---

### 9. Actualizar estado

Permite modificar el estado de una incidencia.

Estados disponibles:

* `Pendiente`
* `En proceso`
* `Finalizado`

El sistema también actualiza automáticamente el estado del equipo relacionado.

Por ejemplo:

```text
Incidencia → En proceso
Equipo → En mantenimiento
```

Cuando la incidencia finaliza:

```text
Incidencia → Finalizado
Equipo → Operativo
```

---

### 10. Mostrar estadísticas

Muestra información general del sistema:

* Total de equipos.
* Total de incidencias.
* Incidencias pendientes.
* Incidencias en proceso.
* Incidencias finalizadas.
* Cantidad de mantenimientos preventivos.
* Cantidad de mantenimientos correctivos.
* Cantidad de mantenimientos predictivos.
* Tiempo total estimado.
* Tiempo promedio de atención.

Ejemplo:

```text
Total de equipos       : 3
Total de incidencias   : 3
Pendientes             : 3
En proceso             : 0
Finalizadas            : 0
Preventivo             : 1
Correctivo             : 1
Predictivo             : 1
Tiempo total           : 135 minutos
Tiempo promedio        : 45.00 minutos
```

---

### 11. Demostración de algoritmos

Incluye demostraciones sencillas de **Bubble Sort**, **búsqueda binaria** y el **algoritmo voraz**.

Se muestran:

* Lista original y sus versiones ordenadas con Bubble Sort.
* SKU centrales revisados por la búsqueda binaria.
* Orden de atención generado por el algoritmo voraz.
* Explicación numerada de cada algoritmo en lenguaje sencillo.

Ejemplo:

```text
Lista original:
[44, 55, 12, 42, 94, 18, 6, 67]

Ordenamiento ascendente:
[6, 12, 18, 42, 44, 55, 67, 94]

Ordenamiento descendente:
[94, 67, 55, 44, 42, 18, 12, 6]
```

---

## ✅ Validaciones

El sistema incorpora validaciones para evitar el ingreso de datos incorrectos.

### SKU

El SKU del equipo:

* Debe contener letras y números.
* Debe tener entre 1 y 20 caracteres.
* Solo admite letras ASCII (sin tildes) y números.
* No puede repetirse.
* No puede estar vacío.
* No puede contener espacios, guiones ni otros símbolos.

Ejemplo válido:

```text
PC1001
LAP2026
EQABC01
```

Ejemplos inválidos:

```text
PC-01
LAP 2026
PCÁ100
```

---

### Tipo

* De 3 a 50 letras; permite espacios, guion y apóstrofo.
* Ejemplos: `Computadora`, `Todo-en-uno`.

### Marca

* De 1 a 50 letras o números; permite espacios y los signos `&`, `.` y `-`.
* Ejemplos: `HP`, `Lenovo`, `Hewlett-Packard`.

### Usuario

* De 3 a 50 caracteres, sin espacios.
* Permite letras, números y los signos `.`, `_`, `@` y `-`.
* Ejemplos: `CarlosPerez`, `usuario01`, `user@empresa`.

---

### Modelo

De 1 a 50 caracteres. Permite letras, números, espacios y los signos `.`, `_`, `/` y `-`. Debe incluir al menos una letra o número.

Ejemplos:

```text
ThinkCentre
ProBook
OptiPlex 7090
EliteBook 840
```

### Identificación del equipo

De 3 a 50 letras o números; permite espacios y los signos `_`, `.`, `/` y `-`. Debe incluir al menos una letra o número.

---

### Problema

La descripción de una incidencia debe:

* Tener mínimo 10 caracteres.
* Tener máximo 250 caracteres.
* Permitir letras.
* Permitir números.
* Permitir espacios.
* Permitir texto imprimible y puntuación; debe incluir letras o números.

Ejemplo:

```text
El equipo no enciende después de presionar el botón de inicio.
```

---

### Tiempo estimado

El tiempo se registra mediante:

* Horas.
* Minutos.

Los minutos deben estar entre `0` y `59`.

El tiempo total se convierte automáticamente a minutos.

Ejemplo:

```text
Horas: 1
Minutos: 30

Resultado: 90 minutos
```

No se permite registrar un tiempo igual a cero.

---

## 🧠 Algoritmos utilizados

El sistema integra tres tipos de algoritmos: ordenamiento, búsqueda y planificación.

### Bubble Sort

Se utiliza el algoritmo de **ordenamiento burbuja** para ordenar las incidencias.

La lógica compara elementos consecutivos y realiza intercambios cuando se encuentran en un orden incorrecto.

El proyecto utiliza Bubble Sort para:

* Ordenar incidencias por prioridad.
* Ordenar incidencias por tiempo.
* Mantener los equipos ordenados por SKU para la búsqueda binaria.
* Realizar demostraciones de ordenamiento ascendente y descendente.

### Complejidad

El algoritmo Bubble Sort tiene una complejidad temporal aproximada de:

```text
O(n²)
```

donde `n` representa la cantidad de elementos que se deben ordenar.

En cada pasada se revisan elementos vecinos. Si están en el orden equivocado, se cambian de lugar. El proceso termina cuando una pasada completa no necesita intercambios.

### Algoritmo voraz para planificar

El planificador considera solo las incidencias pendientes y elige una por una usando esta regla:

1. Elegir la prioridad más alta.
2. Si hay empate, elegir el menor tiempo estimado.
3. Si todavía hay empate, elegir el ID menor.
4. Repetir con las incidencias restantes.

Este método toma la mejor decisión disponible en cada paso; es una regla práctica, no una garantía de que el plan sea el mejor en todos los escenarios. Como vuelve a revisar las candidatas en cada elección, su tiempo crece aproximadamente como `O(n²)`.

---

## 🔎 Búsqueda

### Búsqueda binaria de equipos

Los equipos se mantienen ordenados por SKU. El algoritmo revisa el elemento central y conserva solo la mitad donde podría estar el SKU buscado. Repite hasta encontrarlo o agotar los candidatos.

1. Revisar el SKU del centro.
2. Descartar la mitad que no puede contener el SKU.
3. Repetir con la mitad restante.

Su tiempo de búsqueda crece aproximadamente como `O(log n)` para una lista ordenada.

### Búsqueda secuencial de incidencias

Las incidencias se localizan por ID recorriendo la lista hasta encontrar una coincidencia. Su tiempo crece aproximadamente como `O(n)`.

---

## 📊 Estructuras de datos

El proyecto utiliza principalmente:

### Listas

Se utilizan para almacenar:

```python
equipos = []
incidencias = []
```

### Diccionarios

Cada equipo e incidencia se representa mediante un diccionario.

Ejemplo:

```python
{
    "id": 1,
    "sku": "PC1001",
    "tipo": "Computadora",
    "marca": "Lenovo",
    "modelo": "ThinkCentre",
    "usuario": "CarlosPerez",
    "equipo": "EquipoAdministrativo01",
    "estado": "Operativo"
}
```

Esto permite organizar la información mediante pares:

```text
clave → valor
```

---

## 🏗️ Estructura del proyecto

```text
proyecto/
├── main.py                  # Menús y comunicación por consola
├── metodos.py               # Datos, validaciones y reglas de negocio
├── algoritmo_voraz.py       # Planificación de incidencias
├── busqueda_binaria.py      # Búsqueda de equipos por SKU
├── ordenamiento_burbuja.py  # Ordenamiento de equipos, incidencias y números
└── README.md
```

---

## 🛠️ Tecnologías utilizadas

* **Python 3**
* Programación estructurada
* Listas
* Diccionarios
* Funciones
* Estructuras condicionales
* Bucles
* Validación de datos
* Algoritmo voraz
* Búsqueda binaria y búsqueda secuencial
* Ordenamiento burbuja
* Medición de tiempo de ejecución

Biblioteca utilizada:

```python
import time
```

El módulo `time` se utiliza principalmente para medir el rendimiento de los algoritmos.

---

## 💻 Requisitos

Para ejecutar el proyecto se necesita:

* Python 3.x
* Terminal, CMD, PowerShell o un IDE compatible con Python.

Puedes comprobar la versión instalada mediante:

```bash
python --version
```

o:

```bash
python3 --version
```

---

## ▶️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/mazag12/proyecto-analisis-algoritmo-aaep-upn-2026.git
```

### 2. Entrar al proyecto

```bash
cd proyecto-analisis-algoritmo-aaep-upn-2026

```

### 3. Ejecutar el sistema

El archivo principal es `main.py`:

```bash
python main.py
```

En algunos sistemas puede ser necesario utilizar:

```bash
python3 main.py
```

---

## 📋 Menú principal

Al iniciar el programa se muestra:

```text
======================================================================
       SISTEMA DE MANTENIMIENTO DE EQUIPOS INFORMÁTICOS
======================================================================

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
H. Ayuda
0. Salir
```

El usuario selecciona una opción mediante el teclado.

---

## 🔄 Flujo general del sistema

El funcionamiento principal puede representarse de la siguiente manera:

```text
                 ┌─────────────────────┐
                 │      INICIO         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    MENÚ PRINCIPAL   │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    Registrar equipo   Registrar        Consultar
                       incidencia       información
          │                 │                 │
          │                 ▼                 │
          │          Seleccionar equipo      │
          │                 │                 │
          │                 ▼                 │
          │          Registrar problema      │
          │                 │                 │
          │                 ▼                 │
          │          Definir prioridad       │
          │                 │                 │
          │                 ▼                 │
          │          Definir tiempo          │
          │                 │                 │
          │                 ▼                 │
          │          Crear incidencia        │
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Gestionar estados   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Planificar atención │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Estadísticas     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │        SALIR        │
                 └─────────────────────┘
```

---

## 🎓 Objetivos académicos

Este proyecto permite poner en práctica los siguientes conceptos:

* Desarrollo de programas en Python.
* Uso de funciones.
* Modularización del código.
* Manejo de listas y diccionarios.
* Validación de entradas.
* Manejo de ciclos y condiciones.
* Búsqueda de información.
* Algoritmos de ordenamiento.
* Análisis básico de complejidad.
* Medición de tiempos de ejecución.
* Diseño de un sistema orientado a resolver un problema real.

---

## 🔐 Validación y consistencia de datos

El sistema busca mantener la consistencia de la información mediante validaciones antes de realizar operaciones.

Por ejemplo:

* No se pueden registrar SKU duplicados ni vacíos.
* Una incidencia debe estar asociada a un equipo existente.
* La prioridad debe estar entre 1 y 5.
* El tiempo estimado debe ser mayor que cero.
* Los estados están limitados a las opciones definidas.
* Los tipos de mantenimiento están limitados a las categorías disponibles.

Esto evita que se almacenen datos que puedan afectar el funcionamiento del sistema.

---

## ⚠️ Limitaciones actuales

Esta versión del proyecto utiliza estructuras de datos en memoria.

Por lo tanto:

* Los datos se pierden al cerrar el programa.
* No utiliza una base de datos.
* No cuenta con autenticación de usuarios.
* No posee una interfaz gráfica.
* No dispone de una API.
* La información se gestiona desde la consola.

Estas características pueden considerarse posibles mejoras para futuras versiones.

---

## 🔮 Mejoras futuras

Entre las posibles mejoras se encuentran:

* 💾 Implementar una base de datos como SQLite, MySQL o PostgreSQL.
* 🖥️ Crear una interfaz gráfica.
* 🌐 Convertir el sistema en una aplicación web.
* 👤 Implementar usuarios y autenticación.
* 📊 Incorporar gráficos y dashboards.
* 📄 Generar reportes de mantenimiento.
* 🔔 Implementar notificaciones.
* 🔎 Agregar filtros avanzados de búsqueda.
* 📅 Incorporar programación de mantenimientos preventivos.
* 📦 Agregar categorías y características adicionales de los equipos.
* 📝 Registrar un historial de cambios de estado.
* 📈 Incorporar más algoritmos y comparar su rendimiento.

---

## 👨‍💻 Autor

Proyecto desarrollado con fines académicos y de aprendizaje en programación y algoritmos.

---

## 📄 Licencia

Este proyecto puede utilizarse con fines educativos y de aprendizaje.

Si se requiere una licencia específica para distribución o uso comercial, se recomienda incorporar una licencia formal como **MIT**, **Apache 2.0** u otra que corresponda al propósito del proyecto.

---

## ⭐ Conclusión

El **Sistema de Mantenimiento de Equipos Informáticos** permite gestionar de manera sencilla equipos e incidencias de mantenimiento, proporcionando funcionalidades de registro, consulta, búsqueda, actualización, planificación y estadísticas.

Además de resolver una necesidad básica de gestión, el proyecto permite demostrar la aplicación práctica de **Bubble Sort**, búsqueda binaria, búsqueda secuencial y un algoritmo voraz, junto con técnicas de validación y organización modular del código.

El proyecto constituye una base que puede evolucionar posteriormente hacia una solución con persistencia de datos, interfaz gráfica o aplicación web.
