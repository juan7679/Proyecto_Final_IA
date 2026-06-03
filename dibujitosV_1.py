import cv2
import numpy as np
import math
import mediapipe as mp
from SelectorColor import dibujar_barra_colores, detectar_seleccion_color, ALTURA_BARRA

# =====================================================================
# 1. CONFIGURACIÓN MODERNA DE MEDIAPIPE (Tasks API)
# =====================================================================
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

opciones = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

def calcular_distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos (x, y)."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# =====================================================================
# 2. MOTOR DE DIBUJO EN TIEMPO REAL
# =====================================================================
def iniciar_backend_dibujo():
    captura = cv2.VideoCapture(0)
    x_anterior, y_anterior = 0, 0
    lienzo = None
    color_dibujo = (255, 0, 255)  # Magenta por defecto

    print("[INFO] Cargando el motor de IA desde hand_landmarker.task...")

    try:
        with HandLandmarker.create_from_options(opciones) as reconocedor:
            print("[INFO] Motor iniciado. Junta índice y pulgar para dibujar.")
            print("[INFO] Sube el dedo índice a la barra superior para cambiar color.")

            while True:
                ret, frame = captura.read()
                if not ret:
                    print("[ERROR] No se pudo acceder a la cámara.")
                    break

                # Efecto espejo
                frame = cv2.flip(frame, 1)
                alto, ancho, _ = frame.shape

                if lienzo is None:
                    lienzo = np.zeros((alto, ancho, 3), dtype=np.uint8)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

                resultados = reconocedor.detect(mp_image)

                # --- Dibujar barra de colores ANTES de procesar la mano ---
                botones = dibujar_barra_colores(frame, color_dibujo)

                if resultados.hand_landmarks:
                    mano = resultados.hand_landmarks[0]

                    x_indice = int(mano[8].x * ancho)
                    y_indice = int(mano[8].y * alto)

                    x_pulgar = int(mano[4].x * ancho)
                    y_pulgar = int(mano[4].y * alto)

                    # --- Detectar si el índice apunta a la barra de colores ---
                    nuevo_color = detectar_seleccion_color(x_indice, y_indice, botones)
                    if nuevo_color:
                        color_dibujo = nuevo_color
                        x_anterior, y_anterior = 0, 0  # Evitar trazo al cambiar color
                    else:
                        # --- Lógica de dibujo: pellizco índice + pulgar ---
                        distancia = calcular_distancia((x_indice, y_indice), (x_pulgar, y_pulgar))

                        # Solo dibujar si el dedo no está en la barra de colores
                        if y_indice > ALTURA_BARRA:
                            if distancia < 40:
                                cv2.circle(frame, (x_indice, y_indice), 10, (0, 255, 0), cv2.FILLED)
                                if x_anterior == 0 and y_anterior == 0:
                                    x_anterior, y_anterior = x_indice, y_indice

                                cv2.line(lienzo, (x_anterior, y_anterior),
                                         (x_indice, y_indice), color_dibujo, 10)
                                x_anterior, y_anterior = x_indice, y_indice
                            else:
                                cv2.circle(frame, (x_indice, y_indice), 10, (0, 0, 255), cv2.FILLED)
                                x_anterior, y_anterior = 0, 0

                # Fusionar lienzo con video
                frame_final = cv2.addWeighted(frame, 1, lienzo, 1, 0)

                cv2.putText(frame_final, "Pellizca para dibujar | Sube el dedo para cambiar color",
                            (10, alto - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
                cv2.putText(frame_final, "Presiona 'c' para limpiar | 'q' para salir",
                            (10, alto - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 2)

                cv2.imshow("Dibujo con Deteccion de Manos", frame_final)

                tecla = cv2.waitKey(1) & 0xFF
                if tecla == ord('q'):
                    break
                elif tecla == ord('c'):
                    lienzo = np.zeros((alto, ancho, 3), dtype=np.uint8)

    except Exception as e:
        print(f"\n[ERROR CRÍTICO] {e}")
        print("Asegúrate de que 'hand_landmarker.task' esté en la misma carpeta.")

    finally:
        captura.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_backend_dibujo()