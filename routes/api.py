from fastapi import APIRouter
from pydantic import BaseModel
from utils.validate import validate_books, raise_404_error
from lib.scrape import get_categories, get_books_page, get_book

router = APIRouter()


class Category(BaseModel):
    slug: str
    name: str


class Book(BaseModel):
    slug: str
    title: str
    thumbnail: str
    stars: int
    price: str
    in_stock: bool


class Books(BaseModel):
    categories: list[Category]
    books: list[Book]
    number_pages: int
    current_page: int


@router.get(
    "/page/{page}",
    name="Books page",
    description="Get books by page",
    response_model=Books,
)
async def page(page: int):
    result = get_books_page(page)

    validate_books(result)

    return {
        "categories": get_categories(),
        "books": result["books"],
        "number_pages": result["pages"],
        "current_page": page,
    }


class BooksCategory(Books):
    category: str


@router.get(
    "/{category}/page/{page}",
    name="Books page by category",
    description="Get books by page and category",
    response_model=BooksCategory,
)
async def page(category: str, page: int):
    result = get_books_page(page, category)

    validate_books(result)

    return {
        "categories": get_categories(),
        "books": result["books"],
        "number_pages": result["pages"],
        "current_page": page,
        "category": category,
    }


class ProductInformation(BaseModel):
    upc: str
    type: str
    price: str
    price_incl_tax: str
    tax: str
    availability: str
    number_of_reviews: str


class SingleBook(BaseModel):
    title: str
    thumbnail: str
    price: str
    stock: int
    stars: int
    description: str
    category: str
    product_information: ProductInformation


@router.get(
    "/book/{slug}",
    name="Book",
    description="Get book by slug",
    response_model=SingleBook,
)
async def page(slug: str):
    try:
        book = get_book(slug)
    except Exception as error:
        print(error)
        raise_404_error()

    product_information_keys = {
        "UPC": "upc",
        "Product Type": "type",
        "Price (excl. tax)": "price",
        "Price (incl. tax)": "price_incl_tax",
        "Tax": "tax",
        "Availability": "availability",
        "Number of reviews": "number_of_reviews",
    }

    for key, value in product_information_keys.items():
        book["product_information"][value] = book["product_information"][key]
        book["product_information"].pop(key)

    return book
