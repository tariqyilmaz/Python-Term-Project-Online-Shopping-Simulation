import uuid # Benzersiz sipariş ID'leri oluşturmak için
from datetime import datetime
from storage import write_json
import os

def create_order(cart, customer, payment_method):
    import uuid
    from datetime import datetime
    
    order_id = str(uuid.uuid4())[:8].upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # cart["items"] içinde bazen Decimal objeleri kalabiliyor, 
    # bunları güvenli bir şekilde string'e çevirmeliyiz.
    clean_items = {}
    for item_id, details in cart["items"].items():
        clean_items[item_id] = {
            "product": details["product"],
            "quantity": details["quantity"],
            "price": str(details["price"]) # Decimal -> String
        }

    order = {
        "order_id": order_id,
        "timestamp": timestamp,
        "customer": customer,
        "items": clean_items,
        "subtotal": str(cart.get("subtotal", "0.00")),
        "discount_total": str(cart.get("discount_total", "0.00")),
        "tax_amount": str(cart.get("tax_amount", "0.00")),
        "total": str(cart.get("total", "0.00")),
        "payment_method": payment_method,
        "status": "Completed"
    }
    return order

def update_inventory_after_order(products: list, order: dict) -> list:
    """
    Sipariş edilen ürünlerin miktarlarını katalogdaki stoktan düşer.
    """
    # Gerekli fonksiyon: def update_inventory_after_order(products: list, order: dict) -> list: 
    
    for item_id, details in order["items"].items():
        qty_purchased = details["quantity"]
        
        # Katalogdaki ilgili ürünü bul
        for product in products:
            if product["id"] == item_id:
                # Stoğu azalt
                product["stock"] -= qty_purchased
                break
                
    return products

def generate_receipt(order: dict, directory: str) -> str:
    """
    Sipariş bilgilerini içeren bir metin dosyası (makbuz) oluşturur.
    """
    # Gerekli fonksiyon: def generate_receipt (order: dict, directory: str) -> str: 
    
    file_name = f"receipt_{order['order_id']}.txt"
    file_path = os.path.join(directory, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("--- SATIŞ MAKBUZU ---\n")
        f.write(f"Sipariş ID: {order['order_id']}\n")
        f.write(f"Tarih: {order['timestamp']}\n")
        f.write("-" * 30 + "\n")
        f.write(f"Müşteri: {order['customer']['name']}\n")
        f.write(f"E-posta: {order['customer']['email']}\n")
        f.write("-" * 30 + "\n")
        
        for item_id, details in order["items"].items():
            name = details["product"]["name"]
            qty = details["quantity"]
            f.write(f"{name} x {qty}\n")
            
        f.write("-" * 30 + "\n")
        f.write(f"TOPLAM: {order['total']} TL\n")
        f.write(f"Ödeme: {order['payment_method']}\n")
        f.write("Bizi tercih ettiğiniz için teşekkürler!")

    return file_path