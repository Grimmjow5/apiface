from flask import render_template, request, redirect, Blueprint, flash
import os
from .models import EmpleadoDto, Verificando
from database.repoEmpleado import setEmpleado,getEmpleado
from faces.ControllerImg import ControllerImg
from database.modeld import Empleado
import cv2
from tortoise import Tortoise

#Tal vez un error por el mismo prefix
verificate = Blueprint('verificate', __name__, template_folder='../templates',url_prefix='/reg')


@verificate.route('/registrar', methods=['GET', 'POST'])
async def registrar():
  form = EmpleadoDto(request.form)
  if request.method == 'POST' and form.validate():
    if 'video' not in request.files:
      print("No hay video, en este caso imagen")
      return redirect(request.url)
    file = request.files['video']

    if file.filename == '':
      print("No hay archivo")
      return "No hay archivos",400
    print(form.nickname.data)
    control = ControllerImg(form.nickname.data)
    pathM =control.SaveFile(file)
    control.FormatImg(pathM,"M")
    await setEmpleado(form)
    return render_template('register.html',form=form,success="El empleado ha sido registrado",error="")
  else:
    emplados = await Empleado.all().values()
    await Tortoise.close_connections()
    return render_template('register.html',form=form,success="",error="",empleado=emplados)





@verificate.post("/verifica")
def verificar():
  res = request.form
  if 'foto' not in request.files:
    return "No hay foto", 400

  file = request.files['foto']
  SaveFileTemp(file,res.get('nickname'))
  formatTemp(res.get('nickname'))
  existe = Verificacion(res.get('nickname'))
  if existe != True:
    return "No hay coincidencias", 401
  else:
    return "Coincidencias", 200






@verificate.route("/prueba", methods=['GET'])
async def prueba():
  empleados = await Empleado.all().values()
  return empleados


@verificate.route("/verificarF", methods=['GET','POST'])
def verificarF():
  if request.method == 'GET':
    form = Verificando()
    return render_template('verificando.html',form= form)
  if request.method == 'POST':
    form = Verificando(request.form)
    try:
      if 'foto' not in request.files:
        flash('No file part')
      file = request.files['foto']
      SaveFileTemp(file,form.nickname.data)
      formatTemp(form.nickname.data)

      existe = Verificacion(form.nickname.data)
      if existe:
        form = Verificando()
        return render_template('verificando.html',form=form,error="",success="Foto verificada, Accede!!")
      else:
        form = Verificando(request.form)
        return render_template('verificando.html',form=form,error="Error Usuario no registrado!!",success="")
    except Exception as e:
      print(e)
      return render_template('verificando.html',form=form,error=e,success="")
'''
# Registro de Imagen con nuevo formato
'''

def Verificacion(nickname):
  #Abrir imagen y detectar rostro
  img1 = cv2.imread(f"muestras/{nickname}/{nickname}.jpg",0)
  img2 = cv2.imread(f"C:\\Users\\traba\\AppData\\Local\\Temp\\{nickname}.jpg",0)

  orb = cv2.ORB_create()
  kpa, descr_a = orb.detectAndCompute(img1, None)
  kpb, descr_b = orb.detectAndCompute(img2, None)

  comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = comp.match(descr_a, descr_b)

  similares = [i for i in matches if i.distance < 70]
  rango = 0
  if len(matches) == 0:
    print("No hay similares y da cero")
    rango = 0
  else:
    print("Hay similares y no es cero")
    rr = len(similares)/len(matches)
    rango = rr

  print(rango)
  if rango >= 0.90:
    return True
  else:
    return False

def format(nickname):
  image = cv2.imread(f"muestras/{nickname}/muestra_{nickname}.jpg")
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faceClasifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  faces = faceClasifier.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    cv2.rectangle(image, (x,y), (x+w,+h), (0,255,0), 2)
    rostro = gray[y:y+h, x:x+w]
    face_resize = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(f"muestras/{nickname}/{nickname}.jpg", face_resize)

def formatTemp(nickname):
  image = cv2.imread(f"C:\\Users\\traba\\AppData\\Local\\Temp\\{nickname}.jpg")
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faceClasifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

  faces = faceClasifier.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    cv2.rectangle(image, (x,y), (x+w,+h), (0,255,0), 2)
    rostro = gray[y:y+h, x:x+w]
    face_resize = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(f"C:\\Users\\traba\\AppData\\Local\\Temp\\{nickname}.jpg", face_resize)



'''
  while True:
    ret, frame = cap.read()
    if ret == False: break
    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()

    faces = faceClasifier.detectMultiScale(gray, 1.3, 5)
    #Se dibuja el rectangulo de la cara
    for (x,y,w,h) in faces:
      cv2.rectangle(frame, (x,y), (x+w,+h), (0,255,0), 2)
      rostro = auxFrame[y:y+h, x:x+w]
      rostro = cv2.resize(rostro, dsize=(150,150), interpolation=cv2.INTER_CUBIC)
      grays = cv2.cvtColor(rostro, cv2.COLOR_BGR2GRAY)
      cv2.imwrite(f"muestras/{nickname}/{nickname}.jpg", grays)
      count += 1
    k = cv2.waitKey(1)
    if k == 27 or count >= 800:
      break


'''



'''
#En esta funcion se creara una copia de la imagen guardada, recortara el rostro y con formato en la escala de azuk
def format(nickname):
  #Abrir imagen y detectar rostro
  detector = MTCNN()
  img = pyplot.imread(f"muestras/{nickname}/muestra_{nickname}.jpg")
  rostro = detector.detect_faces(img)

  #Iteración de datos
  for i in range(len(rostro)):
    x1, y1, ancho, alto = rostro[i]['box']
    x2, y2 = x1 + ancho, y1 + alto
    pyplot.subplot(1,len(rostro), i+1)
    pyplot.axis('off')
    reg_rostro = img[y1:y2, x1:x2]
    reg_rostro = cv2.resize(reg_rostro, (150, 200), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(f"muestras/{nickname}/{nickname}.jpg", reg_rostro)
    pyplot.close()
'''
def SaveFileTemp(file, name):
  file.save(os.path.join("C:\\Users\\traba\\AppData\\Local\\Temp\\", f"{name}.jpg"))

'''
def formatTemp(nickname):
  #Abrir imagen y detectar rostro
  detector = MTCNN()
  img = pyplot.imread(f"C:\\Users\\traba\\AppData\\Local\\Temp\\{nickname}.jpg")
  rostro = detector.detect_faces(img)

  #Iteración de datos
  for i in range(len(rostro)):
    x1, y1, ancho, alto = rostro[i]['box']
    x2, y2 = x1 + ancho, y1 + alto
    #pyplot.subplot(1,len(rostro), i+1)
    #pyplot.axis('off')
    reg_rostro = img[y1:y2, x1:x2]
    reg_rostro = cv2.resize(reg_rostro, (150, 200), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(f"C:\\Users\\traba\\AppData\\Local\\Temp\\{nickname}.jpg", reg_rostro)
'''

def SaveFile(file, name):
  if not os.path.exists(f"muestras/{name}"):
    os.makedirs(f"muestras/{name}")
  file.save(os.path.join(f"muestras/{name}", f"muestra_{name}.jpg"))
