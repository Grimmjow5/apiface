

import asyncio

from tortoise import Tortoise
async def init():
  await Tortoise.init(
    db_url='mysql://root:@localhost:3306/nuevas',
    modules={'models': ['database.modeld']}
  )

  await Tortoise.generate_schemas()
  Tortoise.init_models(["database.modeld"],"models")
  await Tortoise.close_connections()


asyncio.run(init())
#run_async(init())
