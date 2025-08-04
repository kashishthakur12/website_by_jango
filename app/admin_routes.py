from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .models import Product, db, User

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('admin.add_product'))
        flash("Invalid credentials")
    return render_template('login.html')

@admin.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin.route('/admin/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        new_product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            description=request.form['description'],
            image_url=request.form['image_url']
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added!')
        return redirect(url_for('main.home'))
    return render_template('add_product.html')

@admin.route('/admin/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.description = request.form['description']
        product.image_url = request.form['image_url']
        db.session.commit()
        flash('Product updated!')
        return redirect(url_for('main.home'))
    return render_template('edit_product.html', product=product)

@admin.route('/admin/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!')
    return redirect(url_for('main.home'))
