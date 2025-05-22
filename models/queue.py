
import collections

class PassengerQueue:
    """Yolcuları FIFO (İlk Giren İlk Çıkar) prensibiyle yöneten kuyruk sınıfı."""

    def __init__(self):
        """Boş bir kuyruk (deque kullanarak) oluşturur."""
        self._items = collections.deque()
        print("Yolcu Kuyruğu başlatıldı.") # Başlangıç bilgisi

    def enqueue(self, passenger):
        """Kuyruğun sonuna bir yolcu ekler."""
        self._items.append(passenger)
        print(f"Kuyruğa Eklendi: {passenger}") # Loglama

    def dequeue(self):
        """Kuyruğun başından bir yolcu çıkarır ve döndürür. Kuyruk boşsa None döndürür."""
        if not self.is_empty():
            passenger = self._items.popleft()
            print(f"Kuyruktan Çıkarıldı: {passenger}") # Loglama
            return passenger
        print("Kuyruk boş, çıkarılacak yolcu yok.") # Hata/Durum mesajı
        return None

    def peek(self):
        """Kuyruğun başındaki yolcuyu çıkarmadan döndürür. Kuyruk boşsa None döndürür."""
        if not self.is_empty():
            return self._items[0]
        return None

    def is_empty(self):
        """Kuyruğun boş olup olmadığını kontrol eder."""
        return len(self._items) == 0

    def size(self):
        """Kuyruktaki yolcu sayısını döndürür."""
        return len(self._items)

    def __len__(self):
        """len() fonksiyonu ile kuyruk boyutunu almayı sağlar."""
        return self.size()

    def get_items(self):
        """GUI'de göstermek için kuyruktaki tüm öğelerin bir listesini döndürür."""
        return list(self._items)

    def __str__(self):
        """Kuyruğun string temsilini döndürür (GUI'de listelemek için faydalı olabilir)."""
        return " -> ".join(str(p) for p in self._items)