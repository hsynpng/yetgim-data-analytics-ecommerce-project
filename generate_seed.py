import random
import datetime

# --- Ayarlar ---
NUM_CUSTOMERS = 60
NUM_PRODUCTS = 20
NUM_ORDERS = 150
MAX_ITEMS_PER_ORDER = 5

OUTPUT_FILE = "seed_data.sql"

# --- Yardımcı Veriler ---
FIRST_NAMES = ["Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Zeynep", "Mustafa", "Elif", "Hüseyin", "Cem", "Canan", "Burak", "Selin", "Deniz", "Emre"]
LAST_NAMES = ["Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç"]
CITIES = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep"]
PRODUCT_CATEGORIES = {
    "Elektronik": [("Laptop", 15000, 20000), ("Akıllı Telefon", 10000, 14000), ("Kulaklık", 500, 800), ("Tablet", 3000, 4500)],
    "Giyim": [("T-Shirt", 100, 250), ("Kot Pantolon", 300, 600), ("Mont", 800, 1500), ("Spor Ayakkabı", 1200, 2000)],
    "Ev & Yaşam": [("Kahve Makinesi", 1500, 2500), ("Ütü", 800, 1200), ("Nevresim Takımı", 400, 700)]
}
CARGO_FIRMS = ["Yurtiçi Kargo", "Aras Kargo", "MNG Kargo", "PTT Kargo"]
ORDER_STATUSES = ["Teslim Edildi", "Teslim Edildi", "Teslim Edildi", "Kargoda", "Hazırlanıyor", "İptal"] # Teslim edildi ağırlıklı olsun

def generate_date(start_year=2023, end_year=2025):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

def escape_sql(text):
    return text.replace("'", "''")

sql_statements = []

# 1. Müşteriler
print("Müşteriler oluşturuluyor...")
sql_statements.append("-- Müşteri Verileri")
for _ in range(NUM_CUSTOMERS):
    ad = random.choice(FIRST_NAMES)
    soyad = random.choice(LAST_NAMES)
    email = f"{ad.lower()}.{soyad.lower()}{random.randint(1,99)}@ornekmail.com"
    sehir = random.choice(CITIES)
    ulke = "Türkiye"
    tarih = generate_date(2023, 2024)
    sql_statements.append(f"INSERT INTO Musteriler (ad, soyad, email, sehir, ulke, kayit_tarihi) VALUES ('{ad}', '{soyad}', '{escape_sql(email)}', '{sehir}', '{ulke}', '{tarih}');")

# 2. Ürünler
print("Ürünler oluşturuluyor...")
sql_statements.append("\n-- Ürün Verileri")
product_ids = [] # Ürün ID'lerini takip etmek için (Generated ID bilmiyoruz ama sırayla 1'den başlayacak varsayımıyla eşleştireceğiz)
current_p_id = 1

for category, products in PRODUCT_CATEGORIES.items():
    for p_name, buy_price, sell_price in products:
        stok = random.randint(10, 100)
        sql_statements.append(f"INSERT INTO Urunler (urun_adi, kategori_adi, alis_fiyati, satis_fiyati, stok_miktari) VALUES ('{p_name}', '{category}', {buy_price}, {sell_price}, {stok});")
        product_ids.append({'id': current_p_id, 'price': sell_price})
        current_p_id += 1

# 3. Siparişler ve Detaylar
print("Siparişler oluşturuluyor...")
sql_statements.append("\n-- Sipariş ve Detay Verileri")
for i in range(1, NUM_ORDERS + 1):
    musteri_id = random.randint(1, NUM_CUSTOMERS)
    siparis_tarihi = generate_date(2024, 2025)
    kargo = random.choice(CARGO_FIRMS)
    durum = random.choice(ORDER_STATUSES)
    
    sql_statements.append(f"INSERT INTO Siparisler (musteri_id, siparis_tarihi, kargo_firmasi, durum) VALUES ({musteri_id}, '{siparis_tarihi}', '{kargo}', '{durum}');")
    
    # Sipariş Detayları (Son eklenen sipariş ID'si 'i' olacak çünkü SERIAL sıralı artar - Transaction içinde yapılsa last_insert_id kullanılır ama bu basit script)
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    selected_products = random.sample(product_ids, num_items)
    
    for prod in selected_products:
        miktar = random.randint(1, 3)
        birim_fiyat = prod['price'] # Fiyat değişimi yok varsayalım
        indirim = random.choice([0.00, 0.05, 0.10, 0.00, 0.00]) # Bazen indirim olsun
        
        sql_statements.append(f"INSERT INTO Siparis_Detay (siparis_id, urun_id, miktar, birim_fiyat, indirim_orani) VALUES ({i}, {prod['id']}, {miktar}, {birim_fiyat}, {indirim});")

# Dosyaya Yazma
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("-- E-Ticaret Örnek Veri Seti (Otomatik Oluşturuldu)\n")
    f.write("\n".join(sql_statements))

print(f"Bitti! {OUTPUT_FILE} oluşturuldu.")
