// Clear prediction and error when form changes
window.onload = function() {
    var form = document.querySelector('form');
    var result = document.querySelector('.prediction');
    var error = document.querySelector('.flash-messages');
    if (form) {
        form.addEventListener('input', function() {
            if (result) result.innerHTML = '';
            if (error) error.innerHTML = '';
        });
    }
}