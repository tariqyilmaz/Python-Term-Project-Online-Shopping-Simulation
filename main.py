import catalog
from typing import List, Dict

# Veri dosyasının yolu
PRODUCTS_PATH = 'data/products.json'

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

    while True:
        print("\n--- ANA MENÜ ---")
        print("1. Ürünlere Göz At")
        print("2. Ürün Ara (Anahtar Kelime)")
        print("3. Kategoriye Göre Filtrele")
        print("4. Yönetici Girişi (İleride Eklenecek)")
        print("5. Çikiş")
        
        choice = input("Seçiminizi yapin (1-5): ")

        if choice == '1':
            display_products(products)
        elif choice == '2':
            keyword = input("Aranacak anahtar kelimeyi girin: ")
            results = catalog.search_products(products, keyword)
            print(f"\n--- '{keyword}' Arama Sonuçlari ---")
            display_products(results)
        elif choice == '3':
            category = input("Filtrelenecek kategoriyi girin (Örn: Elektronik, Giyim): ")
            results = catalog.filter_by_category(products, category)
            print(f"\n--- '{category}' Kategori Sonuçlari ---")
            display_products(results)
        elif choice == '4':
            print("Yönetici girişi işlevi sonraki aşamada eklenecektir.")
        elif choice == '5':
            print("Online Alişveriş Simülasyonu'ndan çikiliyor. Güle güle!")
            break
        else:
            print("Geçersiz seçim. Lütfen 1 ile 5 arasinda bir sayi girin.")

if __name__ == '__main__':
    main_menu()