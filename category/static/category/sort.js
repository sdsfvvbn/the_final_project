function sortRecommendations() {
    const select = document.getElementById("sortSelect").value;
    const list = document.getElementById("recommendationList");
    const cards = Array.from(list.getElementsByClassName("card"));

    cards.sort((a, b) => {
        const lessonsA = parseFloat(a.dataset.lessons);
        const lessonsB = parseFloat(b.dataset.lessons);
        const ratingA = parseFloat(a.dataset.rating);
        const ratingB = parseFloat(b.dataset.rating);
        const nameA = a.dataset.name.toLowerCase();
        const nameB = b.dataset.name.toLowerCase();

        switch (select) {
            case "priceAsc":
                return lessonsA - lessonsB;
            case "priceDesc":
                return lessonsB - lessonsA;
            case "rating":
                return ratingB - ratingA;
            case "name":
                return nameA.localeCompare(nameB);
        }
    });

    cards.forEach(card => list.appendChild(card));
}