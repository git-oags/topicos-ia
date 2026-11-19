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
# columnas como listas: leer de una lista en un ciclo es mucho mas rapido que de pandas
X = list(datos["x"])
Y = list(datos["y"])
IMPORTANCIA = list(datos["importancia"])
CULTIVO = list(datos["cultivo"])
ELEVACION = list(datos["elevacion"])
SUMA_IMPORTANCIA = sum(IMPORTANCIA)
DESV_ELEVACION = datos["elevacion"].std(ddof=0)

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
    for i in range(len(X)):
        mejor = 0
        menor = math.inf
        for k in range(len(sensores)):
            sx, sy = sensores[k]
            d = math.sqrt((X[i] - sx) ** 2 + (Y[i] - sy) ** 2)
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
    for i in range(len(X)):
        suma = suma + IMPORTANCIA[i] * distancias[i] ** 2
    cobertura = suma / SUMA_IMPORTANCIA

    # mezcla de cultivos y desnivel dentro de la zona de cada sensor
    revueltas = 0
    desnivel = 0
    for k in range(len(sensores)):
        cultivos = []
        alturas = []
        for i in range(len(X)):
            if asignacion[i] == k:
                cultivos.append(CULTIVO[i])
                alturas.append(ELEVACION[i])
        n = len(alturas)
        if n == 0:
            continue
        mayoria = max(cultivos.count(c) for c in set(cultivos))
        revueltas = revueltas + n - mayoria
        media = sum(alturas) / n
        varianza = sum((a - media) ** 2 for a in alturas) / n
        desnivel = desnivel + n * math.sqrt(varianza)
    mezcla = revueltas / len(X)
    desnivel = desnivel / len(X) / DESV_ELEVACION
    return cobertura, mezcla, desnivel

def costo(posicion):
    cobertura, mezcla, desnivel = desglose(posicion)
    return cobertura + PESO_CULTIVO * mezcla + PESO_ELEVACION * desnivel


def preparar(tabla):
    # vuelve a calcular las listas con otra tabla de parcelas (para probar otros terrenos)
    global X, Y, IMPORTANCIA, CULTIVO, ELEVACION, SUMA_IMPORTANCIA, DESV_ELEVACION
    sal = tabla["salinidad"]
    hum = tabla["humedad"]
    importancia = (1
        + (sal - sal.min()) / (sal.max() - sal.min())
        + (hum.max() - hum) / (hum.max() - hum.min()))
    X = list(tabla["x"])
    Y = list(tabla["y"])
    IMPORTANCIA = list(importancia)
    CULTIVO = list(tabla["cultivo"])
    ELEVACION = list(tabla["elevacion"])
    SUMA_IMPORTANCIA = sum(IMPORTANCIA)
    DESV_ELEVACION = tabla["elevacion"].std(ddof=0)


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
