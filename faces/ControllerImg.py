
import cv2
import os

class ControllerImg:


  def __init__(self, name):
    self.name = name
    self.pathMuestra = f"muestras/{self.name}"
    if os.name == 'nt':
      self.pathTmp = f"C:\\Users\\traba\\AppData\\Local\\Temp\\"
    else:
      self.pathTmp = "/tmp/"

  def Verificacion(self)->bool:
    #Recordemos que esta comparacion solo se hace con uns dos fotos, una de muestra y otra que se ingresa,
    #Entonces el plan es tener mas de 1 foto de muestra pra comparar multiples veces, al mismo tiempo y
    img1 = cv2.imread(f"{self.pathMuestra}/{self.name}.jpg",0)
    img2 = cv2.imread(f"{self.pathTmp}/{self.name}.jpg",0)

    orb = cv2.ORB_create()

    kpa, descriptorA = orb.detectAndCompute(img1, None)
    kpb, descriptorB = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(descriptorA, descriptorB)

    similares = [ i for i in matches if i.distance < 70 ]

    rango = 0

    if len(matches) == 0:
      rango = 0
    else:
      rango = len(similares)/len(matches)

    if rango >= 0.96:
      return True
    else:
      return False


  #Retorna donde se guardo la imagen
  def SaveFile(self,file):
    if not os.path.exists(self.pathMuestra):
      os.makedirs(self.pathMuestra)
    #En esta parte puede ser posible, con un array
    file.save(os.path.join(self.pathMuestra, f"muestra_{self.name}.jpg"))
    return os.path.join(self.pathMuestra, f"muestra_{self.name}.jpg")

  def SaveFileTemp(self,file):
    file.save(os.path.join(self.pathTmp, f"{self.name}.jpg"))
    return os.path.join(self.pathTmp, f"{self.name}.jpg")


  def FormatImg(self,ruta:str, tipo:str):
    image = cv2.imread(ruta)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Carga de modelo
    faceClasifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces = faceClasifier.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
      cv2.rectangle(image, (x,y), (x+w, +h), (0,255,0), 2)
      rostro = gray[y:y+h, x:x+w]
      resizeImg = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
      if tipo == "TMP": #O LA NUEVA MUESTRA
        cv2.imwrite(self.pathTmp + f"{self.name}.jpg", resizeImg)
      else:
        print(self.pathMuestra + f"/{self.name}.jpg", resizeImg)
        cv2.imwrite(self.pathMuestra + f"/{self.name}.jpg", resizeImg)





  #def SaveFileTemp(self,file):
