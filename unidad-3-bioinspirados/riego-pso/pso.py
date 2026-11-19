import numpy as np
from pyswarms.single import GlobalBestPSO
from datos import datos
from aptitud import costo, NUM_SENSORES


def costo_enjambre(enjambre):
    # pyswarms manda todas las particulas juntas; se evalua una por una
    costos = []
    for particula in enjambre:
        costos.append(costo(particula))
    return np.array(costos)


# limites del campo: cada x va de 0 al ancho y cada y de 0 al alto
ancho = datos["x"].max()
alto = datos["y"].max()
minimos = np.zeros(2 * NUM_SENSORES)
maximos = np.array([ancho, alto] * NUM_SENSORES)

np.random.seed(1)
opciones = {"c1": 1.49445, "c2": 1.49445, "w": 0.729}
optimizador = GlobalBestPSO(n_particles=30, dimensions=2 * NUM_SENSORES,
                            options=opciones, bounds=(minimos, maximos))
mejor_costo, mejor_posicion = optimizador.optimize(costo_enjambre, iters=100)

print("costo de la mejor particula al inicio:", round(optimizador.cost_history[0], 3))
print("mejor costo al final:", round(mejor_costo, 3))
for k in range(NUM_SENSORES):
    print("sensor", k + 1, ":", round(float(mejor_posicion[2 * k]), 2), "km,", round(float(mejor_posicion[2 * k + 1]), 2), "km")

import graficas
graficas.mapa(mejor_posicion, "fig_mapa_sensores.png")
graficas.convergencia(optimizador.cost_history, "fig_convergencia.png")