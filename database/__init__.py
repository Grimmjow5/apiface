



from tortoise import Tortoise, run_async
async def init():
  await Tortoise.init(
    db_url='mysql://root:@127.0.0.1:3306/nuevas',
    modules={'models': ['database.modeld']}
  )
  await Tortoise.generate_schemas()

run_async(init())
