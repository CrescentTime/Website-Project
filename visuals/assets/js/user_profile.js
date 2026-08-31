function go_to_change_password() {
    window.location.href = '/change_password';
}

function open_username_form() {
    document.getElementById("username_div").style.display = "block";
}

const change_username_form = document.getElementById('username_form');
const username_message = document.getElementById('username_message');
change_username_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(change_username_form);

    const response = await fetch('/change_username', {
        method: 'POST',
        body: form_data,
    });

    const result = await response.json();
    username_message.innerText = result.username_message;
});