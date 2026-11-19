import math
from datos import datos

NUM_SENSORES = 8

# importancia de cada parcela: las salinas y las secas necesitan mas vigilancia
sal = datos["salinidad"]
hum = datos["humedad"]
datos["importancia"] = (1
    + (sal - sal.min()) / (sal.max() - sal.min())
    + (hum.max() - hum) / (hum.max() - hum.min()))
def separar_sensores(posicion):
    # convierte [x1, y1, x2, y2, ...] en [(x1, y1), (x2, y2), ...]
    sensores = []
    for i in range(0, len(posicion), 2):
        sensores.append((posicion[i], posicion[i + 1]))
    return sensores


def asignar(sensores):
    # para cada parcela regresa el sensor mas cercano y la distancia a el
    asignacion = []
    distancias = []
    for i in range(len(datos)):
        px = datos["x"][i]
        py = datos["y"][i]
        mejor = 0
        menor = math.inf
        for k in range(len(sensores)):
            sx, sy = sensores[k]
            d = math.sqrt((px - sx) ** 2 + (py - sy) ** 2)
            if d < menor:
                menor = d
                mejor = k
        asignacion.append(mejor)
        distancias.append(menor)
    return asignacion, distancias

def costo(posicion):
    # cobertura: promedio de distancia al cuadrado, pesado por la importancia de la parcela
    sensores = separar_sensores(posicion)
    asignacion, distancias = asignar(sensores)
    suma = 0
    for i in range(len(datos)):
        suma = suma + datos["importancia"][i] * distancias[i] ** 2
    cobertura = suma / datos["importancia"].sum()
    return cobertura

if __name__ == "__main__":
    # prueba con 2 sensores puestos a mano
    prueba = [2.5, 5, 7.5, 5]
    sensores = separar_sensores(prueba)
    asignacion, distancias = asignar(sensores)
    print("sensores:", sensores)
    print("primeras 5 asignaciones:", asignacion[:5])
    print("primeras 5 distancias:", [round(d, 3) for d in distancias[:5]])
    print("parcelas por sensor:", [asignacion.count(k) for k in range(len(sensores))])
    print("distancia promedio:", round(sum(distancias) / len(distancias), 3))
    print(datos[["humedad", "salinidad", "importancia"]].head())
    print("costo con 1 sensor en el centro:", round(costo([5, 5]), 3))
    print("costo con 2 sensores:", round(costo([2.5, 5, 7.5, 5]), 3))
    print("costo con 4 sensores:", round(costo([2.5, 2.5, 7.5, 2.5, 2.5, 8, 7.5, 8]), 3))    
