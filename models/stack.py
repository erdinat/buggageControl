
class BaggageStack:
    """Şüpheli bagajdaki eşyaları LIFO (Son Giren İlk Çıkar) prensibiyle yöneten yığın sınıfı."""

    def __init__(self):
        """Boş bir yığın (liste kullanarak) oluşturur."""
        self._items = []
        print("Bagaj Yığını başlatıldı.") # Başlangıç bilgisi


    def push(self, item):
        """Yığının tepesine bir eşya ekler."""
        self._items.append(item)
        print(f"Yığına Eklendi (Push): {item}") # Loglama


    def pop(self):
        """Yığının tepesinden bir eşya çıkarır ve döndürür. Yığın boşsa None döndürür."""
        if not self.is_empty():
            item = self._items.pop()
            print(f"Yığından Çıkarıldı (Pop): {item}") # Loglama
            return item
        print("Yığın boş, çıkarılacak eşya yok.") # Hata/Durum mesajı
        return None

    def peek(self):
        """Yığının tepesindeki eşyayı çıkarmadan döndürür. Yığın boşsa None döndürür."""
        if not self.is_empty():
            return self._items[-1]
        return None

    def is_empty(self):
        """Yığının boş olup olmadığını kontrol eder."""
        return len(self._items) == 0

    def size(self):
        """Yığındaki eşya sayısını döndürür."""
        return len(self._items)

    def __len__(self):
        """len() fonksiyonu ile yığın boyutunu almayı sağlar."""
        return self.size()

    def get_items(self):
        """GUI'de göstermek için yığındaki tüm öğelerin bir listesini döndürür (Tepedeki en sonda)."""
        return list(self._items)

    def __str__(self):
        """Yığının string temsilini döndürür."""
        return " | ".join(str(i) for i in reversed(self._items)) # Tepedeki önce görünecek şekilde