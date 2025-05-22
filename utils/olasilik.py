import random

# Simülasyonda kullanılabilecek örnek eşya listeleri
SAFE_ITEMS = [
    "Kitap", "Kıyafet", "Laptop", "Şarj Cihazı", "Kulaklık",
    "Gözlük", "Havlu", "Diş Fırçası", "Parfüm", "Ayakkabı",
    "Terlik", "Çorap", "Kalem", "Defter", "Telefon"
]

DANGEROUS_ITEMS = [
    "Bıçak", "Makas (Büyük)", "Çakı", "Sıvı (>100ml)",
    "Mermi", "Silah Parçası", "Yanıcı Madde"
]

DANGEROUS_BAG_PROBABILITY = 0.10

def generate_random_baggage(min_items=5, max_items=10):
    """
    Rastgele sayıda (5-10 arası) ve içerikte bagaj eşyası listesi oluşturur.
    Bagajların %10'u tehlikeli eşya içerir.
    """
    num_items = random.randint(min_items, max_items)
    baggage = []
    print(f"Rastgele Bagaj Oluşturuluyor ({num_items} eşya)...") # Loglama
    
    # Bagajın tehlikeli olup olmadığını belirle
    is_dangerous_bag = random.random() < DANGEROUS_BAG_PROBABILITY
    
    if is_dangerous_bag:
        # Tehlikeli bagaj için en az 1 tehlikeli eşya ekle
        dangerous_item = random.choice(DANGEROUS_ITEMS)
        baggage.append(dangerous_item)
        print(f"  -> Tehlikeli Eşya Eklendi: {dangerous_item}") # Loglama
        num_items -= 1  # Bir eşya zaten eklendi
    
    # Kalan eşyaları ekle
    for _ in range(num_items):
        item = random.choice(SAFE_ITEMS)
        baggage.append(item)
    
    print(f"Oluşturulan Bagaj: {baggage}") # Loglama
    return baggage

def esya_tehlikeli_mi(item_name):
    """
    Verilen bir eşya isminin tehlikeli eşyalar listesinde olup olmadığını kontrol eder.
    Proje tanımındaki `esya_tehlikeli_mi` fonksiyonuna karşılık gelir.
    """
    is_dangerous = item_name in DANGEROUS_ITEMS
    return is_dangerous

# === İsteğe Bağlı Yardımcı Fonksiyonlar ===

def load_blacklist_from_file(filepath="data/kara_liste.json"):
    """
    JSON dosyasından kara liste yolcu ID'lerini yükler.
    """
    import json # Sadece burada gerektiği için lokal import
    try:
        with open(filepath, 'r') as f:
            blacklist_ids = json.load(f)
            print(f"Kara liste yüklendi: {filepath} -> {len(blacklist_ids)} kayıt.")
            return blacklist_ids
    except FileNotFoundError:
        print(f"Uyarı: Kara liste dosyası bulunamadı: {filepath}. Boş liste varsayılıyor.")
        return []
    except json.JSONDecodeError:
        print(f"Hata: Kara liste dosyası ({filepath}) geçerli JSON formatında değil.")
        return []
    except Exception as e:
        print(f"Kara liste yüklenirken beklenmedik hata: {e}")
        return []