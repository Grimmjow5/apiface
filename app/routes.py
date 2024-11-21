from flask import Blueprint, flash, redirect,request, render_template
import os
from .models import EmpleadoDto, Verificando
from database.repoEmpleado import setEmpleado
from faces.Fotos import CapturaFotos
from faces.Entrenamiento import EntrenamientoModel
from faces.Reconocer import ReconocerFaces

simple_page = Blueprint('simple_page', __name__,template_folder='../templates',url_prefix='/reg')
ALLOWED_EXTENSIONS = {'txt', 'mp4'}

@simple_page.route('/addEmpleado', methods=['GET', 'POST'])
async def register():
  #Creacion de modelo desde la petición
  form : EmpleadoDto = EmpleadoDto(request.form)
  #Catura de fotos desde el video del usuario
  fotoss = CapturaFotos(form.nickname.data)
  entrenamiendo = EntrenamientoModel(form.nickname.data)
  try:
    if request.method == 'POST' and form.validate():
      await setEmpleado(form)
      if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)
      file = request.files['video']

      if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

      if file and allowed_file(file.filename):
        SaveFile(file, form.nickname.data)
        #Captura de fotos del usuario
        fotoss.capturarFotos()
        #Entrenamiento del modelo, por usuario
        entrenamiendo.Entrenar()

        form = EmpleadoDto()
        return render_template('register.html', form=form,error="", success="Empleado registrado!!")
    else:
      return render_template('register.html', form=form,error="", success="Registra nuevo Empleado!!")
      #return render_template('controluser.html')
  except Exception as e:
    print(e)
    return render_template('register.html', form=form, error=e, success="")


@simple_page.route("/verificando", methods=['GET','POST'])
def verficando():
  if request.method == 'GET':
    form = Verificando()
    return render_template('verificando.html',form= form)

  if request.method == 'POST':
    form = Verificando(request.form)

    try:
      if 'foto' not in request.files:
        flash('No file part')
      file = request.files['foto']
      SaveFileTmp(file,form.nickname.data)

      reconociendo = ReconocerFaces(form.nickname.data)
      existe = reconociendo.VerificacionFace()
      if existe:
        print("Existe")
        form = Verificando()
        return render_template('verificando.html',form= form,error="",success="Foto verificada, Accede!!")

    except Exception as e:
      print(e)
      return render_template('verificando.html',form= form,error=e,success="")
    print("Error no hay nada aqui!!")
    return render_template('verificando.html',form= form,error="",success="")


def SaveFile(files, name):
  if not os.path.exists(f"videos/{name}"):
    print("No existe")
    os.mkdir(f"videos/{name}")
    print("Llega aqi")
    files.save(os.path.join( f"videos/{name}", f"{name}.mp4"))


def SaveFileTmp(files,name):
  files.save(os.path.join("C:\\Users\\traba\\AppData\\Local\\Temp\\", f"{name}.jpg"))

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
