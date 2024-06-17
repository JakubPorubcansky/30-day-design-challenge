from fastapi import Request
from fastapi.responses import JSONResponse

import business.exceptions as exc

def register_exception_handlers(app):
    @app.exception_handler(exc.ResourceNotFoundException)
    async def http_exception_handler(request: Request, exc: exc.ResourceNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"message": str(exc)},
        )

    @app.exception_handler(exc.OperationRejectedException)
    async def http_exception_handler(request: Request, exc: exc.OperationRejectedException):
        return JSONResponse(
            status_code=400,
            content={"message": str(exc)},
        )

    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": "internal error"},
        )