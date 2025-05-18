function redirectSearch() {
    const input = document.getElementById("materialSearch");
    const keyword = input.value.trim();

    window.location.href = '/category/';

    return false;
}