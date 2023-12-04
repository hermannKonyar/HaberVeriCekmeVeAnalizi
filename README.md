# HaberVeriCekmeVeAnalizi

## Haber Veri Çekme ve Analizi
Bu proje, belirli bir haber sitesinden haber verilerini çekmek, analiz etmek ve bu verileri MongoDB'ye kaydetmek için tasarlanmıştır. Python kullanılarak geliştirilen bu projede, web scraping, veritabanı yönetimi ve basit veri analizi teknikleri kullanılmaktadır.

## Özellikler
* Belirli bir haber sitesinden otomatik olarak haber verilerini çekme.
* Çekilen verileri MongoDB'ye kaydetme.
* Çekilen metin verileri üzerinden en çok kullanılan kelimelerin frekans analizi.
* Çekilen verilerin istatistiksel analizini yapma ve kaydetme.
* Çekilen verileri gruplayarak raporlama.

## Kurulum
Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

## Projeyi klonlayın:
```
git clone https://github.com/hermannKonyar/HaberVeriCekmeVeAnalizi.git

```

## Gerekli kütüphaneleri yükleyin:

```
pip install -r requirements.txt

```

## Projeyi çalıştırmak için aşağıdaki komutu kullanın:

```

python app2.py

```

Bu komut, haber verilerini çeker, analiz eder ve MongoDB'ye kaydeder. Çıktıları logs/logs.log dosyasında ve word_frequency.png grafik dosyasında görebilirsiniz.

