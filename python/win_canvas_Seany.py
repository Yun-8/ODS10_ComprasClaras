import tkinter as tk
from tkinter import ttk, messagebox
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_data():
    """
    Conecta con la API de Open-Meteo y obtiene temperaturas horarias
    de Guadalajara, Jal (últimas 24 horas).
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=20.66&longitude=-103.35"
            "&hourly=temperature_2m&past_days=1"
            "&timezone=auto"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Recortamos a las últimas 24 horas y limpiamos la 'T' de la fecha para mayor legibilidad
        horas = [h.replace("T", " ") for h in data["hourly"]["time"][-24:]]
        temperaturas = data["hourly"]["temperature_2m"][-24:]

        return horas, temperaturas
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron obtener los datos:\n{e}")
        return [], []


def configurar_ejes(ax, titulo):
    """Aplica títulos, etiquetas y espaciado limpio al eje X."""
    ax.set_title(titulo, fontsize=10, fontweight="bold")
    ax.set_xlabel("Fecha y Hora", fontsize=8)
    ax.set_ylabel("Temperatura (°C)", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    # Muestra una etiqueta cada 3 horas para que no se encimen
    ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
    ax.tick_params(axis="x", rotation=25, labelsize=7)
    ax.tick_params(axis="y", labelsize=8)


def create_line_chart(horas, temps):
    """Gráfica 1: Línea."""
    fig, ax = plt.subplots(figsize=(8, 2.2))
    ax.plot(horas, temps, color="royalblue", linestyle="-", marker="o", markersize=4, linewidth=1.5)
    configurar_ejes(ax, "Temperatura en Guadalajara — Gráfica de Línea")
    fig.tight_layout()
    return fig


def create_bar_chart(horas, temps):
    """Gráfica 2: Barras."""
    fig, ax = plt.subplots(figsize=(8, 2.2))
    ax.bar(horas, temps, color="coral", alpha=0.85)
    configurar_ejes(ax, "Temperatura en Guadalajara — Gráfica de Barras")
    fig.tight_layout()
    return fig


def create_scatter_chart(horas, temps):
    """Gráfica 3: Dispersión."""
    fig, ax = plt.subplots(figsize=(8, 2.2))
    ax.scatter(horas, temps, color="seagreen", marker="D", s=25)
    configurar_ejes(ax, "Temperatura en Guadalajara — Gráfica de Dispersión")
    fig.tight_layout()
    return fig


def mostrar_graficas(frm, horas, temps):
    """Inserta las tres gráficas en el frame de la ventana tkinter."""
    for fig in [
        create_line_chart(horas, temps),
        create_bar_chart(horas, temps),
        create_scatter_chart(horas, temps),
    ]:
        canvas = FigureCanvasTkAgg(fig, master=frm)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=4, fill="x")


def open_win_canvas(parent: tk.Tk):
    """Crea la ventana secundaria con gráficas de la API."""
    win = tk.Toplevel(parent)
    win.title("Canvas con API (Open-Meteo) y 3 gráficas")
    win.geometry("960x880")

    frm = ttk.Frame(win, padding=10)
    frm.pack(fill="both", expand=True)

    def cargar():
        horas, temps = fetch_data()
        if horas and temps:
            mostrar_graficas(frm, horas, temps)

    ttk.Button(frm, text="Cargar y mostrar gráficas", command=cargar).pack(pady=6)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prueba win_canvas")
    ttk.Button(root, text="Abrir ventana Canvas", command=lambda: open_win_canvas(root)).pack(pady=20)
    root.mainloop()