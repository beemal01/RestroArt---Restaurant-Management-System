

function extractError(error) {
    if (error.detail) return error.detail;
    if (error.message) return error.message;
    // Handle field-level errors like {"username": ["This field is required."]}
    for (const key in error) {
        if (Array.isArray(error[key])) {
            return error[key][0];
        }
        return String(error[key]);
    }
    return 'An error occurred. Please try again.';
}

function showError(message) {
    // Remove any existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Create error element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #ff4444;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);

    // Auto remove after 5 seconds
    setTimeout(() => {
        errorDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => errorDiv.remove(), 300);
    }, 5000);

    // Add CSS animation
    if (!document.getElementById('error-animation')) {
        const style = document.createElement('style');
        style.id = 'error-animation';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

function showSuccess(message) {
    // Remove any existing success messages
    const existingSuccess = document.querySelector('.success-message');
    if (existingSuccess) {
        existingSuccess.remove();
    }

    // Create success element
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        font-family: 'Poppins', sans-serif;
        font-size: 0.9rem;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);

    // Auto remove after 5 seconds
    setTimeout(() => {
        successDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => successDiv.remove(), 300);
    }, 5000);
}

function getAccessToken() {
    const raw = localStorage.getItem('access');
    if (!raw) return null;

    const cleaned = raw.replace(/^\uFEFF/, '').replace(/[\x00-\x1F\x7F]/g, '').trim();
    if (!cleaned || cleaned.split('.').length !== 3) {
        localStorage.removeItem('access');
        return null;
    }
    return cleaned;
}


async function signupBtn() {
    const name = document.getElementById('name').value;
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone_number = document.getElementById('phone_number').value;
    const password = document.getElementById('password').value;

    const payload = {
        name: name,
        username: username,
        email: email,
        phone_number: phone_number,
        password: password,
    }

    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = 'Signing...';

    const response = await fetch('/api/signupview/', {
        method: "POST",
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify(payload),
    })

    try {
        if (response.ok) {
            window.location.href = '/signin/';
        }
        else {
            const error = await response.json();
            showError(extractError(error));
        }
    }
    catch {
        showError("Network Error! Please Try-again Latter!!!");
    }

    button.disabled = false;
    button.textContent = 'Sign Up';
}


async function signinBtn() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const payload = {
        username: username,
        email: email,
        password: password,
    }

    const button = document.getElementById('btn');
    button.disabled = true;
    button.textContent = 'Signing...';

    const response = await fetch('/api/signinview/', {
        method: "POST",
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify(payload),
    })

    try {
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access', data.access);
            localStorage.setItem('refresh', data.refresh);
            localStorage.setItem('username', data.User.username);
            window.location.href = '/';
        }
        else {
            const error = await response.json();
            showError(extractError(error));
        }
    }
    catch {
        showError("Network Error! Please Try-again Latter!!!");
    }

    button.disabled = false;
    button.textContent = 'Sign In';
}

document.addEventListener('DOMContentLoaded', () => {
    const access = localStorage.getItem('access');
    const u_name = localStorage.getItem('username')
    if (access) {
        const signin = document.getElementById('signin');
        const signup = document.getElementById('signup');
        const displayName = document.getElementById('display_name');
        const logout = document.getElementById('logout');

        if (signin) signin.style.display = 'none';
        if (signup) signup.style.display = 'none';

        if (displayName) {
            displayName.style.display = 'inline-flex';
            displayName.className = 'tsign tsign-u';
            displayName.innerHTML = '<i class="fas fa-user-check"></i>  ' + u_name;
        }

        if (logout) logout.style.display = 'inline-flex';
    }

    // Load cart items if on the cart page
    if (document.getElementById('cartadd')) {
        loadCart();
    }
});


async function logoutUser() {
    const access = getAccessToken();
    const refresh = localStorage.getItem('refresh');

    if (!access || !refresh) {
        console.error("No tokens found in localStorage");
        return;
    }

    try {
        const response = await fetch('/api/logoutview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + access,
            },
            body: JSON.stringify({ refresh })
        });

        if (response.ok) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            localStorage.removeItem("username");
            window.location.href = '/';
        } else {
            const error = await response.json();
            const alertBox = document.getElementById('alert');
            if (alertBox) {
                alertBox.style.display = 'block';
                alertBox.textContent = extractError(error);
            }
            console.error("Logout failed:", error);
        }
    } catch (err) {
        console.error("Network error:", err);
    }
}


