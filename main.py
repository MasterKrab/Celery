from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi
from routes import client, api
from lib.scrape import get_categories


app = FastAPI(
    title="Celery",
    description="Get books info from https://books.toscrape.com/",
    version="0.1.0",
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api.router, prefix="/api")
app.include_router(client.router, include_in_schema=False)


@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exc: StarletteHTTPException):
    code = exc.status_code

    if not request.url.path.startswith("/api") and code in (404, 500):
        return templates.TemplateResponse(
            f"{code}.html",
            {"request": request, "categories": get_categories()},
            status_code=code,
        )

    return JSONResponse(status_code=code, content={"detail": exc.detail})


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Celery API",
        version="0.1.0",
        description="Get books info from https://books.toscrape.com/",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
