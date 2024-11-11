
from wtforms import StringField, validators, Form, FileField, PasswordField, BooleanField,IntegerField

class EmpleadoDto(Form):
  nickname = StringField('Username', [validators.Length(min=4, max=25)])
  nombre = StringField('Nombre Completo', [validators.Length(min=4, max=100)])
  correo = StringField('Correo', [validators.Length(min=6, max=35)])
  nEmpleado = IntegerField('Número de Empleado')
  telefono = IntegerField('Número de Telefono')
  video = FileField('Image File')

class Verificando(Form):
  nickname = StringField('Username', [validators.Length(min=4, max=25)])
  foto = FileField('Image File')