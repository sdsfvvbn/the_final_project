function redirectSearch(category = '') {
    const input = document.getElementById("materialSearch");
    const keyword = input ? input.value.trim() : '';
    
    let url = '/category/';
    const params = new URLSearchParams();
    
    if (category) {
        params.append('category', category);
    }
    if (keyword) {
        params.append('search', keyword);
    }
    
    const queryString = params.toString();
    if (queryString) {
        url += '?' + queryString;
    }
    
    window.location.href = url;
    return false;
}