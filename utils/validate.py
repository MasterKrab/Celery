from starlette.exceptions import HTTPException


def raise_404_error():
    raise HTTPException(status_code=404, detail="Not Found")


def validate_books(result):
    if len(result["books"]) == 0:
        raise_404_error()
