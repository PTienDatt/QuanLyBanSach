

//hàm thêm vào giỏ hàng
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



//hàm thanh toán và xóa sản phẩm trong giỏ hàng
function pay() {
    if (confirm('Bạn có chắc chắn muốn thanh toán giỏ hàng?') == true) {
        fetch('/api/pay', {
            method: 'post',
        }).then(res => {
            console.info('Response:', res);
            return res.json();
        }).then(data => {
            console.info('Data:', data);
            if (data.code == 200) {
                window.location.reload();
            } else {
                console.error('Failed to clear cart:', data.message);
            }
        }).catch(err => console.error('Error:', err));
    }
}


// Hàm cuộn chuột






























