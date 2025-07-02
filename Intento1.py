import cv2
import numpy as np
import os
from pyzbar.pyzbar import decode

print(cv2.__version__)
#URL de la camara que estamos viendo 
url='http://10.203.141.130:8080/video'

Camara=cv2.VideoCapture(url)
Camara.set(3,640)
Camara.set(4,480)
Color=(0,0,255)

if not Camara.isOpened():
    print("Me perdi :(")
    exit()

while(True):
    ret, frame = Camara.read()
    if not ret:
        print("Error leyendo el frame")
        break

    barcodes = decode(frame)
    
    for barcode in barcodes:
        
        cuadro= np.array([barcode.polygon],np.int32)
        cuadro= cuadro.reshape((-1,1,2))
        cv2.polylines(frame,[cuadro],True,Color,5)

        Dato= barcode.data.decode("utf-8")
        ato = barcode.data.decode("utf-8").strip()
        cuadro2 = barcode.rect

        ccl="PL"

        if Dato:
            cv2.putText(frame,Dato,(cuadro2[0],cuadro2[1]), 
                        cv2.FONT_HERSHEY_COMPLEX, 1 , Color, 2 )

        ruta = r"C:\Documentos\Mecatronica\8_Octavo_Semestre\AI\Codigos.txt"

        # Crear archivo si no existe
        if not os.path.exists(ruta):
                open(ruta, "w").close()

            # Leer datos existentes
        with open(ruta, "r") as archivo:
                codigos_guardados = set(line.strip() for line in archivo.readlines())


        if Dato.startswith(ccl):
            print("¡Coincidió con PL!")  # Verificación de la coincidencia con "PL"
            Color = (0, 255, 0)  # Cambiar el color a verde si comienza con "PL"
        else:
            Color=(0,0,255)
            print(":(")
            # Si es nuevo, lo añadimos
        if Dato not in codigos_guardados:
            with open(ruta, "a") as archivo:
                    archivo.write(Dato + "\n")
        

    cv2.imshow("Camara!", frame)
    if cv2.waitKey(1) == ord('q'):
        break

Camara.release()
cv2.destroyAllWindows()