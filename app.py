from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import random

app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

# Sample product data - in a real app, this would come from a database
PRODUCTS = {
    'men': [
        {'id': 'm1', 'name': 'Classic T-Shirt', 'price': 29.99, 'image': 'men_tshirt.jpg', 'category': 'men'},
        {'id': 'm2', 'name': 'Slim Fit Jeans', 'price': 49.99, 'image': 'men_jeans.jpg', 'category': 'men'},
        {'id': 'm3', 'name': 'Casual Shirt', 'price': 39.99, 'image': 'men_shirt.jpg', 'category': 'men'},
        {'id': 'm4', 'name': 'Formal Blazer', 'price': 89.99, 'image': 'men_blazer.jpg', 'category': 'men'}
    ],
    'women': [
        {'id': 'w1', 'name': 'Summer Dress', 'price': 59.99, 'image': 'women_dress.jpg', 'category': 'women'},
        {'id': 'w2', 'name': 'Skinny Jeans', 'price': 54.99, 'image': 'women_jeans.jpg', 'category': 'women'},
        {'id': 'w3', 'name': 'Blouse', 'price': 34.99, 'image': 'women_blouse.jpg', 'category': 'women'},
        {'id': 'w4', 'name': 'Cardigan', 'price': 44.99, 'image': 'women_cardigan.jpg', 'category': 'women'}
    ],
    'kids': [
        {'id': 'k1', 'name': 'Kids T-Shirt', 'price': 19.99, 'image': 'kids_tshirt.jpg', 'category': 'kids'},
        {'id': 'k2', 'name': 'Kids Jeans', 'price': 29.99, 'image': 'kids_jeans.jpg', 'category': 'kids'},
        {'id': 'k3', 'name': 'Kids Dress', 'price': 34.99, 'image': 'kids_dress.jpg', 'category': 'kids'},
        {'id': 'k4', 'name': 'Kids Hoodie', 'price': 39.99, 'image': 'kids_hoodie.jpg', 'category': 'kids'}
    ]
}

# Initialize shopping cart in session
def init_cart():
    if 'cart' not in session:
        session['cart'] = []

# Routes
@app.route('/')
def home():
    featured_products = []
    for category in PRODUCTS:
        featured_products.extend(PRODUCTS[category][:2])  # Add 2 products from each category
    return render_template('index.html', featured_products=featured_products)

@app.route('/category/<category>')
def category(category):
    if category in PRODUCTS:
        return render_template('category.html', 
                              products=PRODUCTS[category], 
                              category=category.capitalize())
    return redirect(url_for('home'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    # Find the product with the given ID
    for category in PRODUCTS:
        for product in PRODUCTS[category]:
            if product['id'] == product_id:
                # Get related products from the same category
                related_products = PRODUCTS[product['category']]
                return render_template('product_detail.html', product=product, related_products=related_products)
    
    # If product not found
    flash('Product not found', 'error')
    return redirect(url_for('home'))

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    init_cart()
    product_id = request.form.get('product_id')
    
    # Find the product
    product = None
    for category in PRODUCTS:
        for p in PRODUCTS[category]:
            if p['id'] == product_id:
                product = p
                break
        if product:
            break
    
    if product:
        # Check if product already in cart
        for item in session['cart']:
            if item['id'] == product_id:
                item['quantity'] += 1
                session.modified = True
                flash(f"{product['name']} quantity updated in cart!", 'success')
                return redirect(request.referrer or url_for('home'))
        
        # Add new product to cart
        cart_item = product.copy()
        cart_item['quantity'] = 1
        session['cart'].append(cart_item)
        session.modified = True
        flash(f"{product['name']} added to cart!", 'success')
    else:
        flash('Product not found', 'error')
    
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    init_cart()
    cart_total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('cart.html', cart=session['cart'], cart_total=cart_total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    init_cart()
    product_id = request.form.get('product_id')
    action = request.form.get('action')
    
    for i, item in enumerate(session['cart']):
        if item['id'] == product_id:
            if action == 'increase':
                session['cart'][i]['quantity'] += 1
            elif action == 'decrease':
                session['cart'][i]['quantity'] -= 1
                if session['cart'][i]['quantity'] <= 0:
                    session['cart'].pop(i)
            elif action == 'remove':
                session['cart'].pop(i)
            session.modified = True
            break
    
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    init_cart()
    if not session['cart']:
        flash('Your cart is empty', 'error')
        return redirect(url_for('home'))
    
    cart_total = sum(item['price'] * item['quantity'] for item in session['cart'])
    return render_template('checkout.html', cart=session['cart'], cart_total=cart_total)

@app.route('/place_order', methods=['POST'])
def place_order():
    init_cart()
    # In a real application, you would process payment and store order in database
    
    # Clear the cart after successful order
    session['cart'] = []
    session.modified = True
    
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('order_confirmation'))

@app.route('/order_confirmation')
def order_confirmation():
    order_number = f"{100000 + random.randint(1, 10000):08d}"
    order_date = datetime.now()
    delivery_date = order_date + timedelta(days=7)
    return render_template('order_confirmation.html', 
                          order_number=order_number,
                          order_date=order_date,
                          delivery_date=delivery_date)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True) 