async function remove_product(product_id) {

    const response = await fetch(`/wishlist`, {
        method: 'DELETE',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({product_id: product_id})
    });
    window.location.reload();
}