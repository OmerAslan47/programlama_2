# =============================================================
# main.py — Ana Çalışma Dosyası
# Programın giriş noktasıdır. Kullanıcı arayüzü burada yönetilir.
# monitor.py ve analyzer.py modülleri buraya import edilir.
# =============================================================

from monitor import GameMonitor          # Veri toplama sınıfını içe aktar
from analyzer import ReportGenerator     # Rapor üretme sınıfını içe aktar


# ---------------------------------------------------------------
# Sınıf: App
# Uygulamanın tüm akışını (menü, izleme, analiz) yöneten sınıf.
# ---------------------------------------------------------------
class App:
    def __init__(self):
        self._monitor = GameMonitor(interval=1.0)   # Her 1 saniyede bir ölçüm
        self._reporter = ReportGenerator()           # Rapor üretici

    # Uygulamayı başlatan ana metot
    def run(self):
        self._print_banner()
        while True:
            choice = self._show_menu()
            if choice == "1":
                self._start_session()
            elif choice == "2":
                self._show_report()
            elif choice == "3":
                self._reset()
            elif choice == "0":
                print("\n[*] Çıkılıyor... Güle güle!\n")
                break
            else:
                print("[!] Geçersiz seçim. Lütfen tekrar deneyin.")

    # ASCII başlık ekranı
    def _print_banner(self):
        print("=" * 50)
        print("   🎮  OYUN PERFORMANS İZLEME ARACI  🎮")
        print("   Programlama II — Dönem Sonu Projesi")
        print("=" * 50)

    # Menüyü ekrana yazdırır ve kullanıcıdan seçim alır
    def _show_menu(self) -> str:
        print("\n--- MENÜ ---")
        print("  [1] Yeni İzleme Oturumu Başlat")
        print("  [2] Son Oturum Raporunu Göster")
        print("  [3] Verileri Sıfırla")
        print("  [0] Çıkış")
        choice = input("\nSeçiminiz: ").strip()
        return choice

    # Kullanıcıdan süre alır, izlemeyi başlatır ve raporu hazırlar
    def _start_session(self):
        try:
            duration = int(input("İzleme süresi (saniye, varsayılan 10): ").strip() or "10")
        except ValueError:
            duration = 10
            print("[!] Geçersiz giriş, 10 saniye kullanılıyor.")

        self._monitor.reset_all()          # Önceki oturumun verilerini temizle
        self._monitor.collect(duration)    # Veri toplamayı başlat

        readings = self._monitor.get_all_readings()
        self._reporter.run_analysis(readings)  # Analizi çalıştır

        print("[✓] Analiz hazır. 'Raporu Göster' seçeneği ile sonuçlara bakabilirsiniz.")

    # Son analiz raporunu ekrana basar
    def _show_report(self):
        self._reporter.print_report()

    # Monitörü sıfırlar
    def _reset(self):
        self._monitor.reset_all()
        print("[✓] Veriler sıfırlandı.")


# ---------------------------------------------------------------
# Program Giriş Noktası
# Bu blok yalnızca dosya doğrudan çalıştırıldığında tetiklenir.
# ---------------------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.run()
