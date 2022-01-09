from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from utils.validate import validate_books, raise_404_error
from lib.scrape import get_categories, get_books_page, get_book

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request):
    result = get_books_page()

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "categories": get_categories(),
            "books": result["books"],
            "number_pages": result["pages"],
            "current_page": 1,
        },
    )


@router.get("/page/{page}")
async def page(request: Request, page: int):
    result = get_books_page(page)

    validate_books(result)

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "categories": get_categories(),
            "books": result["books"],
            "number_pages": result["pages"],
            "current_page": page,
        },
    )


@router.get("/{category}/")
async def root(request: Request, category: str):
    result = get_books_page(category=category)

    validate_books(result)

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "categories": get_categories(),
            "books": result["books"],
            "number_pages": result["pages"],
            "current_page": 1,
            "category": category,
        },
    )


@router.get("/{category}/page/{page}")
async def page(request: Request, category: str, page: int):
    result = get_books_page(page, category)

    validate_books(result)

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "categories": get_categories(),
            "books": result["books"],
            "number_pages": result["pages"],
            "current_page": page,
            "category": category,
        },
    )


@router.get("/book/{slug}")
async def page(request: Request, slug: str):
    try:
        book = get_book(slug)
    except Exception as error:
        print(error)
        raise_404_error()

    return templates.TemplateResponse(
        "book.html",
        {"request": request, "categories": get_categories(), "book": book},
    )
