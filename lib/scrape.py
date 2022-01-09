from bs4 import BeautifulSoup
from utils.user_agent import get_random_user_agent
import requests
import random

BASE_URL = "https://books.toscrape.com"

NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def get_soup(path):
    response = requests.get(
        f"{BASE_URL}/{path}",
        headers={"User-Agent": get_random_user_agent()},
    )
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_categories():
    soup = get_soup("/")

    links = soup.select("ul.nav.nav-list li a")

    def get_category(link):
        slug = link["href"].split("/")[-2]
        name = link.text.strip()

        return {"slug": slug, "name": name}

    return [get_category(link) for link in links]


def get_number_pages():
    soup = get_soup("/")

    li = soup.select_one("li.current")

    number_pages = li.text.strip().split(" ")[-1]

    return int(number_pages)


def get_books_page(number=1, category=None):
    category_path = f"books/{category}" if category != "books_1" else category

    path = (
        f"/catalogue/category/{category_path}/{f'/page-{number}.html' if number > 1 else ''}"
        if category
        else f"catalogue/page-{number}.html"
    )

    soup = get_soup(path)

    articles = soup.select("article.product_pod")

    def get_book_info(article):
        link = article.find("a")

        slug = link["href"].split("/")[-2]

        image = link.find("img")

        title = image["alt"]
        thumbnail = f"{BASE_URL}/{image['src'].replace('../', '')}"

        stars_number_text = article.select_one("p.star-rating")["class"][-1].lower()

        stars = NUMBERS.get(stars_number_text) or 0

        price = article.select_one("p.price_color").text

        stock = article.select_one("p.instock.availability")

        in_stock = stock.text.strip() == "In stock"

        return {
            "slug": slug,
            "title": title,
            "thumbnail": thumbnail,
            "stars": stars,
            "price": price,
            "in_stock": in_stock,
        }

    books = [get_book_info(article) for article in articles]

    li = soup.select_one("li.current")

    pages = li.text.strip().split(" ")[-1] if li else 0

    return {"books": books, "pages": int(pages)}


def get_all_books():
    number_pages = get_number_pages()

    all_books = []

    for i in range(1, number_pages + 1):
        all_books += get_books_page(i)

    return all_books


def get_book(slug):
    soup = get_soup(f"catalogue/{slug}")

    title = soup.find("h1").text

    image = soup.select_one("#product_gallery img")

    thumbnail = f"{BASE_URL}/{image['src'].replace('../', '')}"

    price = soup.select_one("p.price_color").text

    stock_text = soup.select_one("p.instock.availability").text.strip()

    in_stock = stock_text.startswith("In stock")

    stock = int(stock_text.split(" ")[-2][1]) if in_stock else 0

    stars_number_text = soup.select_one("p.star-rating")["class"][-1].lower()

    stars = NUMBERS.get(stars_number_text) or 0

    description_tag = soup.select_one("#product_description + p")

    description = description_tag.text if description_tag else None

    category = soup.select_one("ul.breadcrumb li:nth-child(3)").text.strip()

    product_information = {}

    trs = soup.select("table.table tr")

    for tr in trs:
        key = tr.find("th").text
        value = tr.find("td").text

        product_information[key] = value

    return {
        "title": title,
        "thumbnail": thumbnail,
        "price": price,
        "stock": stock,
        "stars": stars,
        "description": description,
        "category": category,
        "product_information": product_information,
    }
