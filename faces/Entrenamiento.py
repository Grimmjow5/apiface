import os
import cv2
import numpy as np

class EntrenamientoModel:
  def __init__(self,nickname):
    self.nickname = nickname
    self.label = []
    self.faces = []

  def verificacionDir(self):
    if not os.path.exists(f"videos/{self.nickname}/fotos"):
      raise Exception("No existe el directorio")
    else:
      print("El directorio existe")

  def Entrenar(self):
    self.verificacionDir()
    listFotos = os.listdir(f"videos/{self.nickname}/fotos")
    index = 0
    for foto in listFotos:
      self.label.append(index)
      self.faces.append(cv2.imread(f"videos/{self.nickname}/fotos/{foto}",0))
      image = cv2.imread(f"videos/{self.nickname}/fotos/{foto}",0)
      #cv2.imshow("Imagen",image)
      #cv2.waitKey(10)
    index+=1

    face_recofnizer = cv2.face_LBPHFaceRecognizer.create()
    face_recofnizer.train(self.faces, np.array(self.label))
    face_recofnizer.write(f"videos/{self.nickname}/modelLBPH{self.nickname}.xml")
    print("Entrenamiento terminado")
