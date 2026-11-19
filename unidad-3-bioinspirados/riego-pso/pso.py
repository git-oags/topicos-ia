import numpy as np
from pyswarms.single import GlobalBestPSO, LocalBestPSO
from datos import datos
from aptitud import costo, desglose, NUM_SENSORES

ANCHO = datos["x"].max()
ALTO = datos["y"].max()


def costo_enjambre(enjambre):
    # pyswarms manda todas las particulas juntas; se evalua una por una
    costos = []
    for particula in enjambre:
        costos.append(costo(particula))
    return np.array(costos)


def correr_pso(num_sensores=NUM_SENSORES, semilla=1, iteraciones=100, particulas=30, topologia="global"):
    # corre el pso y regresa la mejor posicion, su costo y el historial
    minimos = np.zeros(2 * num_sensores)
    maximos = np.array([ANCHO, ALTO] * num_sensores)
    np.random.seed(semilla)
    opciones = {"c1": 1.49445, "c2": 1.49445, "w": 0.729}
    if topologia == "global":
        optimizador = GlobalBestPSO(n_particles=particulas, dimensions=2 * num_sensores,
                                    options=opciones, bounds=(minimos, maximos))
    else:
        # cada particula solo ve a sus 4 vecinas mas cercanas (distancia euclidiana, p=2)
        opciones["k"] = 4
        opciones["p"] = 2
        optimizador = LocalBestPSO(n_particles=particulas, dimensions=2 * num_sensores,
                                   options=opciones, bounds=(minimos, maximos))
    mejor_costo, mejor_posicion = optimizador.optimize(costo_enjambre, iters=iteraciones, verbose=False)
    return mejor_posicion, mejor_costo, optimizador.cost_history

if __name__ == "__main__":
    import graficas
    # configuracion final: topologia local y la mejor de 3 semillas (ver pruebas 2 y 3)
    posicion, mejor, historial = None, None, None
    for semilla in range(1, 4):
        p, c, h = correr_pso(semilla=semilla, topologia="local")
        if mejor is None or c < mejor:
            posicion, mejor, historial = p, c, h
    cobertura, mezcla, desnivel = desglose(posicion)
    print("costo al inicio:", round(historial[0], 3))
    print("costo al final:", round(mejor, 3))
    print("cobertura:", round(cobertura, 3), " mezcla:", round(mezcla, 3), " desnivel:", round(desnivel, 3))
    for k in range(NUM_SENSORES):
        print("sensor", k + 1, ":", round(float(posicion[2 * k]), 2), "km,", round(float(posicion[2 * k + 1]), 2), "km")
    graficas.mapa(posicion, "fig_mapa_sensores.png")
    graficas.convergencia(historial, "fig_convergencia.png")