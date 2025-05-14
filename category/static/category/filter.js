function filterBy(type) {
    const list = document.getElementById("tutor-list");
    const items = Array.from(list.children);
    let sorted = items;

    if (type === 'rating') {
        sorted = items.sort((a, b) => b.dataset.rating - a.dataset.rating);
    } else if (type === 'class') {
        sorted = items.sort((a, b) => b.dataset.lessons - a.dataset.lessons);
    } else if (type === 'willingness') {
        sorted = items.sort((a, b) => b.dataset.lessons - a.dataset.lessons);
    } else if (type === 'personality') {
        sorted = items.sort((a, b) => a.textContent.localeCompare(b.textContent));
    } else if (type === 'category') {
        sorted = items.sort((a, b) => a.textContent.localeCompare(b.textContent));
    }

    list.innerHTML = '';
    sorted.forEach(item => list.appendChild(item));
}

document.addEventListener('DOMContentLoaded', function () {
    const element = document.getElementById('personalityFilter');
    if (element) {
        new Choices('#personalityFilter', {
            removeItemButton: true,
            placeholder: true,
            placeholderValue: 'Personality',
            searchEnabled: false,
            itemSelectText: '',
            shouldSort: false
        });
    }
});