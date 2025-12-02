from typing import List, Dict, Any
from decimal import Decimal, getcontext

getcontext().prec = 28 #Decimalin hassasiyetini arttırdık

# cart.py (Devamı)

def add_to_cart(cart: Dict[str, Any], product: Dict[str, Any], quantity: int) -> Dict[str, Any]:
    
    product_id = product.get("id")
    
    #Sepete negatif sayıda ürün ekleme
    if quantity <= 0:
        print("Uyari: Sepete eklenen miktar sifirdan büyük olmalidir.")
        return cart

    current_stock = product.get("stock", 0)
    
    # Sepetteki mevcut miktar (Eğer ürün sepette zaten varsa)
    current_cart_qty = cart.get("items", {}).get(product_id, {}).get("quantity", 0)
    new_total_qty = current_cart_qty + quantity

    # Stok Kontrolü 
    if new_total_qty > current_stock:
        print(f"HATA: '{product['name']}' ürünü için stok yetersiz.")
        print(f"Mevcut Stok: {current_stock}, Sepette İstenen Toplam Miktar: {new_total_qty}")
        return cart

    # Sepet (cart) yapısı boşsa başlat
    if "items" not in cart:
        cart["items"] = {}

    # Ürün sepette zaten varsa miktarı güncelle
    if product_id in cart["items"]:
        cart["items"][product_id]["quantity"] = new_total_qty
    # Ürün sepete ilk kez ekleniyorsa
    else:
        # Fiyatı Decimal'e dönüştürerek saklayın
        price_decimal = Decimal(str(product["price"]))
        
        cart["items"][product_id] = {
            "product": product,
            "quantity": quantity,
            "price": price_decimal # Decimal formatında fiyat
        }
    
    print(f"{quantity} adet '{product['name']}' sepete eklendi.")
    return cart

def remove_from_cart(cart: Dict[str, Any], product_id: str) -> Dict[str, Any]:

    if product_id in cart.get("items", {}):
        del cart["items"][product_id]
        print(f"Ürün ID {product_id} sepetten çikarildi.")
    else:
        print(f"Uyari: Ürün ID {product_id} sepette bulunamadi.")       
    return cart

def update_quantity(cart: Dict[str, Any], product_id: str, quantity: int) -> Dict[str, Any]:
    
    if product_id not in cart.get("items", {}):
        print(f"Hata: Ürün ID {product_id} sepette bulunamadi.")
        return cart
        
    #Negatif miktar olmamalı
    if quantity < 0:
        print("Hata: Miktar negatif olamaz.")
        return cart
    
    # Eğer yeni miktar 0 ise, ürünü tamamen sepetten çıkar
    if quantity == 0:
        print(f"Ürün ID {product_id} miktari 0 olduğu için sepetten çikariliyor.")
        return remove_from_cart(cart, product_id)
        
    # Stok Kontrolü (Sadece güncelleme yapıyorsak)
    product = cart["items"][product_id]["product"]
    current_stock = product.get("stock", 0)
    
    if quantity > current_stock:
        print(f"HATA: '{product['name']}' ürünü için stok yetersiz.")
        print(f"Mevcut Stok: {current_stock}, İstenen Miktar: {quantity}")
        return cart
        
    # Başarılı güncelleme
    cart["items"][product_id]["quantity"] = quantity
    print(f"Ürün ID {product_id} için yeni miktar: {quantity}")
    return cart