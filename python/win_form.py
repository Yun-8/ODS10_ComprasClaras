import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def open_win_form(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Escanear")
    win.geometry("420x260")
    frm = ttk.Frame(win, padding=16)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Escanear Producto:").grid(row=0, column=0, sticky="w")
    

    ttk.Label(frm, text="Producto:").grid(row=1, column=0, sticky="w")
 

    def validar_y_guardar():
        nombre = ent_nombre.get().strip()
        edad_txt = ent_edad.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre es requerido.")
            return
        if not edad_txt.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Texto", "*.txt")])
        if ruta:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(f"Nombre: {nombre}\nEdad: {edad_txt}\n")
            messagebox.showinfo("OK", "Datos guardados.")

    ttk.Button(frm, text="Guardar", command=validar_y_guardar)\
        .grid(row=3, column=0, pady=12)
    ttk.Button(frm, text="Cerrar", command=win.destroy)\
        .grid(row=3, column=1, sticky="e", pady=12)