async function loadFoods(limit = null, searchQuery = '', page = 1) {
    let url = "/api/foodlist/?";

    const params = new URLSearchParams();

    if (searchQuery) params.append("search", searchQuery);
    if (limit) params.append("limit", limit);
    if (page) params.append("page", page);

    url += params.toString();

    const response = await fetch(url);

    if (response.status === 429) {
        const msg = await response.json();   
        showError(msg.detail || msg.message || "Too many requests. Please try again later.");                  
        return;                              
    }

    const data = await response.json();

    const container = document.getElementById("food-container");
    container.innerHTML = "";

    const foods = data.results || data;
    if (!foods || foods.length === 0) {
        container.innerHTML = `<div><h2>No items found</h2></div>`;
        return;
    }

    foods.forEach(food => {
        const card = `
        <div class="col-sm-6 col-lg-4 mwrap" data-c="${food.food_category}" data-aos="fade-up">
            <div class="mcard"
                data-id="${food.id}"
                data-img="${food.image}"
                data-title="${food.title}"
                data-cat="${food.show_title}"
                data-price="Rs.${food.price}"
                ${food.old_price ? `data-old="Rs.${food.old_price}"` : ""}
                data-rating="${food.rating}"
                data-cal="${food.calory}"
                data-time="${food.cook_time}"
                data-desc="${food.description}"
                data-tags="${food.tags}">
                <div class="mimg">
                    <img src="${food.image}" alt="${food.title}"/>
                    ${food.chef_tags ? `<div class="mbdg"><i class="fas fa-star"></i> ${food.chef_tags}</div>` : ""}
                    <div class="mhrt"><i class="far fa-heart"></i></div>
                </div>
                <div class="mbody">
                    <div class="mcat">${food.show_title}</div>
                    <div class="mtit">${food.title}</div>
                    <div class="mdesc">${food.description.substring(0, 80)}...</div>
                    <div class="mfoot">
                        <div>
                            <div class="mprice">Rs.${food.price}${food.old_price ? `<small>Rs.${food.old_price}</small>` : ""}</div>
                            <div class="mstars"><i class="fas fa-star"></i> ${food.rating}</div>
                        </div>
                        <button class="madd" title="View Details"><i class="fas fa-plus"></i></button>
                    </div>
                </div>
            </div>
        </div>`;
        container.innerHTML += card;
    });

    // Update pagination display
    const currentPageEl = document.getElementById('currentPage');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (currentPageEl) {
        currentPageEl.textContent = page;
    }
    
    if (prevBtn) {
        prevBtn.disabled = !data.previous;
        prevBtn.onclick = () => {
            if (data.previous) {
                loadFoods(limit, searchQuery, page - 1);
                window.scrollTo({ top: document.getElementById('menu').offsetTop - 100, behavior: 'smooth' });
            }
        };
    }
    
    if (nextBtn) {
        nextBtn.disabled = !data.next;
        nextBtn.onclick = () => {
            if (data.next) {
                loadFoods(limit, searchQuery, page + 1);
                window.scrollTo({ top: document.getElementById('menu').offsetTop - 100, behavior: 'smooth' });
            }
        };
    }

    AOS.refresh();
}



async function addCart(foodId, qty = 1) {
    const access = await getAccessToken();
    const refresh = localStorage.getItem("refresh");

    if (!access || !refresh) {
        window.location.href = "/signin/";
        return;
    }

    const response = await fetch("/api/cartview/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access
        },
        body: JSON.stringify({ food_id: foodId, quantity: qty })
    });

    if (!response.ok) {
        console.error("Failed to add to cart:", response.status, await response.text());
        return;
    }

    loadCart();
}

async function loadCart() {
    const access = getAccessToken();
    if (!access) {
        window.location.href = "/signin/";
        return;
    }

    const response = await fetch("/api/cartview/", {
        headers: { "Authorization": "Bearer " + access }
    });

    if (!response.ok) return;

    const items = await response.json();
    const container = document.getElementById("cartadd");
    const cart_summary = document.getElementById('cartsummary');


    if (!container) return;

    container.innerHTML = "";



    if (!items || items.length === 0) {
        container.innerHTML = `
            <div class="empty-cart">
                <h2>Your cart is empty</h2>
                <p>Please select an item first.</p>
            </div>
        `;
        if (cart_summary) {
            cart_summary.innerHTML = '';
        }
        return;
    }


    items.forEach(item => {
        const totalPrice = (item.food.price || 0) * (item.quantity || 1);
        const card = `
            <div class="cart-row">
                <div class="ci-product">
                    <button class="ci-remove" onclick="removeFromCart(${item.id})"><i class="fas fa-times"></i></button>
                    <img src="${item.food.image || ''}" alt=""/>
                    <div>
                        <div class="ci-name">${item.food.title || ''}</div>
                    </div>
                </div>
                <div class="ci-price">Rs.${item.food.price || ''}</div>
                <div class="ci-qty">
                    <button class="ci-qty-btn ci-qty-minus" data-cart-id="${item.id}">-</button>
                    <span class="ci-qty-num">${item.quantity || 1}</span>
                    <button class="ci-qty-btn ci-qty-plus" data-cart-id="${item.id}">+</button>
                </div>
                <div class="ci-total">Rs.${totalPrice.toFixed(2)}</div>
                <div class="ci-actions">
                    <button class="ci-like"><i class="far fa-heart"></i></button>
                </div>
            </div>
        `;
        container.innerHTML += card;

    });

    if (!cart_summary) return;

    let subtotal = 0;
    items.forEach(item => {
        subtotal += (item.food.price || 0) * (item.quantity || 1);
    });
    let tax = subtotal * 0.13;
    let total = subtotal + tax;

    cart_summary.innerHTML = `
            <h4>Order Summary</h4>
            <div class="cs-row">
                <span>Subtotal</span>
                <span class="cs-val" id="cs-subtotal">Rs.${subtotal.toFixed(2)}</span>
            </div>
            <div class="cs-row">
                <span>Delivery Fee</span>
                <span class="cs-val cs-green">Free</span>
            </div>
            <div class="cs-row">
                <span>Vat (13%)</span>
                <span class="cs-val" id="cs-tax">Rs.${tax.toFixed(2)}</span>
            </div>
            <div class="cs-row cs-total">
                <span>Total</span>
                <span class="cs-val" id="cs-total">Rs.${total.toFixed(2)}</span>
            </div>
            <div class="cs-divider"></div>
            <div class="cs-promo">
                <input type="text" class="cs-promo-input" placeholder="Promo code"/>
                <button class="cs-promo-btn">Apply</button>
            </div>
            <div class="cs-divider"></div>
            <button class="btn-red w-100 justify-content-center" id="checkoutBtn"><i class="fas fa-lock"></i> Proceed to Checkout</button>
    `;

    AOS.refresh();
}

