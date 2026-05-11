# =============================================================
# analyzer.py — Analiz ve Değerlendirme Modülü
# Bu dosya; toplanan ham verileri işleyerek ortalama hesaplar,
# eşik değerlerine göre sistemi değerlendirir ve rapor üretir.
# =============================================================


# ---------------------------------------------------------------
# Temel Sınıf: BaseAnalyzer
# Tüm analizör sınıflarının miras alacağı soyut temel sınıftır.
# ---------------------------------------------------------------
class BaseAnalyzer:
    def __init__(self, sensor_name: str):
        self._sensor_name = sensor_name  # Hangi sensörün verisi işleniyor
        self._average = None             # Hesaplanan ortalama (başta bilinmiyor)

    # Ortalama hesaplama: tüm alt sınıfların uygulaması zorunlu
    def analyze(self, readings: list):
        raise NotImplementedError("analyze() alt sınıfta tanımlanmalıdır.")

    # Hesaplanan ortalamayı dışarıya veren getter (property — kapsülleme)
    @property
    def average(self):
        return self._average

    # Sensörün adını döndüren getter
    @property
    def sensor_name(self):
        return self._sensor_name

    # Ölçüm listesinden sadece sayısal değerleri çıkarır
    def _extract_values(self, readings: list) -> list:
        return [r["value"] for r in readings]   # Her kayıttaki "value" anahtarı

    # Listedeki sayıların aritmetik ortalamasını hesaplar
    def _calc_mean(self, values: list) -> float:
        if not values:                           # Liste boşsa sıfır döndür
            return 0.0
        return round(sum(values) / len(values), 2)  # Topla, böl, 2 ondalığa yuvarla


# ---------------------------------------------------------------
# Alt Sınıf: FPSAnalyzer  (BaseAnalyzer'dan kalıtım alır)
# FPS verilerini analiz eder ve performans durumunu değerlendirir.
# ---------------------------------------------------------------
class FPSAnalyzer(BaseAnalyzer):
    GOOD_THRESHOLD = 60       # 60 FPS ve üzeri: iyi performans
    WARN_THRESHOLD = 30       # 30-59 FPS arası: uyarı seviyesi

    def __init__(self):
        super().__init__("FPS")

    def analyze(self, readings: list):
        values = self._extract_values(readings)   # Sayıları çıkar
        self._average = self._calc_mean(values)   # Ortalamayı hesapla

    def status(self) -> str:
        if self._average is None:
            return "Veri yok"
        if self._average >= self.GOOD_THRESHOLD:
            return "✅ İyi"
        elif self._average >= self.WARN_THRESHOLD:
            return "⚠️  Orta"
        else:
            return "❌ Düşük"


# ---------------------------------------------------------------
# Alt Sınıf: ThermalAnalyzer  (BaseAnalyzer'dan kalıtım alır)
# CPU veya GPU sıcaklık verilerini analiz eder.
# Hem CPU hem GPU için aynı sınıf kullanılır (yeniden kullanılabilirlik).
# ---------------------------------------------------------------
class ThermalAnalyzer(BaseAnalyzer):
    SAFE_THRESHOLD = 70.0     # 70°C altı: güvenli
    WARN_THRESHOLD = 85.0     # 70-85°C arası: uyarı

    def __init__(self, sensor_name: str):
        super().__init__(sensor_name)

    def analyze(self, readings: list):
        values = self._extract_values(readings)
        self._average = self._calc_mean(values)

    def status(self) -> str:
        if self._average is None:
            return "Veri yok"
        if self._average < self.SAFE_THRESHOLD:
            return "✅ Normal"
        elif self._average < self.WARN_THRESHOLD:
            return "⚠️  Sıcak"
        else:
            return "❌ Kritik"


# ---------------------------------------------------------------
# Bileşik Sınıf: ReportGenerator
# Tüm analizör sonuçlarını birleştirerek genel sistem skoru
# hesaplar ve kullanıcıya anlaşılır bir rapor sunar.
# ---------------------------------------------------------------
class ReportGenerator:
    def __init__(self):
        # Her veri tipi için uygun analizör nesnesi oluşturuluyor (Kompozisyon)
        self._analyzers = {
            "FPS":           FPSAnalyzer(),
            "CPU Sıcaklık":  ThermalAnalyzer("CPU Sıcaklık"),
            "GPU Sıcaklık":  ThermalAnalyzer("GPU Sıcaklık"),
        }

    # Tüm sensör verilerini ilgili analizörlere gönderir
    def run_analysis(self, all_readings: dict):
        for name, analyzer in self._analyzers.items():
            if name in all_readings:
                analyzer.analyze(all_readings[name])

    # Analiz sonuçlarını ekrana yazdırır
    def print_report(self):
        print("=" * 50)
        print("        SİSTEM PERFORMANS RAPORU")
        print("=" * 50)

        score_total = 0
        score_count = 0

        for name, analyzer in self._analyzers.items():
            avg = analyzer.average
            status = analyzer.status()
            unit = "FPS" if name == "FPS" else "°C"
            print(f"  {name:<15}: Ort. {avg:>6} {unit}  |  {status}")

            if "✅" in status:
                score_total += 100
            elif "⚠️" in status:
                score_total += 50
            else:
                score_total += 0
            score_count += 1

        overall = round(score_total / score_count) if score_count > 0 else 0
        print("-" * 50)
        print(f"  Genel Sistem Skoru  : %{overall}")
        print(self._overall_verdict(overall))
        print("=" * 50)

    # Genel skora göre toplu değerlendirme mesajı döndürür
    def _overall_verdict(self, score: int) -> str:
        if score >= 80:
            return "  Sonuç: Sisteminiz oyun için HAZIR. 🎮"
        elif score >= 50:
            return "  Sonuç: Sistem ORTA düzeyde. İyileştirme önerilir."
        else:
            return "  Sonuç: Sistem ZAYIF. Soğutma veya donanım kontrolü yapın!"
