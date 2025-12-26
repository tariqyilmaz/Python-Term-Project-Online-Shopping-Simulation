import catalog
import cart
import orders
import storage
import admin
from typing import List, Dict
from decimal import Decimal

# Veri dosyasının yolu
PRODUCTS_PATH = 'data/products.json'
ADMIN_PASSWORD = "1234"

PROMO_RULES = {
    "SAVE10": {"type": "percentage", "value": 10}, # %10 indirim
    "FLAT50": {"type": "fixed", "value": 50}      # 50 TL indirim
}

def display_products(products: List[Dict]):
    """Ürün listesini kullanici dostu bir formatta görüntüler."""
    if not products:
        print("Katalogda ürün bulunamadi.")
        return

    # Başlık
    print("\n--- Ürün Kataloğu ---")
    print(f"{'ID':<6} | {'İSİM':<35} | {'FİYAT':<8} | {'STOK':<4} | KATEGORİ")
    print("-" * 65)
    
    # Ürünleri listele
    for p in products:
        # Fiyatı 2 ondalık basamakla formatlayın
        price_formatted = f"{p['price']:.2f}"
        print(f"{p['id']:<6} | {p['name']:<35} | {price_formatted:<8} | {p['stock']:<4} | {p['category']}")
    print("-" * 65)

def main_menu():
    products = catalog.load_products(PRODUCTS_PATH)
    shopping_cart = {"items": {}, "applied_discount": Decimal("0.00")} # Boş sepet [cite: 36]
    TAX_RATE = 0.10 # %20 KDV [cite: 43]

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
            display_products(products) # Hafta 1'de yazdığımız fonksiyon

        elif secim == '2':
            product_id = input("Eklemek istediğiniz ürün ID: ")
            # Katalogda ürünü bulalım
            target_product = next((p for p in products if p['id'] == product_id), None)
            
            if target_product:
                qty = int(input(f"Kaç adet {target_product['name']} eklemek istersiniz? "))
                shopping_cart = cart.add_to_cart(shopping_cart, target_product, qty) # [cite: 41]
            else:
                print("Hata: Ürün bulunamadı!")

        elif secim == '3':
            # Önce toplamları hesapla [cite: 43]
            shopping_cart = cart.calculate_totals(shopping_cart, TAX_RATE)
            show_cart(shopping_cart)

        elif secim == '4':
            code = input("Promosyon kodunu giriniz: ")
            shopping_cart = cart.apply_promo_code(shopping_cart, code, PROMO_RULES) # [cite: 44]
        elif secim == '5':
            # Önce sepetin dolu olup olmadığını kontrol et
            if not shopping_cart.get("items"):
                print("Sepetiniz boş!")
            else:
                shopping_cart = cart.calculate_totals(shopping_cart, 0.20)
                # 1. Müşteri bilgilerini al
                customer = {
                    "name": input("Ad Soyad: "),
                    "email": input("E-posta: ")
                }
                # 2. Siparişi oluştur (orders.py'deki fonksiyonun)
                new_order = orders.create_order(shopping_cart, customer, "Kredi Kartı")
        
                # 2. Stokları Güncelle
                products = orders.update_inventory_after_order(products, new_order)
                catalog.save_products('data/products.json', products)
        
                # --- BURAYA EKLE: Siparişi Dosyaya Kaydetme ---
                all_orders = storage.load_json('data/orders.json')
                all_orders.append(new_order)
                storage.write_json('data/orders.json', all_orders)
                # ----------------------------------------------
        
                # 3. Makbuz Üret
                orders.generate_receipt(new_order, 'receipts/')
        
                print("\n✅ Sipariş Başarıyla Tamamlandı!")
                shopping_cart = {"items": {}, "applied_discount": Decimal("0.00")}
        
        elif secim == '6':
            sifre = input("Admin Şifresi: ")
            if sifre == "1234":  # Belirlediğin şifre
                all_orders = storage.load_json('data/orders.json')
                print(f"\n--- YÖNETİCİ RAPORU ---")
                revenue = admin.calculate_total_revenue(all_orders)
                best_sellers = admin.get_best_selling_products(all_orders)
                print(f"Toplam Gelir: {revenue} TL")
                print(f"En Çok Satanlar: {best_sellers}")
            else:
                print("Yetkisiz Giriş!")

        elif secim == '7':
            break

