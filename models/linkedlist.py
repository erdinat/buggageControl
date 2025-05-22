
class Node:
    """Bağlı listenin her bir düğümünü temsil eder."""
    def __init__(self, data):
        self.data = data  # Düğümün taşıdığı veri (örn: yolcu ID)
        self.next = None  # Bir sonraki düğüme referans

class LinkedList:
    """Tek Yönlü Bağlı Liste sınıfı (Kara Liste için)."""
    def __init__(self):
        """Boş bir bağlı liste oluşturur."""
        self.head = None
        print("Kara Liste (Bağlı Liste) başlatıldı.") # Başlangıç bilgisi


    def append(self, data):
        """Listenin sonuna yeni bir düğüm ekler."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            print(f"Kara Listeye Eklendi (İlk): {data}") # Loglama
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        print(f"Kara Listeye Eklendi: {data}") # Loglama

    def search(self, target_data):
        """Listede belirli bir veriyi (yolcu ID) arar. Bulursa True, bulamazsa False döner."""
        current_node = self.head
        while current_node:
            if current_node.data == target_data:
                print(f"Kara Listede Bulundu: {target_data}") # Loglama
                return True
            current_node = current_node.next
        print(f"Kara Listede Bulunamadı: {target_data}") # Loglama
        return False

    def is_empty(self):
        """Listenin boş olup olmadığını kontrol eder."""
        return self.head is None

    def display(self):
        """Listenin içeriğini yazdırmak için (Debug amaçlı)."""
        elements = []
        current_node = self.head
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        print("Kara Liste İçeriği: " + " -> ".join(elements))

    def get_items(self):
        """GUI'de göstermek için listedeki tüm öğelerin bir listesini döndürür."""
        items = []
        current_node = self.head
        while current_node:
            items.append(current_node.data)
            current_node = current_node.next
        return items