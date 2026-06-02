POR FAVOR, corran esto en un Entorno Virtual (venv).** Si lo instalan en su Python global, las versiones de las librerías van a chocar y va a tronar todo.
Además de tener el archivo hand_landmarker.task igual que el .py
1. Abran la terminal en esta carpeta y creen su burbuja virtual:
   ```bash
   python -m venv venv
2. Activen el entorno:
   Windows: .\venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
3. Instalen las únicas 3 librerías que necesitamos:
    Bash
    pip install mediapipe opencv-python numpy
4. Ejecutar el programa:
   python dibujitosV_1.py