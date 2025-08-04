# seed_products.py

from app import create_app
from app.models import db, Product

app = create_app()
app.app_context().push()

# Add sample products
p1 = Product(name="Lip Glaze no. 01", price=599.00, description="Nourishing lip gloss with a soft tint.",
             image_url="https://cdn.shopify.com/s/files/1/0604/7285/2369/products/lip-glaze-01.jpg")

p2 = Product(name="Velvet Cheeks no. 01", price=749.00, description="Smooth mousse blush for natural glow.",
             image_url="https://cdn.shopify.com/s/files/1/0604/7285/2369/products/velvet-cheeks-01.jpg")

db.session.add_all([p1, p2])
db.session.commit()

print("✅ Products added successfully.")