// Checkout button
document.addEventListener('click', async function (e) {
    const checkoutBtn = e.target.closest('#checkoutBtn');
    if (checkoutBtn) {
        e.preventDefault();
        const access = getAccessToken();
        if (!access) {
            window.location.href = '/signin/';
            return;
        }

        checkoutBtn.disabled = true;
        checkoutBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

        try {
            const response = await fetch('/api/checkout/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + access
                }
            });

            if (response.status === 429) {
                const msg = await response.json();
                showError(msg.detail || msg.message || "Too many requests. Please try again later.");
                checkoutBtn.disabled = false;
                checkoutBtn.innerHTML = '<i class="fas fa-lock"></i> Proceed to Checkout';
                return;
            }

            const data = await response.json();

            if (response.ok) {
                showSuccess('Order placed successfully! Check your email for confirmation.');
                loadCart(); // Reload cart (will be empty)
            } else {
                showError(data.error || 'Checkout failed. Please try again.');
            }
        } catch (err) {
            showError('Network error. Please try again.');
            console.error('Checkout error:', err);
        }

        checkoutBtn.disabled = false;
        checkoutBtn.innerHTML = '<i class="fas fa-lock"></i> Proceed to Checkout';
        return;
    }

    const minusBtn = e.target.closest('.ci-qty-minus');
    if (minusBtn) {
        const cartId = minusBtn.getAttribute('data-cart-id');
        const qtyEl = minusBtn.parentElement.querySelector('.ci-qty-num');
        let qty = parseInt(qtyEl.textContent);
        if (qty > 1) {
            updateCartQty(cartId, qty - 1);
        }
        return;
    }

    const plusBtn = e.target.closest('.ci-qty-plus');
    if (plusBtn) {
        const cartId = plusBtn.getAttribute('data-cart-id');
        const qtyEl = plusBtn.parentElement.querySelector('.ci-qty-num');
        let qty = parseInt(qtyEl.textContent);
        updateCartQty(cartId, qty + 1);
    }
});

async function updateCartQty(cartId, qty) {
    const access = getAccessToken();
    if (!access) return;

    const response = await fetch(`/api/cartview/${cartId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access
        },
        body: JSON.stringify({ quantity: qty })
    });

    if (response.ok) {
        loadCart();
    }
}

async function removeFromCart(cartId) {
    const access = await getAccessToken();
    if (!access) return;

    const response = await fetch(`/api/deleteview/${cartId}/`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + access }
    });

    if (response.ok) {
        loadCart();
    }
}

async function resBtn() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const number = document.getElementById('number').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const guest = document.getElementById('guest').value;
    const special_request = document.getElementById('special_request').value;
    const access = localStorage.getItem('access')

    if (!access) {
        document.getElementById('resOk').style.display = 'none';
        window.location.href = '/signin/';
        return;
    }


    const payload = {
        full_name: name,
        email: email,
        number: number,
        date: date,
        time: time,
        guest: guest,
        special_request: special_request,
    }

    const response = await fetch('/api/reservationview/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access,
        },
        body: JSON.stringify(payload)
    })

    if (response.status === 429) {
        const msg = await response.json();
        showError(msg.detail || "Too many requests. Please try again later.");
        return;
    }

    if (response.ok) {
        msg = await response.json();
    } else {
        document.getElementById('resOk').style.display = 'none';
        window.location.href = '/signin/';
    }
}

async function searchItem() {
    const search = document.getElementById('searchInput').value;
    if (search.trim()) {
        window.location.href = `/menu/?search=${search}`;
    }
}