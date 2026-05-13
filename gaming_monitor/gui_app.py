import customtkinter as ctk
import threading
import time
from monitor import GameMonitor
from analyzer import ReportGenerator

# Görünüm Ayarları
ctk.set_appearance_mode("Dark")  # Karanlık tema
ctk.set_default_color_theme("blue")  # Mavi butonlar

class ProPerformanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("PRO Game Performance Analyzer")
        self.geometry("900x600")

        # Modülleri Başlat (Senin OOP yapın)
        self.monitor = GameMonitor()
        self.reporter = ReportGenerator()

        # Arayüz Elemanlarını Oluştur
        self._create_widgets()

    def _create_widgets(self):
        # --- SOL PANEL (Kontroller) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="PERF-CHECK", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        self.duration_label = ctk.CTkLabel(self.sidebar, text="İzleme Süresi (sn):")
        self.duration_label.pack(pady=(20, 0))
        
        self.duration_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Örn: 5")
        self.duration_entry.insert(0, "5")
        self.duration_entry.pack(pady=10, padx=20)

        self.start_btn = ctk.CTkButton(self.sidebar, text="Analizi Başlat", command=self.start_analysis_thread, fg_color="#2ecc71", hover_color="#27ae60")
        self.start_btn.pack(pady=20, padx=20)

        # --- SAĞ PANEL (Sonuçlar) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Durum Göstergesi
        self.status_label = ctk.CTkLabel(self.main_frame, text="Sistem Analize Hazır", font=("Segoe UI", 16))
        self.status_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=10)

        # Rapor Metin Kutusu
        self.result_box = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13), corner_radius=10)
        self.result_box.pack(expand=True, fill="both", pady=10)

    def start_analysis_thread(self):
        """Arayüzün donmaması için analizi arka planda (thread) başlatır."""
        try:
            duration = int(self.duration_entry.get())
            self.start_btn.configure(state="disabled")
            self.result_box.delete("1.0", "end")
            self.status_label.configure(text="📊 Veriler Toplanıyor... Lütfen Bekleyin", text_color="#f1c40f")
            
            # Arka plan işini başlat
            threading.Thread(target=self.run_logic, args=(duration,), daemon=True).start()
        except ValueError:
            self.result_box.insert("end", "HATA: Lütfen geçerli bir saniye girin!")

    def run_logic(self, duration):
        """Senin monitor ve analyzer sınıflarını çalıştıran ana mantık."""
        # 1. Veri Topla
        self.progress_bar.start()
        self.monitor.collect(duration=duration)
        data = self.monitor.get_all_readings()
        self.progress_bar.stop()
        self.progress_bar.set(1)

        # 2. Analiz Et
        results = self.reporter.run_analysis(data)
        
        # 3. Arayüzü Güncelle (Main Thread'e dönerek)
        self.after(0, lambda: self.show_results(results))

    def show_results(self, results):
        """Sonuçları şık bir şekilde ekrana basar."""
        self.status_label.configure(text="✅ Analiz Tamamlandı!", text_color="#2ecc71")
        self.start_btn.configure(state="normal")
        
        # Rapor metnini oluştur
        report_text = f"--- PERFORMANS RAPORU ---\n"
        report_text += f"Genel Sistem Skoru: %{results['score']}\n"
        report_text += "="*30 + "\n\n"
        
        for sensor, info in results["details"].items():
            report_text += f"[{sensor}]\n"
            report_text += f"  Ortalama: {info['avg']:.2f}\n"
            report_text += f"  Durum: {info['status']}\n"
            report_text += "-"*20 + "\n"
        
        self.result_box.insert("end", report_text)

if __name__ == "__main__":
    app = ProPerformanceApp()
    app.mainloop()
