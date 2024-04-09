from threading import Thread

from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers.sales import router as sales
from bot import bot

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sales, prefix="/sales", tags=["sales"])


if __name__ == "__main__":
    t1 = Thread(target=uvicorn.run, args=(app,))
    t2 = Thread(target=bot.polling)
    t1.start()
    t2.start()