def show_cart(cart_data: dict):
    """Sepet içeriğini ve mali özetini tablo olarak gösterir."""
    if not cart_data.get("items"):
        print("\nSepetiniz şu an boş.")
        return

    print("\n--- SEPETİNİZ ---")
    print(f"{'Ürün':<25} | {'Adet':<6} | {'Birim Fiyat':<12} | {'Toplam'}")
    print("-" * 60)

    for item_id, details in cart_data["items"].items():
        p_name = details['product']['name']
        qty = details['quantity']
        price = details['price']
        line_total = price * qty
        print(f"{p_name[:25]:<25} | {qty:<6} | {price:<12} | {line_total}")

    print("-" * 60)
    # calculate_totals'dan gelen verileri yazdıralım [cite: 37, 43]
    print(f"{'ARA TOPLAM:':<46} {cart_data.get('subtotal', 0):>10} TL")
    print(f"{'İNDİRİM:':<46} -{cart_data.get('discount_total', 0):>9} TL")
    print(f"{'VERGİ (%20):':<46} {cart_data.get('tax_amount', 0):>10} TL")
    print("-" * 60)
    print(f"{'GENEL TOPLAM:':<46} {cart_data.get('total', 0):>10} TL")

def checkout_flow(shopping_cart, products):
    """Müşteriden bilgi alıp siparişi tamamlayan akış."""
    if not shopping_cart.get("items"):
        print("Sepetiniz boş, ödeme yapılamaz!")
        return products, shopping_cart

    print("\n--- ÖDEME EKRANI ---")
    customer = {
        "name": input("Adınız Soyadınız: "),
        "email": input("E-posta Adresiniz: "),
        "address": input("Teslimat Adresiniz: ")
    }
    
    print("\nÖdeme Yöntemi Seçin:")
    print("1. Kredi Kartı\n2. Nakit\n3. Dijital Cüzdan")
    p_choice = input("Seçiminiz: ")
    methods = {"1": "Kredi Kartı", "2": "Nakit", "3": "Dijital Cüzdan"}
    payment_method = methods.get(p_choice, "Bilinmeyen")

    # 1. Siparişi Oluştur
    new_order = orders.create_order(shopping_cart, customer, payment_method)
    
    # 2. Stokları Güncelle
    updated_products = orders.update_inventory_after_order(products, new_order)
    
    # 3. Verileri Kaydet (storage modülünü kullanarak)
    catalog.save_products('data/products.json', updated_products)
    
    # Mevcut siparişleri yükle, yenisini ekle ve geri kaydet
    all_orders = storage.load_json('data/orders.json')
    all_orders.append(new_order)
    storage.write_json('data/orders.json', all_orders)
    
    # 4. Makbuz Oluştur
    receipt_path = orders.generate_receipt(new_order, 'receipts/')
    
    print(f"\n✅ Sipariş Başarıyla Tamamlandı!")
    print(f"Makbuzunuz oluşturuldu: {receipt_path}")
    
    # Sepeti temizle
    return updated_products, {"items": {}, "applied_discount": Decimal("0.00")}

def admin_panel(products, all_orders):
    password = input("Yönetici şifresini girin: ")
    if password != ADMIN_PASSWORD:
        print("Hatalı şifre! Giriş engellendi.")
        return products

    while True:
        print("\n--- YÖNETİCİ PANELİ ---")
        print("1. Toplam Geliri Gör")
        print("2. En Çok Satan Ürünler")
        print("3. Stok Güncelle")
        print("4. Yeni Ürün Ekle")
        print("5. Ana Menüye Dön")
        
        choice = input("Seçiminiz: ")
        
        if choice == '1':
            revenue = admin.calculate_total_revenue(all_orders)
            print(f"Toplam Gelir: {revenue} TL")
        elif choice == '2':
            best_sellers = admin.get_best_selling_products(all_orders)
            for name, qty in best_sellers.items():
                print(f"{name}: {qty} adet satıldı")
        elif choice == '5':
            break
    return products

if __name__ == '__main__':
    main_menu()