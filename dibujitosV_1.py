import cv2
import numpy as np
import math
import mediapipe as mp

# =====================================================================
# 1. CONFIGURACIÓN MODERNA DE MEDIAPIPE (Tasks API)
# =====================================================================
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# IMPORTANTE: El archivo descargado debe llamarse exactamente así y estar en esta carpeta
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
    
    print("[INFO] Cargando el motor de IA desde hand_landmarker.task...")
    
    try:
        # Inicializamos el reconocedor
        with HandLandmarker.create_from_options(opciones) as reconocedor:
            print("[INFO] Motor iniciado exitosamente. Haz un 'pellizco' (índice y pulgar) para dibujar.")
            
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
                
                # Procesamos el frame con el nuevo motor
                resultados = reconocedor.detect(mp_image)
                
                if resultados.hand_landmarks:
                    mano = resultados.hand_landmarks[0]
                    
                    x_indice = int(mano[8].x * ancho)
                    y_indice = int(mano[8].y * alto)
                    
                    x_pulgar = int(mano[4].x * ancho)
                    y_pulgar = int(mano[4].y * alto)
                    
                    # LÓGICA DE ESTADO: Calcular distancia
                    distancia = calcular_distancia((x_indice, y_indice), (x_pulgar, y_pulgar))
                    
                    if distancia < 40:
                        cv2.circle(frame, (x_indice, y_indice), 10, (0, 255, 0), cv2.FILLED)
                        if x_anterior == 0 and y_anterior == 0:
                            x_anterior, y_anterior = x_indice, y_indice
                            
                        cv2.line(lienzo, (x_anterior, y_anterior), (x_indice, y_indice), (255, 0, 255), 10)
                        x_anterior, y_anterior = x_indice, y_indice
                    else:
                        cv2.circle(frame, (x_indice, y_indice), 10, (0, 0, 255), cv2.FILLED)
                        x_anterior, y_anterior = 0, 0 
                        
                # Fusionamos el lienzo de dibujo con el video en vivo
                frame_final = cv2.addWeighted(frame, 1, lienzo, 1, 0)
                
                cv2.putText(frame_final, "Junta Indice y Pulgar para dibujar", (10, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame_final, "Presiona 'c' para limpiar | 'q' para salir", (10, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
                
                cv2.imshow("Motor de Dibujo - Nuevo Standard", frame_final)
                
                tecla = cv2.waitKey(1) & 0xFF
                if tecla == ord('q'):
                    break
                elif tecla == ord('c'):
                    lienzo = np.zeros((alto, ancho, 3), dtype=np.uint8)

    except Exception as e:
        print(f"\n[ERROR CRÍTICO] Algo falló al cargar el modelo: {e}")
        print("Asegúrate de que 'hand_landmarker.task' esté en la misma carpeta que este script.")

    finally:
        captura.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_backend_dibujo()