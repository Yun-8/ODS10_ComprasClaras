
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_data():
    """
    Conecta con la API de Open-Meteo y obtiene temperaturas horarias
    de Hermosillo, Sonora (últimas 24 horas).
    Devuelve dos listas: horas (formato HH:MM) y temperaturas.
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=29.07&longitude=-110.97"
            "&hourly=temperature_2m&past_days=1"
            "&timezone=auto"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

   
        raw_horas = data["hourly"]["time"][-24:]
        temperaturas = data["hourly"]["temperature_2m"][-24:]
        horas = [h.split("T")[1] for h in raw_horas]

        return horas, temperaturas
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def create_line_chart(horas, temps):
    """Gráfica de línea (Hermosillo)."""
    fig, ax = plt.subplots(figsize=(6, 2.8))
    temp_min, temp_max = min(temps), max(temps)
    
    ax.plot(horas, temps, linestyle="--", marker="d", color="firebrick", linewidth=2, label="Temp °C")
    ax.set_title(f"Hermosillo — Tendencia de Línea (Mín: {temp_min}°C | Máx: {temp_max}°C)")
    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def create_bar_chart(horas, temps):
    """Gráfica de barras (Hermosillo)."""
    fig, ax = plt.subplots(figsize=(6, 2.8))
    
    ax.bar(horas, temps, color="goldenrod", edgecolor="saddlebrown", alpha=0.85)
    ax.set_title("Hermosillo — Distribución en Barras")
    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def create_area_chart(horas, temps):
    """Gráfica de área rellena (Hermosillo)."""
    fig, ax = plt.subplots(figsize=(6, 2.8))
    
    ax.fill_between(horas, temps, color="orange", alpha=0.35)
    ax.plot(horas, temps, color="darkorange", linewidth=1.8)
    ax.set_title("Hermosillo — Gráfica de Área (Volumen de Temp)")
    ax.set_xlabel("Hora del Día")
    ax.set_ylabel("Temperatura (°C)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def mostrar_graficas(frm, horas, temps):
    """Inserta las tres gráficas en el frame de Tkinter."""

    for widget in frm.winfo_children():
        if isinstance(widget, tk.Frame) or not isinstance(widget, ttk.Button):
            widget.destroy()


    fig1 = create_line_chart(horas, temps)
    canvas1 = FigureCanvasTkAgg(fig1, master=frm)
    canvas1.draw()
    canvas1.get_tk_widget().pack(pady=8, fill="x")

   
    fig2 = create_bar_chart(horas, temps)
    canvas2 = FigureCanvasTkAgg(fig2, master=frm)
    canvas2.draw()
    canvas2.get_tk_widget().pack(pady=8, fill="x")


    fig3 = create_area_chart(horas, temps)
    canvas3 = FigureCanvasTkAgg(fig3, master=frm)
    canvas3.draw()
    canvas3.get_tk_widget().pack(pady=8, fill="x")


def open_win_canvas(parent: tk.Tk):
    """Crea la ventana secundaria con scroll para alojar las 3 gráficas."""
    win = tk.Toplevel(parent)
    win.title("Canvas API — Hermosillo, Son.")
    win.geometry("800x700")

  
    canvas_container = tk.Canvas(win)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas_container.yview)
    scrollable_frame = ttk.Frame(canvas_container, padding=12)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
    )

    canvas_container.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_container.configure(yscrollcommand=scrollbar.set)

    canvas_container.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def cargar():
        horas, temps = fetch_data()
        if horas and temps:
            mostrar_graficas(scrollable_frame, horas, temps)

    ttk.Button(scrollable_frame, text="Cargar y mostrar gráficas", command=cargar).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba win_canvas")
    ttk.Button(root, text="Abrir ventana Canvas", command=lambda: open_win_canvas(root)).pack(pady=20)
    root.mainloop()
