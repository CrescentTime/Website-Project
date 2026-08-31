function open_reset_password() {
    document.getElementById("reset_password_div").style.display = "block";
}

const login_form = document.getElementById('login_form');
const login_error = document.getElementById('login_error');
login_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(login_form);
    const response = await fetch('/login', {
        method: 'POST',
        body: form_data,
    });

    if (response.redirected) {
        window.location.href = response.url;
        return;
    }

    const result = await response.json();
    login_error.innerText = result.login_error;
});

const reset_password_form = document.getElementById('reset_password_form');
const reset_message = document.getElementById('reset_message');
reset_password_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(reset_password_form);
    const parameters = new URLSearchParams(form_data);
    const response = await fetch(
        `/reset_password?${parameters.toString()}`
    );
    const result = await response.json();
    reset_message.innerText = result.reset_message;
});