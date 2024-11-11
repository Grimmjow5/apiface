from tortoise.models import Model
from tortoise import fields

class Empleado(Model):
  id = fields.IntField(primary_key=True)
  nickname = fields.CharField(max_length=30,unique=True)
  nombre = fields.CharField(max_length=60)
  nempleado = fields.IntField()
  correo = fields.CharField(max_length=60)
  telefono = fields.IntField()

  class Meta:
    table = "empleados"