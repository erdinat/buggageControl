import time # İsteğe bağlı olarak adımlar arasına bekleme eklemek için
from models.queue import PassengerQueue
from models.stack import BaggageStack
from models.linkedlist import LinkedList
from models.yolcu import Passenger
import tkinter as tk
from gui import AppGUIManager
from utils.olasilik import (
    generate_random_baggage,
    esya_tehlikeli_mi,
    load_blacklist_from_file,
    DANGEROUS_ITEMS # Tehlikeli eşya kontrolü için gerekebilir
)

class SimulationController:
    """
    Bagaj Güvenlik Simülasyonunun ana kontrol sınıfı.
    Tüm veri yapılarını, istatistikleri ve işlem adımlarını yönetir.
    """
    def __init__(self):
        print("--- Simülasyon Başlatılıyor ---")
        # 1. Veri Yapılarını Başlatma
        self.passenger_queue = PassengerQueue()
        self.baggage_stack = BaggageStack()
        self.blacklist = LinkedList()

        # Yolcu sayacını sıfırla
        Passenger._id_counter = 1

        # 2. İstatistikleri Sıfırlama
        self.total_passengers_processed = 0
        self.alarms_triggered = 0 # Tehlikeli eşya tespit sayısı
        self.blacklisted_caught = 0
        self.clean_passes = 0
        self.bags_sent_to_stack = 0 # Stack'e gönderilen toplam bagaj sayısı

        # 3. Başlangıç Verilerini Yükleme (Kara Liste)
        self._load_initial_data()

        # GUI Referansları (Daha sonra gui.py'den atanacak)
        self.gui_manager = None # GUI güncelleme fonksiyonlarını çağırmak için

        print("--- Simülasyon Hazır ---")

    def set_gui_manager(self, gui_manager):
        """GUI Yönetici nesnesini (güncelleme fonksiyonlarını içeren) ayarlar."""
        self.gui_manager = gui_manager
        print("GUI Yöneticisi ayarlandı.")

    def _load_initial_data(self):
        """Başlangıç verilerini (örn: kara liste) yükler."""
        print("Başlangıç verileri yükleniyor...")
        blacklist_ids = load_blacklist_from_file() # utils'den fonksiyonu çağır
        for passenger_id in blacklist_ids:
            self.blacklist.append(passenger_id)
        # self.blacklist.display() # Gerekirse kara liste içeriğini kontrol et

    # --- A. Yolcu Oluştur ve Kuyruğa Ekle ---
    def yolcu_olustur_ve_ekle(self):
        """Yeni bir yolcu oluşturur, rastgele bagaj atar ve kuyruğa ekler."""
        print("\n--- Yeni Yolcu Oluşturuluyor ---")
        random_baggage = generate_random_baggage()
        new_passenger = Passenger(baggage=random_baggage)
        self.passenger_queue.enqueue(new_passenger)

        # GUI Güncelleme (Eğer GUI bağlıysa)
        if self.gui_manager:
            self.gui_manager.update_queue_panel()
            self.gui_manager.log_message(f"Yeni yolcu eklendi: {new_passenger}")

        return new_passenger

    # --- B. Simülasyonu Başlat ve Kuyruktan Yolcu Al ---
    # Bu fonksiyon tek bir adımı işler. Tam simülasyon için döngüye alınabilir.
    def simulasyon_adimini_calistir(self):
        """Simülasyonun bir adımını çalıştırır: Kuyruktan yolcu alır ve işler."""
        print("\n--- Simülasyon Adımı Başlatılıyor ---")
        if self.passenger_queue.is_empty():
            message = "Kuyrukta bekleyen yolcu kalmadı."
            print(message)
            if self.gui_manager: self.gui_manager.log_message(message)
            return None # İşlenecek yolcu yok

        # Kuyruktan yolcu al
        current_passenger = self.passenger_queue.dequeue()
        self.total_passengers_processed += 1
        passenger_id = current_passenger.passenger_id
        message = f"İşleniyor: {passenger_id} (Bagaj: {len(current_passenger.baggage)} eşya)"
        print(message)
        if self.gui_manager:
             self.gui_manager.log_message(message)
             self.gui_manager.update_queue_panel() # Kuyruk değiştiği için güncelle

        # --- C. Kara Liste Kontrolü ---
        is_blacklisted = self.kara_listede_mi(passenger_id)

        if is_blacklisted:
            current_passenger.set_risky(True)
            self.blacklisted_caught += 1
            message = f"DIKKAT: {passenger_id} kara listede! Bagaj doğrudan yığına gönderiliyor."
            print(message)
            if self.gui_manager:
                self.gui_manager.log_message(message, level="warning")
                self.gui_manager.update_linked_list_panel(highlight_id=passenger_id) # GUI'de görselleştir

            # Bagajı doğrudan Stack'e gönder
            self.bags_sent_to_stack += 1
            for item in current_passenger.baggage:
                self.baggage_stack.push(item) # Eşyaları stack'e ekle
            if self.gui_manager: self.gui_manager.update_stack_panel() # Stack değişti
            # İsteğe bağlı: Stack taramasını hemen başlatabiliriz
            # self.stack_taramasi()

        else:
            # --- D. Bagajı Tara (Tehlikeli mi?) ---
            passed_cleanly = self.bagaj_tarama(current_passenger)

            if passed_cleanly:
                self.clean_passes += 1
                message = f"{passenger_id} bagajı temiz. Geçiş onaylandı."
                print(message)
                if self.gui_manager: self.gui_manager.log_message(message, level="info")
            # else: Bagaj stack'e gitti, mesaj bagaj_tarama içinde verildi.

        # İşlem tamamlandı logu
        final_status = "Temiz Geçti" if not is_blacklisted and 'passed_cleanly' in locals() and passed_cleanly else ("Kara Listede Yakalandı" if is_blacklisted else "Bagaj İncelemede")
        print(f"İşlem Tamamlandı: {passenger_id} - Durum: {final_status}")
        if self.gui_manager: self.gui_manager.log_message(f"İşlem Tamamlandı: {passenger_id} - Durum: {final_status}")


        # İsteğe bağlı bekleme (Simülasyonu yavaşlatmak için)
        # time.sleep(0.5)

        return current_passenger # İşlenen yolcuyu döndür


    # --- C. Kara Liste Kontrolü (Yardımcı Fonksiyon) ---
    def kara_listede_mi(self, passenger_id):
        """Verilen yolcu ID'sinin kara listede (LinkedList) olup olmadığını kontrol eder."""
        found = self.blacklist.search(passenger_id)
        return found

    # --- D. Bagajı Stack'e Aktar (Tehlikeli mi?) ---
    def bagaj_tarama(self, passenger):
        """Yolcunun bagajındaki eşyaları tarar. Tehlikeli bulursa yığına gönderir."""
        print(f"Bagaj Taranıyor: {passenger.passenger_id}")
        
        # Baggage sınıfının has_dangerous_items metodunu kullan
        if passenger.baggage.has_dangerous_items(DANGEROUS_ITEMS):
            self.alarms_triggered += 1
            message = f"ALARM: {passenger.passenger_id} bagajında tehlikeli eşya bulundu: {passenger.baggage.suspicious_items}! Bagaj yığına gönderiliyor."
            print(message)
            if self.gui_manager: 
                self.gui_manager.log_message(message, level="danger")

            self.bags_sent_to_stack += 1
            # Tüm bagajı yığına aktar
            for item in passenger.baggage.get_items():
                self.baggage_stack.push(item)

            if self.gui_manager:
                self.gui_manager.update_stack_panel(highlight=True)
            return False
        else:
            return True

    # --- E. Stack İncelemesi (Görsel Tarama) ---
    def stack_taramasi(self):
        """Yığındaki (stack) eşyaları tek tek çıkarır ve loglar."""
        print("\n--- Yığın (Stack) İnceleniyor ---")
        if self.baggage_stack.is_empty():
            message="Yığında incelenecek eşya yok."
            print(message)
            if self.gui_manager: self.gui_manager.log_message(message)
            return

        while not self.baggage_stack.is_empty():
            item = self.baggage_stack.pop()
            # Sadece tehlikeli eşyaları göster
            if esya_tehlikeli_mi(item):
                message = f"Yığından çıkarıldı ve incelendi: {item} (Tehlikeli!)"
                print(message)
                if self.gui_manager:
                    self.gui_manager.log_message(message)
                    self.gui_manager.update_stack_panel() # Her çıkarma sonrası stack panelini güncelle
        print("--- Yığın İncelemesi Tamamlandı ---")
        if self.gui_manager: self.gui_manager.log_message("Yığın incelemesi tamamlandı.")


    # --- F. Gün Sonu Raporu ---
    def rapor_goster(self):
        """Simülasyonun sonunda istatistiksel bir rapor oluşturur ve yazdırır."""
        print("\n--- GÜN SONU RAPORU ---")
        print(f"Toplam İşlenen Yolcu Sayısı : {self.total_passengers_processed}")
        print(f"Temiz Geçiş Yapan Yolcu     : {self.clean_passes}")
        print(f"Kara Listede Yakalanan      : {self.blacklisted_caught}")
        print(f"Bagajı İncelenen (Stack'e)  : {self.bags_sent_to_stack}")
        print(f"Tespit Edilen Alarm Sayısı  : {self.alarms_triggered}") # Tehlikeli eşya kaynaklı
        print("--------------------------")

        # Raporu GUI'de gösterme veya dosyaya yazma kısmı eklenebilir
        report_text = f"""--- GÜN SONU RAPORU ---
Toplam İşlenen Yolcu Sayısı : {self.total_passengers_processed}
Temiz Geçiş Yapan Yolcu     : {self.clean_passes}
Kara Listede Yakalanan      : {self.blacklisted_caught}
Bagajı İncelenen (Stack'e)  : {self.bags_sent_to_stack}
Tespit Edilen Alarm Sayısı  : {self.alarms_triggered}
--------------------------"""
        if self.gui_manager:
            self.gui_manager.show_report(report_text)

        # CSV olarak dışa aktarma
        import csv
        try:
            with open('rapor.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Metric', 'Value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Metric': 'Toplam İşlenen Yolcu', 'Value': self.total_passengers_processed})
                writer.writerow({'Metric': 'Temiz Geçiş', 'Value': self.clean_passes})
                writer.writerow({'Metric': 'Kara Liste Yakalanan', 'Value': self.blacklisted_caught})
                writer.writerow({'Metric': 'Stack\'e Gönderilen Bagaj', 'Value': self.bags_sent_to_stack})
                writer.writerow({'Metric': 'Alarm Sayısı', 'Value': self.alarms_triggered})
            print("Rapor 'rapor.csv' dosyasına yazıldı.")
            if self.gui_manager:
                self.gui_manager.log_message("Rapor 'rapor.csv' dosyasına yazıldı.", "success")
        except Exception as e:
            print(f"Rapor CSV'ye yazılamadı: {e}")
            if self.gui_manager:
                self.gui_manager.log_message(f"Rapor CSV'ye yazılamadı: {e}", "warning")


# === Basit Test Çalıştırması (GUI olmadan) ===
if __name__ == "__main__":
    # 1. Tkinter Ana Penceresini Oluştur
    root = tk.Tk()

    # 2. Simülasyon kontrolcüsünü oluştur
    controller = SimulationController()

    # 3. GUI Yöneticisini Oluştur (Bu, controller'a GUI referansını da verir)
    app_gui = AppGUIManager(root, controller)

    # 4. Tkinter Olay Döngüsünü Başlat (Pencereyi açık tutar ve olayları dinler)
    root.mainloop()