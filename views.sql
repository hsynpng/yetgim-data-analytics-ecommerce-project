-- Power BI İçin Görünümler (Views)

-- Bu view, satış detaylarını müşteri ve ürün bilgileriyle zenginleştirir.
-- Power BI'da tek bir geniş tablo gibi çalışarak analizleri kolaylaştırır.

CREATE OR REPLACE VIEW vw_Satis_Detay AS
SELECT 
    sd.detay_id,
    s.siparis_id,
    s.siparis_tarihi,
    -- Takvim tablosu için yıl/ay/gün ayrıştırma (Power BI'da da yapılabilir ama burada hazır olması iyidir)
    EXTRACT(YEAR FROM s.siparis_tarihi) AS Yil,
    EXTRACT(MONTH FROM s.siparis_tarihi) AS Ay,
    
    -- Müşteri Bilgileri
    m.musteri_id,
    m.ad || ' ' || m.soyad AS Musteri_Tam_Ad,
    m.sehir AS Musteri_Sehir,
    m.ulke AS Musteri_Ulke,
    
    -- Ürün Bilgileri
    u.urun_id,
    u.urun_adi,
    u.kategori_adi,
    
    -- Satış Metrikleri
    sd.miktar,
    sd.birim_fiyat,
    sd.indirim_orani,
    
    -- Hesaplanmış Sütunlar
    (sd.miktar * sd.birim_fiyat) AS Brut_Tutar,
    (sd.miktar * sd.birim_fiyat * sd.indirim_orani) AS Indirim_Tutari,
    ((sd.miktar * sd.birim_fiyat) - (sd.miktar * sd.birim_fiyat * sd.indirim_orani)) AS Net_Tutar,
    
    -- Maliyet ve Kar Hesabı (Opsiyonel: Eğer ürün tablosundaki alış fiyatı sabitse buraya çekilebilir)
    -- Not: Gerçek hayatta alış fiyatı da zamanla değişir, sipariş detayına kaydedilmesi daha doğrudur.
    -- Burada basitlik adına güncel alış fiyatını kullanıyoruz.
    ((sd.miktar * sd.birim_fiyat) - (sd.miktar * sd.birim_fiyat * sd.indirim_orani)) - (sd.miktar * u.alis_fiyati) AS Tahmini_Kar,
    
    s.kargo_firmasi,
    s.durum AS Siparis_Durumu

FROM Siparis_Detay sd
JOIN Siparisler s ON sd.siparis_id = s.siparis_id
JOIN Urunler u ON sd.urun_id = u.urun_id
JOIN Musteriler m ON s.musteri_id = m.musteri_id;
