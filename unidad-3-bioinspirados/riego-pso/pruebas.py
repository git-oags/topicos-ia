import numpy as np
from datos import datos
from aptitud import costo, desglose
from pso import correr_pso, ANCHO, ALTO


def prueba1():
    # 1. cuadricula de 4 columnas por 2 filas, cada sensor en el centro de su celda
    cuadricula = []
    for fila in range(2):
        for col in range(4):
            cuadricula = cuadricula + [(col + 0.5) * ANCHO / 4, (fila + 0.5) * ALTO / 2]

    # 2. 30 acomodos al azar
    np.random.seed(1)
    costos_azar = []
    for r in range(30):
        posicion = []
        for k in range(8):
            posicion = posicion + [np.random.uniform(0, ANCHO), np.random.uniform(0, ALTO)]
        costos_azar.append(costo(posicion))

    # 3. pso
    mejor_pso, costo_pso, historial = correr_pso()

    print("PRUEBA 1: PSO contra cuadricula y azar (8 sensores)")
    print("al azar, promedio de 30:", round(float(np.mean(costos_azar)), 3),
          " mejor:", round(float(min(costos_azar)), 3), " peor:", round(float(max(costos_azar)), 3))
    print("cuadricula 4x2:", round(costo(cuadricula), 3), [round(float(v), 3) for v in desglose(cuadricula)])
    print("pso:", round(costo_pso, 3), [round(float(v), 3) for v in desglose(mejor_pso)])
    print("mejora del pso contra la cuadricula:", round(100 * (1 - costo_pso / costo(cuadricula)), 1), "%")
    print("mejora del pso contra el azar:", round(100 * (1 - costo_pso / np.mean(costos_azar)), 1), "%")


def prueba2():
    print()
    print("PRUEBA 2: 5 semillas con 300 iteraciones")
    finales = []
    for semilla in range(1, 6):
        posicion, mejor, historial = correr_pso(semilla=semilla, iteraciones=300)
        # ultima iteracion en la que bajo el costo
        ultima = 1
        for i in range(1, len(historial)):
            if historial[i] < historial[i - 1]:
                ultima = i + 1
        finales.append(mejor)
        print("semilla", semilla, " it 100:", round(historial[99], 3), " it 200:", round(historial[199], 3),
              " it 300:", round(mejor, 3), " ultima mejora en la iteracion", ultima)
    print("promedio:", round(float(np.mean(finales)), 3), " mejor:", round(min(finales), 3), " peor:", round(max(finales), 3))


def prueba3():
    print()
    print("PRUEBA 3: tamano y topologia del enjambre (100 iteraciones, 5 semillas)")
    for particulas, topologia in [(30, "global"), (60, "global"), (120, "global"), (30, "local")]:
        costos = []
        for semilla in range(1, 6):
            posicion, mejor, historial = correr_pso(semilla=semilla, particulas=particulas, topologia=topologia)
            costos.append(mejor)
        print(particulas, "particulas,", topologia, ":", [round(float(c), 3) for c in costos],
              " promedio:", round(float(np.mean(costos)), 3))


if __name__ == "__main__":
    #prueba1()
    #prueba2()
    prueba3()