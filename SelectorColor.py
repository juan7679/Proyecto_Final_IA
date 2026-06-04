import cv2
import numpy as np

# =====================================================================
# MÓDULO: SELECTOR DE COLORES POR POSICIÓN DEL DEDO
# Descripción: Dibuja una barra de colores en la parte superior de la
#              pantalla. Cuando el dedo índice apunta a un color,
#              ese color queda seleccionado para dibujar.
# =====================================================================

# Colores disponibles en formato BGR (OpenCV usa BGR, no RGB)
COLORES = {
    "Magenta": (255, 0, 255),
    "Azul":    (255, 100, 0),
    "Verde":   (0, 255, 100),
    "Amarillo":(0, 255, 255),
    "Rojo":    (0, 0, 255),
    "Blanco":  (255, 255, 255),
}

# Altura de la barra de colores en pixeles
ALTURA_BARRA = 60

def dibujar_barra_colores(frame, color_actual):
    
    #Dibuja la barra de selección de colores en la parte superior del frame.
    #Resalta el color actualmente seleccionado.

     # Parámetros:
     # frame: imagen del frame actual (numpy array)
     # color_actual: tupla BGR del color seleccionado actualmente

     #Retorna:
     #  lista de diccionarios con la info de cada botón de color:
     #   [{"nombre": str, "color": tuple, "x_inicio": int, "x_fin": int}]

    alto, ancho, _ = frame.shape
    nombres = list(COLORES.keys())
    ancho_boton = ancho // len(nombres)
    botones = []

    for i, nombre in enumerate(nombres):
        color_bgr = COLORES[nombre]
        x_inicio = i * ancho_boton
        x_fin = x_inicio + ancho_boton

        # Fondo del botón
        cv2.rectangle(frame, (x_inicio, 0), (x_fin, ALTURA_BARRA), color_bgr, cv2.FILLED)

        # Resaltar el color actualmente seleccionado con un borde blanco
        if color_bgr == color_actual:
            cv2.rectangle(frame, (x_inicio + 3, 3), (x_fin - 3, ALTURA_BARRA - 3), (255, 255, 255), 3)
            cv2.putText(frame, nombre, (x_inicio + 8, ALTURA_BARRA - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        else:
            cv2.putText(frame, nombre, (x_inicio + 8, ALTURA_BARRA - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 50, 50), 1)

        botones.append({
            "nombre": nombre,
            "color": color_bgr,
            "x_inicio": x_inicio,
            "x_fin": x_fin
        })

    return botones


def detectar_seleccion_color(x_indice, y_indice, botones):
    #Revisa si el dedo índice está apuntando a la barra de colores.
   # Si está dentro de la altura de la barra, devuelve el color correspondiente.

   # Parámetros:
   #x_indice: posición X del dedo índice en píxeles
   #y_indice: posición Y del dedo índice en píxeles
   #botones : lista de botones devuelta por dibujar_barra_colores()

    #Retorna:
    # tupla BGR del nuevo color si se seleccionó uno, o None si no
    
    if y_indice <= ALTURA_BARRA:
        for boton in botones:
            if boton["x_inicio"] <= x_indice <= boton["x_fin"]:
                return boton["color"]
    return None
