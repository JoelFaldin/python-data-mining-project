import os
import pandas as pd
from tkinter import filedialog, messagebox

from modules.generate_stats import generar_estadisticas
from modules.show_graph import mostrar_grafico
from modules.show_monthly_tendency import mostrar_tendencia_mensual

def load_excel(app, filepath=None):
  if not filepath:
    filepath = filedialog.askopenfilename(
      title="Selecciona un archivo Excel o CSV",
      filetypes=[("Archivos Excel y CSV", "*.xlsx *.xls *.csv")]
    )

  if filepath:
    try:
      ext = os.path.splitext(filepath)[1].lower()
      df = pd.read_csv(filepath) if ext == ".csv" else pd.read_excel(filepath)

      if "Especie" not in df.columns or "Fecha" not in df.columns:
          raise ValueError("El archivo debe contener columnas 'Fecha' y 'Especie'.")

      app.df_original = df.copy()

      # Calculate frequency
      frecuencia = df["Especie"].value_counts().reset_index()
      frecuencia.columns = ["Especie", "Frecuencia"]
      app.df_resultado = frecuencia

      # Update UI
      app.species_table.populate(frecuencia)
      generar_estadisticas(app, df)
      mostrar_grafico(app)
      mostrar_tendencia_mensual(app)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")