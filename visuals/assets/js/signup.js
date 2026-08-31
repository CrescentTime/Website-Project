const signup_form = document.getElementById('signup_form');
const username_error = document.getElementById('username_error');

signup_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(signup_form);
    const response = await fetch('/signup', {
        method: 'POST',
        body: form_data,
    });

    if (response.redirected) {
        window.location.href = response.url;
        return;
    }

    const result = await response.json();
    username_error.innerText = result.username_error;
});