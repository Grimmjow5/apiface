import cv2
import os

class ReconocerFaces:
  def __init__(self,nickname):
    self.nickname = nickname
    self.foto = f"C:\\Users\\traba\\AppData\\Local\\Temp\\{self.nickname}.jpg"

    self.model = cv2.face_LBPHFaceRecognizer.create()
    self.model.read(f"videos/{self.nickname}/modelLBPH{self.nickname}.xml")

  def VerificacionFace(self):
    #Se tranforma la imagen a escala de grices
    image = cv2.imread(self.foto)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Carga de Configuración de CV2
    faceClass = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    #Deteccion de rostros
    faces = faceClass.detectMultiScale(gray, 1.3, 5)
    #*print(len(faces))
    print("Antes del for")
    for (x, y, w, h) in faces:
      rostro = gray[y:y + h, x:x + w]

      rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
      result = self.model.predict(rostro)

      print(f"Valor n {result[1]}")
      if result[1] < 5700:
        print(f"El usuario {self.nickname}")
        return True
        #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
      else:
        print("No encontrado")
        raise Exception("Rostro no registrado")

    print(f"No se encontro rostros, intentelo de nuevo=> {result[1]}")
    raise Exception("Sin coincidencias !!")
        #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
  #else:
    #raise Exception("No se encontro rostros, intentelo de nuevo")
