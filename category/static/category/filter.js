function filterByCategory() {
    const category = document.getElementById('categoryFilter').value;
    updateFilters('category', category);
}

function filterBySkill() {
    const mode = document.getElementById('skillFilter').value;
    updateFilters('skill', skill);
}

function filterByPersonality() {
    const personality = document.getElementById('personalityFilter').value;
    updateFilters('personality', personality);
}

function filterByMode() {
    const mode = document.getElementById('modeFilter').value;
    updateFilters('mode', mode);
}

function updateFilters(param, value) {
    const currentUrl = new URL(window.location.href);
    const searchParams = currentUrl.searchParams;
    
    if (value) {
        searchParams.set(param, value);
    } else {
        searchParams.delete(param);
    }
    
    window.location.href = currentUrl.toString();
}

function filterMentorCards() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('#mentorCards .col-12');

    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(input) ? 'block' : 'none';
    });
}