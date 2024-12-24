function addToCart(event, id, name, price) {
    event.preventDefault();
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(function(res) {
        console.info(res);
        return res.json();
    }).then(function(data) {
        console.info(data);

        let counter = document.getElementById('cartCounter');
        counter.innerText = data.total_quantity;
    }).catch(function(error) {
        console.error('Error:', error);
    });
}