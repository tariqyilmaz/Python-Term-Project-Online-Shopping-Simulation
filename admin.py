from decimal import Decimal
from typing import List, Dict

def calculate_total_revenue(orders: List[Dict]) -> Decimal:
    """Tüm tamamlanmış siparişlerden elde edilen toplam geliri hesaplar."""
    total_revenue = Decimal("0.00")
    for order in orders:
        # Siparişler kaydedilirken 'total' string olarak kaydedilmişti
        total_revenue += Decimal(order["total"])
    return total_revenue

def get_best_selling_products(orders: List[Dict]) -> Dict[str, int]:
    """Hangi üründen kaç adet satıldığını hesaplar."""
    sales_count = {}
    for order in orders:
        for item_id, details in order["items"].items():
            product_name = details["product"]["name"]
            quantity = details["quantity"]
            sales_count[product_name] = sales_count.get(product_name, 0) + quantity
    
    # Çoktan aza sıralayalım
    return dict(sorted(sales_count.items(), key=lambda x: x[1], reverse=True))

def add_new_product(products: List[Dict], new_product: Dict) -> List[Dict]:
    """Kataloğa yeni bir ürün ekler."""
    # Aynı ID'ye sahip ürün var mı kontrolü
    if any(p['id'] == new_product['id'] for p in products):
        print(f"Hata: {new_product['id']} ID'li ürün zaten mevcut.")
        return products
    
    products.append(new_product)
    return products

def update_stock_manually(products: List[Dict], product_id: str, new_stock: int) -> List[Dict]:
    """Belirli bir ürünün stoğunu manuel olarak günceller."""
    for product in products:
        if product["id"] == product_id:
            product["stock"] = new_stock
            break
    return products