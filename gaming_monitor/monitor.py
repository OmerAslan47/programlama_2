# =============================================================
# monitor.py — Veri Toplama Modülü
# Bu dosya; FPS, CPU sıcaklığı ve GPU sıcaklığı verilerini
# gerçekçi biçimde simüle ederek toplayan sınıfları barındırır.
# Her ölçüm, bir öncekinin etrafında küçük adımlarla değişir.
# =============================================================

import random          # Küçük rastgele değişim miktarı üretmek için
import time            # Ölçümler arasına bekleme süresi eklemek için
from datetime import datetime  # Her ölçüme zaman damgası eklemek için


# ---------------------------------------------------------------
# Temel (Base) Sınıf: Sensor
# Tüm sensör sınıflarının türeyeceği soyut temel sınıftır.
# Kapsülleme: _readings listesi dışarıdan doğrudan erişilemez (_).
# ---------------------------------------------------------------
class Sensor:
    def __init__(self, name: str):
        self._name = name          # Sensörün adı (ör. "CPU Sıcaklık")
        self._readings = []        # Toplanan ölçümleri tutan liste (kapsüllendi)

    # Her alt sınıfın kendi okuma mantığını uygulaması gerekir
    def read(self):
        raise NotImplementedError("read() metodu alt sınıfta tanımlanmalıdır.")

    # Dışarıdan ölçüm listesine erişim için güvenli getter (property)
    @property
    def readings(self):
        return self._readings      # Listeyi dışarıya salt okunur verir

    # Sensörün adını döndüren getter
    @property
    def name(self):
        return self._name

    # Birikmiş ölçümleri sıfırlar
    def reset(self):
        self._readings = []        # Listeyi boşalt

    # Ölçüm sayısını döndürür
    def count(self):
        return len(self._readings)

    # -------------------------------------------------------
    # Yardımcı metot: _smooth_value
    # Bir önceki ölçüm varsa etrafında küçük adım atar,
    # yoksa aralık ortasından başlar. Tüm alt sınıflar kullanır.
    # min_val      : değerin çıkabileceği alt sınır
    # max_val      : değerin çıkabileceği üst sınır
    # delta_range  : tek adımda maksimum değişim miktarı
    # is_int       : True ise sonucu tam sayıya yuvarlar (FPS için)
    # -------------------------------------------------------
    def _smooth_value(self, min_val, max_val, delta_range, is_int=False):
        if self._readings:
            last = self._readings[-1]["value"]              # Son ölçümü al
            delta = random.uniform(-delta_range, delta_range)  # Küçük rastgele adım
            new_val = last + delta                          # Yeni değer = son + adım
            new_val = max(min_val, min(max_val, new_val))   # Sınırlar içinde tut
        else:
            new_val = (min_val + max_val) / 2  # İlk ölçüm: aralığın ortasından başla

        if is_int:
            return int(round(new_val))   # Tam sayıya yuvarla (FPS için)
        return round(new_val, 1)         # 1 ondalık basamak (sıcaklık için)


# ---------------------------------------------------------------
# Alt Sınıf: FPSSensor  (Sensor sınıfından kalıtım alır)
# Oyun sırasındaki FPS değerlerini gerçekçi şekilde simüle eder.
# Her adımda en fazla ±5 FPS değişir.
# ---------------------------------------------------------------
class FPSSensor(Sensor):
    def __init__(self, min_fps: int = 30, max_fps: int = 144):
        super().__init__("FPS")    # Üst sınıfın __init__'ini çağır
        self._min_fps = min_fps    # Simülasyonun alt sınırı
        self._max_fps = max_fps    # Simülasyonun üst sınırı

    def read(self):
        # Bir önceki FPS değerine göre ±5 aralığında gerçekçi değişim
        value = self._smooth_value(self._min_fps, self._max_fps,
                                   delta_range=5, is_int=True)
        timestamp = datetime.now().strftime("%H:%M:%S")  # Anlık saati al
        record = {"time": timestamp, "value": value}     # Sözlük olarak sakla
        self._readings.append(record)                    # Listeye ekle
        return record


# ---------------------------------------------------------------
# Alt Sınıf: CPUSensor  (Sensor sınıfından kalıtım alır)
# CPU sıcaklık değerlerini gerçekçi şekilde simüle eder.
# Her adımda en fazla ±1.5°C değişir.
# ---------------------------------------------------------------
class CPUSensor(Sensor):
    def __init__(self, min_temp: float = 45.0, max_temp: float = 95.0):
        super().__init__("CPU Sıcaklık")
        self._min_temp = min_temp
        self._max_temp = max_temp

    def read(self):
        # Bir önceki sıcaklığa göre ±1.5°C aralığında gerçekçi değişim
        value = self._smooth_value(self._min_temp, self._max_temp,
                                   delta_range=1.5)
        timestamp = datetime.now().strftime("%H:%M:%S")
        record = {"time": timestamp, "value": value}
        self._readings.append(record)
        return record


# ---------------------------------------------------------------
# Alt Sınıf: GPUSensor  (Sensor sınıfından kalıtım alır)
# GPU sıcaklık değerlerini gerçekçi şekilde simüle eder.
# Her adımda en fazla ±1.5°C değişir.
# ---------------------------------------------------------------
class GPUSensor(Sensor):
    def __init__(self, min_temp: float = 40.0, max_temp: float = 90.0):
        super().__init__("GPU Sıcaklık")
        self._min_temp = min_temp
        self._max_temp = max_temp

    def read(self):
        # Bir önceki sıcaklığa göre ±1.5°C aralığında gerçekçi değişim
        value = self._smooth_value(self._min_temp, self._max_temp,
                                   delta_range=1.5)
        timestamp = datetime.now().strftime("%H:%M:%S")
        record = {"time": timestamp, "value": value}
        self._readings.append(record)
        return record


# ---------------------------------------------------------------
# Bileşik Sınıf: GameMonitor
# Tüm sensörleri bir arada yöneten ana izleme sınıfıdır.
# ---------------------------------------------------------------
class GameMonitor:
    def __init__(self, interval: float = 1.0):
        # Her sensörden bir nesne oluştur ve listeye ekle (Kompozisyon)
        self._sensors = [
            FPSSensor(),
            CPUSensor(),
            GPUSensor(),
        ]
        self._interval = interval  # Ölçümler arası bekleme süresi (saniye)

    # Belirtilen süre boyunca tüm sensörlerden veri toplar
    def collect(self, duration: int = 10):
        print(f"\n[*] İzleme başlatıldı — {duration} saniye boyunca veri toplanacak...\n")
        start = time.time()

        while time.time() - start < duration:
            for sensor in self._sensors:
                record = sensor.read()
                print(f"  [{record['time']}] {sensor.name:>15}: {record['value']}")
            print("  " + "-" * 40)
            time.sleep(self._interval)

        print("\n[✓] Veri toplama tamamlandı.\n")

    # Tüm sensörlerin topladığı ham ölçüm listelerini sözlük olarak döndürür
    def get_all_readings(self) -> dict:
        return {sensor.name: sensor.readings for sensor in self._sensors}

    # Tüm sensörleri sıfırlar (yeni oturum için)
    def reset_all(self):
        for sensor in self._sensors:
            sensor.reset()
