import math
from datos import datos

NUM_SENSORES = 8

PESO_CULTIVO = 2
PESO_ELEVACION = 1

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

def desglose(posicion):
    # regresa las tres partes del costo por separado
    sensores = separar_sensores(posicion)
    asignacion, distancias = asignar(sensores)

    # cobertura: distancia al cuadrado pesada por importancia
    suma = 0
    for i in range(len(datos)):
        suma = suma + datos["importancia"][i] * distancias[i] ** 2
    cobertura = suma / datos["importancia"].sum()

    # mezcla de cultivos y desnivel dentro de la zona de cada sensor
    revueltas = 0
    desnivel = 0
    for k in range(len(sensores)):
        zona = datos[[a == k for a in asignacion]]
        if len(zona) == 0:
            continue
        revueltas = revueltas + len(zona) - zona["cultivo"].value_counts().max()
        desnivel = desnivel + len(zona) * zona["elevacion"].std(ddof=0)
    mezcla = revueltas / len(datos)
    desnivel = desnivel / len(datos) / datos["elevacion"].std(ddof=0)

    return cobertura, mezcla, desnivel


def costo(posicion):
    cobertura, mezcla, desnivel = desglose(posicion)
    return cobertura + PESO_CULTIVO * mezcla + PESO_ELEVACION * desnivel

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
    print("costo con 1 sensor:", round(costo([5, 5]), 3), desglose([5, 5]))
    print("costo con 2 sensores:", round(costo([2.5, 5, 7.5, 5]), 3), desglose([2.5, 5, 7.5, 5]))