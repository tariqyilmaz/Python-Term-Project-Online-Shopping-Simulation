import catalog
import cart
import orders
import storage
import admin
from typing import List, Dict
from decimal import Decimal
import os

#Data yolları
PRODUCTS_PATH = 'data/products.json'
ORDERS_PATH = 'data/orders.json'
RECEIPTS_DIR = 'receipts/'
ADMIN_PASSWORD = "1234"

for folder in ['data', 'receipts']:
    if not os.path.exists(folder):
        os.makedirs(folder)

PROMO_RULES = {
    "SAVE10": {"type": "percentage", "value": 10},
    "FLAT50": {"type": "fixed", "value": 50}
}

def display_products(products: List[Dict]):
    """Ürün listesini kullanıcı dostu bir formatta görüntüler."""
    if not products:
        print("\nKatalogda ürün bulunamadı.")
        return

    print("\n--- ÜRÜN KATALOĞU ---")
    print(f"{'ID':<6} | {'İSİM':<35} | {'FİYAT':<8} | {'STOK':<4} | KATEGORİ")
    print("-" * 75)
    
    for p in products:
        price_formatted = f"{float(p['price']):.2f}"
        print(f"{p['id']:<6} | {p['name'][:35]:<35} | {price_formatted:<8} | {p['stock']:<4} | {p['category']}")
    print("-" * 75)

def show_cart(cart_data: dict):
    """Sepet içeriğini ve özetini tablo gösterir"""
    if not cart_data.get("items"):
        print("\nSepetiniz şu an boş.")
        return

    print("\n--- SEPETİNİZ ---")
    print(f"{'Ürün':<25} | {'Adet':<6} | {'Birim Fiyat':<12} | {'Toplam'}")
    print("-" * 65)

    for item_id, details in cart_data["items"].items():
        p_name = details['product']['name']
        qty = details['quantity']
        price = details['price']
        line_total = Decimal(str(price)) * qty
        print(f"{p_name[:25]:<25} | {qty:<6} | {price:<12} | {line_total:.2f}")

    print("-" * 65)
    print(f"{'ARA TOPLAM:':<48} {cart_data.get('subtotal', '0.00'):>10} TL")
    print(f"{'İNDİRİM:':<48} -{cart_data.get('discount_total', '0.00'):>9} TL")
    print(f"{'VERGİ (%20):':<48} {cart_data.get('tax_amount', '0.00'):>10} TL")
    print("-" * 65)
    print(f"{'GENEL TOPLAM:':<48} {cart_data.get('total', '0.00'):>10} TL")

def admin_panel(products, all_orders):
    """Yönetici işlemlerinin yapıldığı döngü"""
    while True:
        print("\n--- YÖNETİCİ PANELİ ---")
        print("1. Toplam Geliri Gör")
        print("2. En Çok Satan Ürünler")
        print("3. Yeni Ürün Ekle")
        print("4. Ana Menüye Dön")
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            all_orders = storage.load_json(ORDERS_PATH) # Güncel veriyi oku
            revenue = admin.calculate_total_revenue(all_orders)
            print(f"\n💰 Toplam Gelir: {revenue} TL")
            
        elif choice == '2':
            all_orders = storage.load_json(ORDERS_PATH)
            best_sellers = admin.get_best_selling_products(all_orders)
            print("\n🔥 En Çok Satanlar:")
            for name, qty in best_sellers.items():
                print(f"- {name}: {qty} adet")
                
        elif choice == '3':
            print("\n--- YENİ ÜRÜN EKLEME ---")
            new_id = input("Ürün ID: ")
            new_name = input("Ürün Adı: ")
            new_category = input("Kategori: ")
            new_price = float(input("Fiyat: "))
            new_stock = int(input("Başlangıç Stoğu: "))

            new_product = {
                "id": new_id, "name": new_name, "category": new_category,
                "price": new_price, "stock": new_stock
            }
            products = admin.add_new_product(products, new_product)
            catalog.save_products(PRODUCTS_PATH, products)
            print(f"\n✅ {new_name} kataloğa eklendi!")
            
        elif choice == '4':
            break
    return products

def main_menu():
    products = catalog.load_products(PRODUCTS_PATH)
    shopping_cart = {"items": {}, "applied_discount": Decimal("0.00")}
    TAX_RATE = 0.20 # %20 KDV

    while True:
        print("\n--- ONLINE ALIŞVERİŞ SİSTEMİ ---")
        print("1. Ürünleri Listele")
        print("2. Sepete Ürün Ekle")
        print("3. Sepeti Görüntüle")
        print("4. Promosyon Kodu Uygula")
        print("5. Ödeme Yap (Satın Al)")
        print("6. Yönetici Paneli")
        print("7. Çıkış")
        
        secim = input("Seçiminiz: ")

        if secim == '1':
            display_products(products)

        elif secim == '2':
            product_id = input("Ürün ID: ")
            target_product = next((p for p in products if p['id'] == product_id), None)
            if target_product:
                try:
                    qty = int(input(f"Kaç adet {target_product['name']}? "))
                    shopping_cart = cart.add_to_cart(shopping_cart, target_product, qty)
                except ValueError:
                    print("Lütfen geçerli bir sayı girin!")
            else:
                print("Hata: Ürün bulunamadı!")

        elif secim == '3':
            shopping_cart = cart.calculate_totals(shopping_cart, TAX_RATE)
            show_cart(shopping_cart)

        elif secim == '4':
            code = input("Promosyon kodu: ")
            shopping_cart = cart.apply_promo_code(shopping_cart, code, PROMO_RULES)

        elif secim == '5':
            if not shopping_cart.get("items"):
                print("Sepetiniz boş!")
            else:
                shopping_cart = cart.calculate_totals(shopping_cart, TAX_RATE)
                customer = {"name": input("Ad Soyad: "), "email": input("E-posta: ")}
                
                new_order = orders.create_order(shopping_cart, customer, "Kredi Kartı")
                products = orders.update_inventory_after_order(products, new_order)
                catalog.save_products(PRODUCTS_PATH, products)
                
                all_orders = storage.load_json(ORDERS_PATH)
                all_orders.append(new_order)
                storage.write_json(ORDERS_PATH, all_orders)
                
                orders.generate_receipt(new_order, RECEIPTS_DIR)
                print("\n✅ Satın alma başarılı! Makbuz oluşturuldu.")
                shopping_cart = {"items": {}, "applied_discount": Decimal("0.00")}

        elif secim == '6':
            password = input("Admin Şifresi: ")
            if password == ADMIN_PASSWORD:
                all_orders = storage.load_json(ORDERS_PATH)
                products = admin_panel(products, all_orders)
            else:
                print("Hatalı şifre!")

        elif secim == '7':
            print("Güle güle!")
            break

if __name__ == '__main__':
    main_menu()