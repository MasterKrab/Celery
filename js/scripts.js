import FloatingFocus from '@q42/floating-focus-a11y';
import focusableElements from './focusable-elements'

new FloatingFocus();


const waitEvent = (element, eventName) => new Promise((resolve) => element.addEventListener(eventName, resolve))

const categoriesItem = document.getElementById("categories-item")
const categoriesDialog = document.getElementById("categories-dialog")

let firstElementFocus
let lastElementFocus

const toggleClasses = () => {
    document.body.classList.toggle("no-scroll")
    categoriesDialog.classList.toggle("dialog--active")
}

const handleKeyDown = (e) => {
    if (e.key === "Tab") {
        const focus = document.activeElement;

        if (focus === firstElementFocus && e.shiftKey) {
            e.preventDefault();
            lastElementFocus.focus();
        } else if (focus === lastElementFocus && !e.shiftKey) {
            e.preventDefault();
            firstElementFocus.focus();
        }
    } else if (e.key === "Escape") {
        toggleClasses()
        categoriesDialog.removeEventListener("keydown", handleKeyDown)
    }
};

const toggleModal = async () => {
    if (categoriesDialog.classList.contains("dialog--active")) {
        toggleClasses()
        categoriesDialog.removeEventListener("keydown", handleKeyDown)
        return
    }

    toggleClasses()

    await waitEvent(categoriesDialog, "transitionend")

    const focusableElementsInNode = categoriesDialog.querySelectorAll(focusableElements)


    firstElementFocus = focusableElementsInNode[0]

    lastElementFocus = focusableElementsInNode[focusableElementsInNode.length - 1]

    firstElementFocus.focus()

    categoriesDialog.addEventListener("keydown", handleKeyDown)
}

categoriesItem.addEventListener("click", (e) => {
    e.target.closest("button") && toggleModal()
})
