const books = document.getElementById("books")

const handleClick = (e) => {
    const card = e.target.closest(".book")

    if(!card) return

    window.location.href = card.getAttribute("data-url")
}

const handleFocus = (e) => {
    const cardContent = e.target.parentElement.parentElement

    cardContent.classList.toggle("book__content--show")
}

books.addEventListener("click", handleClick)
books.addEventListener("focusin", handleFocus)
books.addEventListener("focusout", handleFocus)
