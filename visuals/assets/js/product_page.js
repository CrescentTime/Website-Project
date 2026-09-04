const cart_button = document.getElementById('cart_button');
const cart_message = document.getElementById('cart_message');

cart_button.addEventListener('click', async (e) => {
    e.preventDefault();
    const response = await fetch(`/cart`, {
        method: 'POST'
    })

    if (response.redirect) {
        window.location.href = response.redirect;
        return;
    }

    const result = await response.json();
    cart_message.innerText = result.cart_message;
})

const wishlist_button = document.getElementById('wishlist_button');
const wishlist_message = document.getElementById('wishlist_message');

wishlist_button.addEventListener('click', async (e) => {
    e.preventDefault();
    const response = await fetch(`/wishlist`, {
        method: 'POST'
    })

    if (response.redirect) {
        window.location.href = response.redirect;
        return;
    }

    const result = await response.json();
    wishlist_message.innerText = result.wishlist_message;
})