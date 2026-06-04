import math

# MÓDULO: DETECCIÓN DE GESTOS MANUALES
# Puño cerrado = borrar el lienzo
# Mano abierta = pausar el dibujo

def detectar_gesto(mano, ancho, alto):
    puntos = [(int(lm.x * ancho), int(lm.y * alto)) for lm in mano]

    puntas   = [8, 12, 16, 20]
    nudillos = [6, 10, 14, 18]

    dedos_doblados = sum(1 for p, n in zip(puntas, nudillos) if puntos[p][1] > puntos[n][1])
    if dedos_doblados == 4:
        return "puno"

    dedos_extendidos = sum(1 for p, n in zip(puntas, nudillos) if puntos[p][1] < puntos[n][1])
    if dedos_extendidos == 4:
        return "mano_abierta"

    return "ninguno"