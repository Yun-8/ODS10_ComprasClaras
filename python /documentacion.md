Proyecto Integrador - MVP (tkinter)
1. Descripción general

Aplicación de escritorio demostrativa construida con Python y tkinter/ttk. Presenta una ventana principal (menú) desde la cual se abren cinco ventanas secundarias (Toplevel), cada una ilustrando un componente típico de interfaces gráficas: mensajes, formularios con validación, listas con operaciones CRUD básicas, tablas (Treeview) con datos desde CSV y dibujo en Canvas.

Lenguaje: Python 3.8+
Dependencias externas: ninguna (solo biblioteca estándar: tkinter, csv, pathlib)
Tipo de aplicación: GUI de escritorio, orientada a eventos
2. Estructura sugerida del proyecto

El código usa imports del tipo from app.win_home import ... y busca data/sample.csv, por lo que la estructura esperada es:

<repo>/
├── main.py              # Punto de entrada (ventana principal)
├── app/
│   ├── __init__.py      # Recomendado (opcional en Python 3.3+)
│   ├── win_home.py      # Ventana de bienvenida
│   ├── win_form.py      # Formulario con validación y guardado
│   ├── win_list.py      # Lista con agregar / eliminar / limpiar
│   ├── win_table.py     # Tabla Treeview alimentada desde CSV
│   └── win_canvas.py    # Dibujo con Canvas
└── data/
    └── sample.csv       # Datos de ejemplo (columnas: nombre, valor1, valor2)

Ejecución: desde la raíz del repositorio, python main.py.

3. Arquitectura y patrón de diseño

Todas las ventanas siguen el mismo patrón:

Cada módulo expone una función open_win_xxx(parent).
La función crea un tk.Toplevel(parent) (ventana hija de la principal).
Construye los widgets dentro de un ttk.Frame con padding.
Define los callbacks como funciones anidadas (closures) que acceden a los widgets locales.
Incluye un botón Cerrar que llama a win.destroy.

La ventana principal solo conoce las funciones open_win_*, lo que mantiene bajo el acoplamiento: agregar una ventana nueva implica crear un módulo y un botón.

main.py ──► open_win_home(root)
        ├─► open_win_form(root)
        ├─► open_win_list(root)
        ├─► open_win_table(root)
        └─► open_win_canvas(root)
4. Descripción de los módulos
4.1 main.py — Ventana principal

Función: main()

Elemento	Detalle
tk.Tk()	Crea la ventana raíz (título "Proyecto Integrador - MVP", 420x340).
ttk.Frame	Contenedor con padding de 16 px, empaquetado con fill="both", expand=True.
Botones 1–5	Cada uno abre una ventana mediante lambda, pasando root como padre.
ttk.Separator	Separa visualmente el botón "Salir".
Salir	Ejecuta root.destroy y termina la aplicación.
root.mainloop()	Inicia el bucle de eventos.

El bloque if __name__ == "__main__": asegura que main() solo se ejecute al correr el archivo directamente, no al importarlo.

Nota técnica: se usan lambda porque command espera un callable sin argumentos; la lambda difiere la llamada hasta el clic y permite pasar root.

4.2 app/win_home.py — Home / Bienvenida

Función: open_win_home(parent)

Muestra una etiqueta de bienvenida (fuente Segoe UI 11 negrita) y un texto orientativo.
Botón Mostrar mensaje: abre messagebox.showinfo("Info", "¡Equipo listo!").
Botón Cerrar: destruye la ventana.
Tamaño: 360x220.

Demuestra el uso básico de Label, Button y cuadros de diálogo informativos.

4.3 app/win_form.py — Formulario

Función: open_win_form(parent) con callback interno validar_y_guardar().

Campos:

Campo	Widget	Validación
Nombre	ttk.Entry (ancho 28)	Obligatorio (no vacío tras strip()).
Edad	ttk.Entry (ancho 10)	Debe ser entero positivo (str.isdigit()).

Flujo de validar_y_guardar():

Lee y limpia los valores con .get().strip().
Si el nombre está vacío → messagebox.showerror y return.
Si la edad no es dígito → messagebox.showerror y return.
Abre filedialog.asksaveasfilename (extensión .txt por defecto).
Si el usuario elige ruta, escribe un archivo UTF-8 con el formato:
   Nombre: <nombre>
   Edad: <edad>
Muestra messagebox.showinfo("OK", "Datos guardados.").

Layout: usa grid (etiquetas en columna 0, entradas en columna 1, botones en la fila 3).

4.4 app/win_list.py — Lista (CRUD básico)

