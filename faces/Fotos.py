import cv2
import os
import cv2.data
import imutils

class CapturaFotos:
  def __init__(self,nickname):
      self.nickname = nickname

  def imprimir(self):
    print(f"Los nombres ====>{self.nickname}")

  def createDir(self):
     if not os.path.exists(f"videos/{self.nickname}/fotos"):
        os.mkdir(f"videos/{self.nickname}/fotos")
        print("Creado")



  def capturarFotos(self):
    self.createDir()
    #Carga de video
    video = cv2.VideoCapture(f"videos/{self.nickname}/{self.nickname}.mp4")
    #Carga de modelo cv2
    faceClasification = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    #Captura de fotos por medio de una video
    index = 0
    while True:
      #Toma de frames
      ret, frame = video.read()
      #Cuando se acabe se detiene el video
      if ret == False: break
      #Se redimenciona al video para mejorar el prceso
      frame = imutils.resize(frame, width=640)
      #Ob frame de pasa a escala de frices par que la identifique la misma libreria
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #Se crea una copia para trabjar con esta nueva imagen
      auxFrame = frame.copy()

      #Se detectan rostros del video
      #Falta investigar que sion los argumentos que se dan para el reconocimiento de rostros
      face = faceClasification.detectMultiScale(gray, 1.3, 5)
      #Se obtiene las coordenadas que son de las la matriz de la imagen
      for (x, y, w, h) in face:
        #Creacion del rectangulo que recortara los rostros
        cv2.rectangle(frame,(x,y), (x + w, +h), (0,255,0), 2)
        rostro = auxFrame[y:y+h, x:x+w]
        #Su tamaño se reduces para el espacio y para que trabaje las imagenes compatibles entre ellas
        rostro = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
        #Guardando img del video
        cv2.imwrite(f"videos/{self.nickname}/fotos/rostro{index}.jpg", rostro)
        index += 1
      #Para mostrar frame de como se capturan las fotos
      #cv2.imshow('Captura de Fotos', frame)

      k = cv2.waitKey(1)
      #Se obtenga como minimo 300 ftoos pro usuario
      if k == 27 or index >= 500:
          break

    #video.release()
    #cv2.destroyAllWindows()