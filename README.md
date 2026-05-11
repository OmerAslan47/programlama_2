# 🎮 Oyun Performans İzleme Aracı
> Kastamonu Üniversitesi Tosya MYO — Programlama II Dönem Sonu Projesi

## 📌 Proje Açıklaması

Bu uygulama, oyun oynarken sistem performansını **(FPS, CPU sıcaklığı, GPU sıcaklığı)** simüle ederek izleyen, toplanan verilerin ortalamasını hesaplayan ve sistemi değerlendiren bir komut satırı (CLI) aracıdır.

Sensörler **gerçekçi bir davranış** sergilemektedir: her ölçüm, bir öncekinin etrafında küçük adımlarla değişir. Bu sayede ani ve gerçek dışı sıçramalar yerine doğal bir veri akışı elde edilir.

Proje tamamen **Python** diliyle, **Nesne Tabanlı Programlama (OOP)** prensiplerine ve modüler yapıya uygun şekilde geliştirilmiştir.

---

## 🗂️ Proje Dosya Yapısı

```
gaming_monitor/
│
├── main.py        # Ana çalışma dosyası — menü ve uygulama akışı
├── monitor.py     # Sensör sınıfları — FPS, CPU, GPU veri toplama
└── analyzer.py    # Analizör sınıfları — ortalama hesaplama ve rapor üretme
```

---

## ⚙️ Kurulum ve Çalıştırma

Python 3.8 veya üzeri yeterlidir. Harici kütüphane gerekmez.

```bash
# Projeyi klonla
git clone https://github.com/KULLANICI_ADINIZ/gaming-monitor.git
cd gaming-monitor

# Programı başlat
python main.py
```

---

## 🧱 OOP Mimarisi

| Sınıf | Dosya | Açıklama |
|---|---|---|
| `Sensor` | monitor.py | Tüm sensörlerin temel (base) sınıfı; `_smooth_value()` yardımcı metodu burada |
| `FPSSensor` | monitor.py | `Sensor`'dan kalıtım — ±5 adımlı gerçekçi FPS simülasyonu |
| `CPUSensor` | monitor.py | `Sensor`'dan kalıtım — ±1.5°C adımlı CPU sıcaklık simülasyonu |
| `GPUSensor` | monitor.py | `Sensor`'dan kalıtım — ±1.5°C adımlı GPU sıcaklık simülasyonu |
| `GameMonitor` | monitor.py | Tüm sensörleri yöneten bileşik sınıf |
| `BaseAnalyzer` | analyzer.py | Tüm analizörlerin temel sınıfı |
| `FPSAnalyzer` | analyzer.py | `BaseAnalyzer`'dan kalıtım — FPS analizi ve durum değerlendirmesi |
| `ThermalAnalyzer` | analyzer.py | `BaseAnalyzer`'dan kalıtım — CPU ve GPU sıcaklık analizi |
| `ReportGenerator` | analyzer.py | Tüm analizörleri birleştirip rapor üretir |
| `App` | main.py | Uygulama akışını yöneten ana sınıf |

---

## 🎯 Gerçekçi Sensör Simülasyonu

Projenin öne çıkan teknik özelliği, sensörlerin **kademeli değişim (smooth simulation)** modelidir:

- **İlk ölçüm:** Aralığın orta noktasından başlar (ör. CPU için 70°C)
- **Sonraki ölçümler:** Her ölçüm, bir önceki değerin ±`delta_range` kadar etrafında rastgele değişir
- **Sınır kontrolü:** `max()` ve `min()` ile değer hiçbir zaman belirlenen aralığın dışına çıkmaz

```
CPU:  70.0 → 71.2 → 70.6 → 72.0 → 71.5  ✅ Gerçekçi
CPU:  70.0 → 48.3 → 91.7 → 55.2 → 88.4  ❌ Eski rastgele yöntem
```

---

## 🖥️ Örnek Çıktı

```
==================================================
   🎮  OYUN PERFORMANS İZLEME ARACI  🎮
==================================================

[*] İzleme başlatıldı — 5 saniye boyunca veri toplanacak...

  [14:22:01]             FPS: 87
  [14:22:01]    CPU Sıcaklık: 70.0
  [14:22:01]    GPU Sıcaklık: 65.0
  ----------------------------------------
  [14:22:02]             FPS: 89
  [14:22:02]    CPU Sıcaklık: 71.3
  [14:22:02]    GPU Sıcaklık: 64.2
  ----------------------------------------

==================================================
        SİSTEM PERFORMANS RAPORU
==================================================
  FPS            : Ort.  88.20 FPS  |  ✅ İyi
  CPU Sıcaklık   : Ort.  70.80 °C   |  ⚠️  Sıcak
  GPU Sıcaklık   : Ort.  64.50 °C   |  ✅ Normal
--------------------------------------------------
  Genel Sistem Skoru  : %83
  Sonuç: Sisteminiz oyun için HAZIR. 🎮
==================================================
```

---

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x** — Ana programlama dili
- `random` — Kademeli sensör değişimi için küçük rastgele adım üretimi
- `time` — Ölçüm aralığı kontrolü
- `datetime` — Zaman damgası üretimi

---

## 👤 Geliştirici

| Ad Soyad | Okul No |
|---|---|
| [Adınız Soyadınız] | [Okul Numaranız] |

---

## 📄 Lisans

Bu proje eğitim amaçlıdır.
