from .modeld import Empleado
from app.models import EmpleadoDto
from tortoise import Tortoise

class RepoEmpleados:
  async def setEmpleado(empleado:EmpleadoDto ):
    try:
      emplead = Empleado(
        nickname=empleado.nickname.data,
        correo=empleado.correo.data,
        nombre=empleado.nombre.data,
        nempleado=empleado.nEmpleado.data,
        telefono=empleado.telefono.data,
        activo=empleado.activo.data
      )
      await emplead.save()
      await Tortoise.close_connections()
    except Exception as es:
      await Tortoise.close_connections()
      raise Exception(es)

  async def getEmpleado(name):
    print("GteWtf"+name)
    try:
      print("GteWtf"+name)
      emplead = await Empleado.get(nickname=name)
      await Tortoise.close_connections()
      return emplead.nombre
    except Exception as es:
      await Tortoise.close_connections()
      raise Exception(es)

  async def getAll():
    try:
      empleados = await Empleado.all().values()
      await Tortoise.close_connections()
      return empleados
    except Exception as es:
      await Tortoise.close_connections()
      raise Exception(es)

  async def getId(id:int):
    try:
      empleadoDb = await Empleado.get(id=id)
      await Tortoise.close_connections()
      empleado = EmpleadoDto(
        id=empleadoDb.id,
        nickname=empleadoDb.nickname,
        nombre=empleadoDb.nombre,
        correo=empleadoDb.correo,
        nEmpleado=empleadoDb.nempleado,
        telefono=empleadoDb.telefono,
        activo=empleadoDb.activo
      )
      return empleado
    except Exception as es:
      await Tortoise.close_connections()
      raise Exception(es)

  async def updateEmpleado(empleado):
    try:
      await Empleado.filter(id=empleado.id.data).update(
        nickname=empleado.nickname,
        nombre=empleado.nombre,
        correo=empleado.correo,
        nEmpleado=empleado.nEmpleado,
        telefono=empleado.telefono,
        activo=empleado.activo
      )
      await Tortoise.close_connections()
    except Exception as es:
      await Tortoise.close_connections()
      raise Exception(es)