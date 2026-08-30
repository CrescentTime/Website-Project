const form = document.getElementById('change_password_form');
const message = document.getElementById('message');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(form);
    const response = await fetch('/change_password', {
        method: 'POST',
        body: form_data,
    });
    const result = await response.json();
    message.innerText = result.message;
});