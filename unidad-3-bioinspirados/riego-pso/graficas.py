import matplotlib.pyplot as plt
from datos import datos
from aptitud import separar_sensores, asignar

MARCAS = {"Maíz": "o", "Chile": "^", "Tomate": "s"}


def mapa(posicion, archivo):
    # parcelas por cultivo, sensores y la linea de cada parcela a su sensor
    sensores = separar_sensores(posicion)
    asignacion, distancias = asignar(sensores)
    plt.figure(figsize=(7, 7))
    for i in range(len(datos)):
        sx, sy = sensores[asignacion[i]]
        plt.plot([datos["x"][i], sx], [datos["y"][i], sy], color="lightgray", linewidth=0.8, zorder=1)
    for cultivo in MARCAS:
        parte = datos[datos["cultivo"] == cultivo]
        plt.scatter(parte["x"], parte["y"], marker=MARCAS[cultivo], label=cultivo, zorder=2)
    for k in range(len(sensores)):
        plt.scatter(sensores[k][0], sensores[k][1], marker="X", s=200, color="black", zorder=3)
        plt.text(sensores[k][0] + 0.15, sensores[k][1] + 0.15, "S" + str(k + 1), fontsize=11)
    plt.xlabel("x (km)")
    plt.ylabel("y (km)")
    plt.title("Ubicacion de los sensores")
    plt.legend()
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()


def convergencia(historial, archivo):
    # mejor costo de cada iteracion
    plt.figure(figsize=(7, 4))
    plt.plot(range(1, len(historial) + 1), historial)
    plt.xlabel("Iteracion")
    plt.ylabel("Mejor costo")
    plt.title("Convergencia del PSO")
    plt.grid(True, alpha=0.3)
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close()