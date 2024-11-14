document.addEventListener("DOMContentLoaded", function() {
    const productsContainer = document.getElementById('products');
    const categoryFilter = document.getElementById('categoryFilter');
    const searchByIdInput = document.getElementById('searchById');
    const searchButton = document.getElementById('searchButton');

    // Fetch products data from GitHub
   fetch('https://cdn.jsdelivr.net/gh/NurbArys/sales-Garage/products.json?clear_cache=' + Math.random())
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(products => {
            console.log('Products fetched successfully:', products);
            const categories = new Set();
            products.forEach(product => {
                categories.add(product.category);
            });

            // Populate category filter dropdown
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilter.appendChild(option);
            });

            // Render products initially
            renderProducts(products);

            // Filter products based on selected category
            categoryFilter.addEventListener('change', () => {
                const selectedCategory = categoryFilter.value;
                const filteredProducts = selectedCategory === 'all' ? products : products.filter(product => product.category === selectedCategory);
                renderProducts(filteredProducts);
            });

            // Search product by ID
            searchButton.addEventListener('click', () => {
                const searchId = searchByIdInput.value.trim();
                if (searchId) {
                    const filteredProducts = products.filter(product => product.id == searchId);
                    renderProducts(filteredProducts);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            productsContainer.innerHTML = '<p class="text-danger">Failed to load products. Please try again later.</p>';
        });

    // Function to render products
    function renderProducts(products) {
        productsContainer.innerHTML = '';
        if (products.length === 0) {
            productsContainer.innerHTML = '<p class="text-warning">No products available for the selected criteria.</p>';
            return;
        }
        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'col-md-4 product-card';
            const images = Array.isArray(product.image_urls) ? product.image_urls : [];
            productCard.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text"><strong>Product ID:</strong> ${product.id}</p>
                        <p class="card-text">${product.description}</p>
                        <p class="card-text"><strong>Category:</strong> ${product.category}</p>
                        <p class="card-text"><strong>Price:</strong> ${product.price}</p>
                        <div class="image-carousel">
                            ${images.length > 0 ? images.map(url => `<img src="${url}" alt="Product Image">`).join('') : '<p>No images available</p>'}
                        </div>
                    </div>
                </div>
            `;
            productsContainer.appendChild(productCard);
        });
    }
});
