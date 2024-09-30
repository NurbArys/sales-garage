document.addEventListener('DOMContentLoaded', function() {
    var products = [
        { name: "Товар 1", description: "Описание товара 1", imageUrl: "https://example.com/path_to_image1.jpg" },
        { name: "Товар 2", description: "Описание товара 2", imageUrl: "https://example.com/path_to_image2.jpg" },
        // Добавьте больше товаров по аналогии
    ];

    var productContainer = document.getElementById('product-container');

    products.forEach(function(product) {
        var productDiv = document.createElement('div');
        productDiv.className = 'product';
        productDiv.innerHTML = `<h2>${product.name}</h2>
                                 <p>${product.description}</p>
                                 <img src="${product.imageUrl}" alt="${product.name}" style="width:100%;">`;
        productContainer.appendChild(productDiv);
    });
});
