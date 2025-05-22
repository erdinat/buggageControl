import tkinter as tk
from tkinter import ttk # Daha modern görünümlü widget'lar için
from tkinter import scrolledtext # Kaydırılabilir metin alanı için
from tkinter import messagebox # Rapor gösterme gibi durumlar için
from models.queue import PassengerQueue  # Eksik import eklendi
from utils.olasilik import esya_tehlikeli_mi  # Tehlikeli eşya kontrolü için

class AppGUIManager:
    """
    Tkinter kullanarak Bagaj Güvenlik Simülatörü için Grafiksel Kullanıcı Arayüzünü yönetir.
    """
    def __init__(self, root, controller):
        """
        Ana pencereyi (root) ve simülasyon kontrolcüsünü (controller) alır,
        arayüzü oluşturur ve controller'a GUI referansını iletir.
        """
        self.root = root
        self.controller = controller
        self.root.title("Bagaj Güvenlik Simülatörü")
        # Pencere boyutunu ayarla (isteğe bağlı)
        self.root.geometry("1000x600")

        # Ana çerçeveyi oluştur
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Widget'ları oluşturacak metodu çağır
        self._create_widgets(main_frame)

        # Controller'a bu GUI yöneticisi nesnesini bildir
        self.controller.set_gui_manager(self)

        # Başlangıç durumunu yükle (örn: kara liste)
        self.update_linked_list_panel()
        self.log_message("Arayüz başarıyla yüklendi.", "info")

    def _create_widgets(self, parent_frame):
        """Arayüzdeki tüm panelleri ve kontrol widget'larını oluşturur."""

        # Grid konfigürasyonu (3 ana sütun)
        parent_frame.columnconfigure(0, weight=1) # Kontrol Paneli
        parent_frame.columnconfigure(1, weight=2) # Orta Paneller (Queue, Stack, Blacklist)
        parent_frame.columnconfigure(2, weight=3) # Log Paneli
        parent_frame.rowconfigure(0, weight=1)

        # --- Sol Sütun: Kontrol Paneli ---
        control_frame = ttk.LabelFrame(parent_frame, text="Kontrol Paneli", padding="10")
        control_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))

        # Butonlar
        btn_add_passenger = ttk.Button(control_frame, text="Yeni Yolcu Ekle", command=self.controller.yolcu_olustur_ve_ekle)
        btn_add_passenger.pack(pady=5, fill=tk.X)

        btn_process_step = ttk.Button(control_frame, text="Simülasyon Adımı Çalıştır", command=self.controller.simulasyon_adimini_calistir)
        btn_process_step.pack(pady=5, fill=tk.X)

        btn_process_all = ttk.Button(control_frame, text="Tüm Kuyruğu İşle", command=self._run_full_simulation)
        btn_process_all.pack(pady=5, fill=tk.X)

        btn_inspect_stack = ttk.Button(control_frame, text="Yığını (Stack) Tara", command=self.controller.stack_taramasi)
        btn_inspect_stack.pack(pady=10, fill=tk.X)

        btn_show_report = ttk.Button(control_frame, text="Gün Sonu Raporu Göster", command=self.controller.rapor_goster)
        btn_show_report.pack(pady=10, fill=tk.X)

        # Hazır veri yükleme butonu
        btn_load_data = ttk.Button(control_frame, text="Hazır Veri Yükle (30 Yolcu)", command=self._load_preset_data)
        btn_load_data.pack(pady=5, fill=tk.X)


        # --- Orta Sütun: Queue, Stack, Blacklist ---
        middle_frame = ttk.Frame(parent_frame, padding="5")
        middle_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        middle_frame.rowconfigure(0, weight=1) # Queue
        middle_frame.rowconfigure(1, weight=1) # Stack
        middle_frame.rowconfigure(2, weight=1) # Blacklist
        middle_frame.columnconfigure(0, weight=1)

        # Queue Panel
        queue_frame = ttk.LabelFrame(middle_frame, text="Yolcu Kuyruğu (Queue - FIFO)", padding="5")
        queue_frame.grid(row=0, column=0, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        queue_frame.rowconfigure(0, weight=1)
        queue_frame.columnconfigure(0, weight=1)
        self.queue_listbox = tk.Listbox(queue_frame, height=8)
        self.queue_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        # Scrollbar ekleme (isteğe bağlı, çok uzarsa diye)
        # queue_scrollbar = ttk.Scrollbar(queue_frame, orient=tk.VERTICAL, command=self.queue_listbox.yview)
        # self.queue_listbox.configure(yscrollcommand=queue_scrollbar.set)
        # queue_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))


        # Stack Panel
        self.stack_frame = ttk.LabelFrame(middle_frame, text="Şüpheli Bagaj Yığını (Stack - LIFO)", padding="5") # LabelFrame'i sakla
        self.stack_frame.grid(row=1, column=0, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.stack_frame.rowconfigure(0, weight=1)
        self.stack_frame.columnconfigure(0, weight=1)
        self.stack_listbox = tk.Listbox(self.stack_frame, height=8)
        self.stack_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        # Başlangıç rengi
        self.stack_listbox.configure(bg="white")


        # Linked List (Blacklist) Panel
        blacklist_frame = ttk.LabelFrame(middle_frame, text="Kara Liste (Linked List)", padding="5")
        blacklist_frame.grid(row=2, column=0, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        blacklist_frame.rowconfigure(0, weight=1)
        blacklist_frame.columnconfigure(0, weight=1)
        self.blacklist_listbox = tk.Listbox(blacklist_frame, height=5)
        self.blacklist_listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))


        # --- Sağ Sütun: Log Paneli ---
        log_frame = ttk.LabelFrame(parent_frame, text="Olay Kayıtları (Log)", padding="5")
        log_frame.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=25, width=50)
        self.log_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.log_text.configure(state='disabled') # Başlangıçta düzenlemeyi engelle

        # Log seviyeleri için renk etiketleri (tags) tanımla
        self.log_text.tag_config('info', foreground='black')
        self.log_text.tag_config('warning', foreground='orange', font=('TkDefaultFont', 9, 'bold'))
        self.log_text.tag_config('danger', foreground='red', font=('TkDefaultFont', 9, 'bold'))
        self.log_text.tag_config('success', foreground='green')


    # --- GUI Güncelleme Metodları ---

    def update_queue_panel(self):
        """Kuyruk panelindeki listbox'ı günceller."""
        self.queue_listbox.delete(0, tk.END) # Önceki içeriği temizle
        passengers = self.controller.passenger_queue.get_items()
        for passenger in passengers:
            # Yolcunun string temsilini (__str__) kullan
            self.queue_listbox.insert(tk.END, str(passenger))

    def update_stack_panel(self, highlight=False):
        """Yığın panelindeki listbox'ı günceller ve isteğe bağlı olarak vurgular."""
        self.stack_listbox.delete(0, tk.END)
        # Sadece tehlikeli eşyaları göster
        items = self.controller.baggage_stack.get_items()
        dangerous_items = [item for item in items if esya_tehlikeli_mi(item)]
        # LIFO göstermek için ters sırada ekleyelim (Tepedeki en üstte)
        for item in reversed(dangerous_items):
            self.stack_listbox.insert(tk.END, item)

        # Vurgulama (Alarm durumu)
        if highlight:
            self.stack_listbox.configure(bg="salmon") # Kırmızımsı bir renk
            self.stack_frame.configure(relief=tk.SOLID, borderwidth=2) # Çerçeveyi belirginleştir
        else:
            self.stack_listbox.configure(bg="white") # Normal renk
            self.stack_frame.configure(relief=tk.GROOVE, borderwidth=1) # Normal çerçeve

    def update_linked_list_panel(self, highlight_id=None):
        """Kara liste panelindeki listbox'ı günceller ve eşleşen ID'yi vurgular."""
        self.blacklist_listbox.delete(0, tk.END)
        items = self.controller.blacklist.get_items()
        for idx, item_id in enumerate(items):
            self.blacklist_listbox.insert(tk.END, item_id)
            if item_id == highlight_id:
                self.blacklist_listbox.itemconfig(idx, {'bg':'yellow', 'fg':'black'}) # Vurgulama
            else:
                 self.blacklist_listbox.itemconfig(idx, {'bg':'white', 'fg':'black'}) # Vurgu yoksa normal

    def log_message(self, message, level='info'):
        """Log paneline belirli bir seviyede mesaj ekler."""
        self.log_text.configure(state='normal') # Yazmak için aktif et
        self.log_text.insert(tk.END, message + "\n", level) # Mesajı ve etiketi ekle
        self.log_text.configure(state='disabled') # Tekrar düzenlemeyi engelle
        self.log_text.see(tk.END) # En sona kaydır

    def show_report(self, report_text):
        """Raporu ayrı bir pencerede veya mesaj kutusunda gösterir."""
        messagebox.showinfo("Gün Sonu Raporu", report_text)

    # --- GUI Yardımcı Metodları ---

    def _run_full_simulation(self):
        """Kuyruktaki tüm yolcuları işleyen simülasyonu çalıştırır."""
        self.log_message("--- Tam Simülasyon Başlatıldı ---", "info")
        # Butonu geçici olarak devre dışı bırakabiliriz
        # (Eğer çok uzun sürüyorsa veya tekrar tıklanmasını istemiyorsak)
        # self.control_frame.children['!button3'].config(state="disabled")

        while not self.controller.passenger_queue.is_empty():
            self.controller.simulasyon_adimini_calistir()
            self.root.update() # Arayüzün her adımda güncellenmesini sağla
            # time.sleep(0.1) # Adımları yavaşlatmak için (isteğe bağlı)

        self.log_message("--- Tam Simülasyon Tamamlandı ---", "success")
        # Butonu tekrar aktif et
        # self.control_frame.children['!button3'].config(state="normal")

    def _load_preset_data(self, count=30):
        """Hazır veri (belirtilen sayıda yolcu) yükler."""
        self.log_message(f"{count} adet hazır yolcu yükleniyor...", "info")
        # Mevcut kuyruğu temizle
        self.controller.passenger_queue = PassengerQueue()
        self.update_queue_panel()
        
        # Yeni yolcuları ekle
        for _ in range(count):
            self.controller.yolcu_olustur_ve_ekle()
        self.log_message(f"{count} yolcu başarıyla eklendi.", "success")