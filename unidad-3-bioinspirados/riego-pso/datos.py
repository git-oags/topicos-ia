import pandas as pd
import numpy as np

datos = pd.read_csv("parcelas_guasave.csv")
datos.columns = ["humedad", "cultivo", "elevacion", "salinidad", "temperatura", "lat", "lon"]

# pasa de latitud y longitud a kilometros, origen en la esquina inferior izquierda
lat0 = datos["lat"].min()
lon0 = datos["lon"].min()
datos["x"] = (datos["lon"] - lon0) * 111.32 * np.cos(np.radians(lat0))
datos["y"] = (datos["lat"] - lat0) * 110.57

if __name__ == "__main__":
    print(datos.head())
    print(datos["cultivo"].value_counts())
    print(datos[["x", "y"]].head())
    print("ancho del campo (km):", datos["x"].max())
    print("alto del campo (km):", datos["y"].max())
    print(datos[["humedad", "elevacion", "salinidad"]].describe())