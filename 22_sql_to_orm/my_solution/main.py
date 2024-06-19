from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from api.exception_handling import register_exception_handlers
from api import routes
import business.notifications as notifications
from database.setup import init_db
from database.create_db import create_db


DB_FILE_NAME = "events.db"
# create_db(DB_FILE_NAME, "schema.sql")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(DB_FILE_NAME)
    notifications.email.subscribe()
    notifications.sms.subscribe()
    yield


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(routes.router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
