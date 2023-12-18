const form = document.querySelector("#form");

form.addEventListener("submit", function (e) {
    e.preventDefault();
    const query = form.elements.query.value;
    getColours(query);
});

function getColours(query) {
    fetch("/palette", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            query: query
        })
    })
    .then((response) => response.json())
    .then(data => {
        const colours = data.colours;
        const container = document.querySelector(".container");
        createColourBoxes(colours, container);
    })
}


function createColourBoxes(colours, parent) {
    parent.innerHTML = "";
    for (const colour of colours) {
        const div = document.createElement("div");
        div.classList.add("colourBox");
        div.style.backgroundColor = colour;
        div.style.width = `calc(100%/${colours.length})`;

        div.addEventListener("click", function() {
            navigator.clipboard.writeText(colour);
        });
        const span = document.createElement("span");
        span.innerText = colour;

        div.appendChild(span);
        parent.appendChild(div);
    }

}