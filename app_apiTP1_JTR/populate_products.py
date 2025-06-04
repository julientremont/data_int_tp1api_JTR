from app_apiTP1_JTR.models import Product

def populate_products():
    """Ajouter 15 produits de test dans la base de données"""
    products_data = [
        {"name": "iPhone 15 Pro", "price": 1199.99, "description": "Latest Apple smartphone with titanium design"},
        {"name": "Samsung Galaxy S24", "price": 999.99, "description": "Android flagship with AI features"},
        {"name": "MacBook Pro M3", "price": 1999.99, "description": "Professional laptop with M3 chip"},
        {"name": "Sony WH-1000XM5", "price": 399.99, "description": "Premium noise-canceling headphones"},
        {"name": "iPad Pro 12.9", "price": 1099.99, "description": "Professional tablet with M2 chip"},
        {"name": "Nintendo Switch OLED", "price": 349.99, "description": "Gaming console with OLED screen"},
        {"name": "AirPods Pro 2", "price": 249.99, "description": "Wireless earbuds with spatial audio"},
        {"name": "Tesla Model Y", "price": 52999.99, "description": "Electric SUV with autopilot"},
        {"name": "PlayStation 5", "price": 499.99, "description": "Next-gen gaming console"},
        {"name": "Dell XPS 13", "price": 1299.99, "description": "Premium ultrabook laptop"},
        {"name": "Google Pixel 8", "price": 699.99, "description": "Google smartphone with AI photography"},
        {"name": "Microsoft Surface Pro 9", "price": 999.99, "description": "2-in-1 tablet and laptop"},
        {"name": "Dyson V15 Detect", "price": 749.99, "description": "Cordless vacuum with laser dust detection"},
        {"name": "Apple Watch Ultra 2", "price": 799.99, "description": "Premium smartwatch for athletes"},
        {"name": "Bose QuietComfort 45", "price": 329.99, "description": "Wireless noise-canceling headphones"}
    ]
    
    created_count = 0
    for product_data in products_data:
        # Vérifier si le produit existe déjà
        if not Product.objects.filter(name=product_data['name']).exists():
            Product.objects.create(**product_data)
            created_count += 1
    
    print(f"{created_count} nouveaux produits créés!")
    print(f"Total de produits en DB: {Product.objects.count()}")