const shopItems = document.getElementById("shopItems");

fetch("/inventory", {
    method: "GET",
})
    .then((response) => response.json())
    .then((response) => (shopItems.innerText = response.items));

const shopForm = document.getElementById("form");
const shopTimeResult = document.getElementById("shopTimeResult");
const confirmationModal = document.getElementById("confirmationModal");
const closeButton = document.getElementById("closeButton");

shopForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const data = new URLSearchParams();
    for (let pair of new FormData(shopForm)) {
        data.append(pair[0], pair[1]);
    }

    fetch("/shop", {
        method: "POST",
        body: data,
    })
        .then((response) => response.json())
        .then((response) => showShoppingTime(response.time));
});

function showShoppingTime(time) {
    confirmationModal.style.display = "block";
    shopTimeResult.innerText = time;
}

closeButton.onclick = function () {
    confirmationModal.style.display = "none";
};

window.onclick = function (e) {
    if (e.target == confirmationModal) {
        confirmationModal.style.display = "none";
    }
};
