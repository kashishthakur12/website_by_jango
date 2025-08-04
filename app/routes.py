from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from .models import Product
import razorpay

# 👇 Use your Razorpay test keys here
client = razorpay.Client(auth=("rzp_test_abc123", "secret_xyz456"))

main = Blueprint('main', __name__)

@main.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Item added to cart')
    return redirect(url_for('main.home'))

@main.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    products = Product.query.filter(Product.id.in_(map(int, cart.keys()))).all()
    total = sum(p.price * cart[str(p.id)] for p in products)
    return render_template('cart.html', products=products, cart=cart, total=total)

@main.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form['quantity'])
    cart = session.get('cart', {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = quantity
    session['cart'] = cart
    return redirect(url_for('main.view_cart'))

@main.route('/pay', methods=['POST'])
def pay():
    cart = session.get('cart', {})
    products = Product.query.filter(Product.id.in_(map(int, cart.keys()))).all()
    total_amount = int(sum(p.price * cart[str(p.id)] for p in products) * 100)
    payment = client.order.create({'amount': total_amount, 'currency': 'INR', 'payment_capture': '1'})
    session['payment_id'] = payment['id']
    return render_template('pay.html', payment=payment)

@main.route('/payment_success')
def payment_success():
    session.pop('cart', None)
    return "Payment Successful!"

@main.route('/payment_failed')
def payment_failed():
    return "Payment Failed!"
