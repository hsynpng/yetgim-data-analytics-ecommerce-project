-- E-Ticaret Satış Analizi Projesi - PostgreSQL Şeması

-- Eğer varsa önce tabloları temizle (Sıralama önemli: FK bağımlılıkları yüzünden sondan başa)
DROP TABLE IF EXISTS Siparis_Detay;
DROP TABLE IF EXISTS Siparisler;
DROP TABLE IF EXISTS Urunler;
DROP TABLE IF EXISTS Musteriler;

-- 1. Müşteriler Tablosu
CREATE TABLE Musteriler (
    musteri_id SERIAL PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sehir VARCHAR(50),
    ulke VARCHAR(50),
    kayit_tarihi DATE DEFAULT CURRENT_DATE
);

-- 2. Ürünler Tablosu
CREATE TABLE Urunler (
    urun_id SERIAL PRIMARY KEY,
    urun_adi VARCHAR(100) NOT NULL,
    kategori_adi VARCHAR(50), -- Kategori ID yerine basitlik için adını tutuyoruz, normalize edilebilir.
    alis_fiyati NUMERIC(10, 2) NOT NULL,
    satis_fiyati NUMERIC(10, 2) NOT NULL,
    stok_miktari INT DEFAULT 0
);

-- 3. Siparişler Tablosu
CREATE TABLE Siparisler (
    siparis_id SERIAL PRIMARY KEY,
    musteri_id INT NOT NULL,
    siparis_tarihi DATE NOT NULL,
    kargo_firmasi VARCHAR(50),
    durum VARCHAR(20) CHECK (durum IN ('Hazırlanıyor', 'Kargoda', 'Teslim Edildi', 'İptal')),
    FOREIGN KEY (musteri_id) REFERENCES Musteriler(musteri_id)
);

-- 4. Sipariş Detay Tablosu
CREATE TABLE Siparis_Detay (
    detay_id SERIAL PRIMARY KEY,
    siparis_id INT NOT NULL,
    urun_id INT NOT NULL,
    miktar INT NOT NULL CHECK (miktar > 0),
    birim_fiyat NUMERIC(10, 2) NOT NULL, -- Sipariş anındaki fiyat (ürün fiyatı değişebilir)
    indirim_orani NUMERIC(3, 2) DEFAULT 0.00, -- Örn: 0.10 (%10 indirim)
    FOREIGN KEY (siparis_id) REFERENCES Siparisler(siparis_id),
    FOREIGN KEY (urun_id) REFERENCES Urunler(urun_id)
);

-- İndeksler (Performans için)
CREATE INDEX idx_siparis_musteri ON Siparisler(musteri_id);
CREATE INDEX idx_detay_siparis ON Siparis_Detay(siparis_id);
CREATE INDEX idx_detay_urun ON Siparis_Detay(urun_id);
