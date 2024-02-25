document.addEventListener('DOMContentLoaded', () => {
window.onload = function() {
    var includeFollows = localStorage.getItem('includeFollows');
    if (includeFollows === 'on') {
        document.getElementById('slide-trend').checked = true;
    } else {
        document.getElementById('slide-trend').checked = false;
    }
};

document.getElementById('slide-trend').addEventListener('change', function() {
    if (this.checked) {
        localStorage.setItem('includeFollows', 'on');
    } else {
        localStorage.setItem('includeFollows', 'off');
    }
    document.getElementById('form__trend').submit();

});
});