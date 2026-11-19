import os
import matplotlib.pyplot as plt
from datos import datos
from aptitud import separar_sensores, asignar

CARPETA = "figuras"
os.makedirs(CARPETA, exist_ok=True)

MARCAS = {"Maíz": "o", "Chile": "^", "Tomate": "s"}

def mapa(posicion, archivo, tabla=datos, titulo="Ubicacion de los sensores", color=None):
    # parcelas, sensores y la linea de cada parcela a su sensor
    # si color es el nombre de una columna, los puntos se pintan segun esa columna
    sensores = separar_sensores(posicion)
    asignacion, distancias = asignar(sensores)
    plt.figure(figsize=(7, 7))
    for i in range(len(tabla)):
        sx, sy = sensores[asignacion[i]]
        plt.plot([tabla["x"][i], sx], [tabla["y"][i], sy], color="lightgray", linewidth=0.8, zorder=1)
    if color is None:
        for cultivo in MARCAS:
            parte = tabla[tabla["cultivo"] == cultivo]
            plt.scatter(parte["x"], parte["y"], marker=MARCAS[cultivo], label=cultivo, zorder=2)
        plt.legend()
    else:
        puntos = plt.scatter(tabla["x"], tabla["y"], c=tabla[color], cmap="viridis", zorder=2)
        plt.colorbar(puntos, label=color, shrink=0.8)
    for k in range(len(sensores)):
        plt.scatter(sensores[k][0], sensores[k][1], marker="X", s=200, color="black", zorder=3)
        plt.text(sensores[k][0] + 0.15, sensores[k][1] + 0.15, "S" + str(k + 1), fontsize=11)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title(titulo)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(CARPETA, archivo), dpi=150, bbox_inches="tight")
    plt.close()

def convergencia(historial, archivo):
    # mejor costo de cada iteracion
    plt.figure(figsize=(7, 4))
    plt.plot(range(1, len(historial) + 1), historial)
    plt.xlabel("Iteracion")
    plt.ylabel("Mejor costo")
    plt.title("Convergencia del PSO")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(CARPETA, archivo), dpi=150, bbox_inches="tight")
    plt.close()

def costo_por_sensores(numeros, costos, archivo):
    # grafica del codo: costo segun cuantos sensores se ponen
    plt.figure(figsize=(7, 4))
    plt.plot(numeros, costos, marker="o")
    plt.xlabel("Numero de sensores")
    plt.ylabel("Mejor costo")
    plt.title("Costo segun el numero de sensores")
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(CARPETA, archivo), dpi=150, bbox_inches="tight")
    plt.close()