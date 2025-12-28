from storage import load_json, write_json
from typing import List, Dict

# Urunleri veri dosyasindan yukluyor
def load_products(path: str) -> List[Dict]:
    return load_json(path)

# Urun katalogunu veri dosyasina kaydediyor
def save_products(path: str, products: List[Dict]) -> None:
    write_json(path, products)

#Urunleri araıyor
def search_products(products: List[Dict], keyword: str) -> List[Dict]:
    keyword = keyword.lower()
    return [
        p for p in products 
        if keyword in p.get('name', '').lower() 
        or keyword in p.get('description', '').lower()
    ]

#Urunleri filtreliyor
def filter_by_category(products: List[Dict], category: str) -> List[Dict]:
    category = category.lower()
    return [p for p in products if p.get('category', '').lower() == category]