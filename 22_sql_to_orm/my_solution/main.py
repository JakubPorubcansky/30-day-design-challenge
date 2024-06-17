import uvicorn
from fastapi import FastAPI

from api.exception_handling import register_exception_handlers
from api import routes

from database.setup import init_db
from database.create_db import create_db

app = FastAPI()

DB_FILE_NAME = "events.db"
# create_db(DB_FILE_NAME, "schema.sql")

register_exception_handlers(app)

app.include_router(routes.router)

@app.on_event("startup")
async def startup_event():
    init_db(DB_FILE_NAME)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
