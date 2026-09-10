async function remove_product(product_id) {

    const response = await fetch(`/cart`, {
        method: 'DELETE',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({product_id: product_id})
    });
    window.location.reload();
}


async function checkout() {
    const confirmation = confirm(`Are you sure you want to checkout?`);
    const response = await fetch(`/purchase`, {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({confirmation: confirmation})
    });

    if (confirmation) {
        window.location.reload();
    }

    const result = await response.json();
    alert(result.purchase_message);
}