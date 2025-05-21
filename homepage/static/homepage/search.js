function redirectSearch(skill = '') {
    const input = document.getElementById("materialSearch");
    const keyword = input ? input.value.trim() : '';
    
    let url = '/category/';
    const params = new URLSearchParams();
    
    if (skill) {
        params.append('skillFilter', skill);
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