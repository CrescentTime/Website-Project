const cart_form = document.getElementById('cart_form');
const cart_message = document.getElementById('cart_message');

cart_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(cart_form);
    const response = await fetch(`/cart`, {
        method: 'POST',
        body: form_data
    });

    if (response.redirected) {
        window.location.href = response.url;
        return;
    }

    const result = await response.json();
    cart_message.innerText = result.cart_message;
});

const wishlist_form = document.getElementById('wishlist_form');
const wishlist_message = document.getElementById('wishlist_message');

wishlist_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form_data = new FormData(wishlist_form);
    const response = await fetch(`/wishlist`, {
        method: 'POST',
        body: form_data
    });

    if (response.redirected) {
        window.location.href = response.url;
        return;
    }

    const result = await response.json();
    wishlist_message.innerText = result.wishlist_message;
});