Función: open_win_list(parent) con callbacks agregar(), eliminar() y limpiar().

Widgets:

tk.Listbox (altura 10) a la izquierda, que se expande gracias a columnconfigure/rowconfigure(weight=1) y sticky="nsew".
ttk.Entry a la derecha para capturar el texto.
Botones: Agregar, Eliminar seleccionado, Limpiar, Cerrar.

Operaciones:

Operación	Implementación
Create	lb.insert("end", valor) y limpia el campo; si está vacío, showwarning.
Delete	lb.curselection() obtiene el índice seleccionado y lb.delete(sel[0]).
Clear	lb.delete(0, "end") borra todo.

Los datos viven solo en memoria: se pierden al cerrar la ventana. No hay Update (edición), por eso se nombra "CRUD básico".

4.5 app/win_table.py — Tabla (Treeview)

Función: open_win_table(parent)

Define columnas ("nombre", "valor1", "valor2").
Crea ttk.Treeview con show="headings" (oculta la columna de árbol); cada encabezado se capitaliza y centra, con ancho de 120 px.
Calcula la ruta del CSV: Path(__file__).resolve().parents[2] / "data" / "sample.csv".
Si el archivo no existe, muestra showwarning y termina la función.
Si existe, lo lee con csv.DictReader (UTF-8) e inserta cada fila con tv.insert("", "end", values=...).
Agrega el botón Cerrar.

Formato esperado de data/sample.csv:

csv
nombre,valor1,valor2
Ana,10,20
Luis,15,30
4.6 app/win_canvas.py — Canvas (Dibujo)

Función: open_win_canvas(parent)

Crea un tk.Canvas de 440x240 con fondo blanco y dibuja cuatro primitivas:

Método	Resultado
create_rectangle(20, 20, 120, 80, ...)	Rectángulo con borde negro de 2 px.
create_oval(150, 20, 220, 90, fill="lightblue")	Óvalo azul claro.
create_line(240, 30, 360, 90, width=3)	Línea diagonal de 3 px.
create_text(220, 140, ...)	Texto "¡Hola Canvas!" en negrita.

Las coordenadas son (x1, y1, x2, y2) con origen en la esquina superior izquierda.

5. Conceptos de tkinter utilizados
Concepto	Dónde
Tk vs Toplevel	Ventana raíz en main.py; secundarias en win_*.py.
Gestores de geometría pack y grid	pack en la mayoría; grid en form y list.
Widgets ttk (temáticos)	Frame, Label, Button, Entry, Treeview, Separator.
Widgets clásicos tk	Listbox, Canvas.
Diálogos	messagebox (info, warning, error) y filedialog.
Closures como callbacks	validar_y_guardar, agregar, eliminar, limpiar.
E/S de archivos	Escritura de .txt (form) y lectura de .csv (table).
6. Observaciones y posibles mejoras

Posibles errores / puntos de atención

Ruta del CSV (win_table.py): parents[2] sube dos niveles desde el archivo. Si el archivo está en <repo>/app/win_table.py, parents[2] apunta fuera del repositorio y el CSV no se encontrará; en ese caso debe usarse parents[1]. parents[2] solo es correcto si el módulo está en <repo>/src/app/.
Botón "Cerrar" en win_table.py: se crea después del return por archivo faltante, por lo que en ese caso la ventana queda vacía y sin botón. Conviene crearlo antes de cargar los datos o cerrar la ventana al fallar.
Validación de edad: isdigit() acepta "0" y algunos caracteres Unicode numéricos; no valida rangos (p. ej. 1–120).
Encabezados CSV: si faltan columnas, row["nombre"] lanza KeyError.
Múltiples instancias: se puede abrir la misma ventana varias veces; se puede evitar con win.transient(parent) / win.grab_set() o controlando instancias abiertas.
win_list.py: eliminar() no avisa si no hay selección.

Mejoras sugeridas

Añadir app/__init__.py y un requirements.txt (vacío) para formalizar el paquete.
Centralizar fuentes y tamaños en un módulo de constantes (config.py).
Agregar scrollbar al Treeview y al Listbox.
Incluir edición (Update) y persistencia (CSV/JSON/SQLite) en la lista.
Manejar excepciones de E/S (try/except OSError) al guardar y leer archivos.
Añadir pruebas para la lógica de validación, separándola de la interfaz.
7. Ejecución
bash
# 1. Ubicarse en la raíz del proyecto
cd <repo>

# 2. Verificar que existe data/sample.csv
# 3. Ejecutar
python main.py
