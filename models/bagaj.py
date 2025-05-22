class Baggage:
    """Bagaj sınıfı, yolcunun eşyalarını ve bagaj durumunu yönetir."""
    
    def __init__(self, items=None):
        """Yeni bir bagaj nesnesi oluşturur."""
        self.items = items if items is not None else []
        self.is_suspicious = False
        self.suspicious_items = []
        
    def add_item(self, item):
        """Bagaja yeni bir eşya ekler."""
        self.items.append(item)
        
    def get_items(self):
        """Bagajdaki tüm eşyaları döndürür."""
        return self.items
        
    def has_dangerous_items(self, dangerous_items_list):
        """Bagajda tehlikeli eşya olup olmadığını kontrol eder."""
        self.suspicious_items = [item for item in self.items if item in dangerous_items_list]
        self.is_suspicious = len(self.suspicious_items) > 0
        return self.is_suspicious
        
    def __len__(self):
        """Bagajdaki eşya sayısını döndürür."""
        return len(self.items)
        
    def __iter__(self):
        """Bagajdaki eşyalar üzerinde iterasyon sağlar."""
        return iter(self.items)
        
    def __str__(self):
        """Bagajın string temsilini döndürür."""
        return f"Bagaj ({len(self)} eşya)" + (" [Şüpheli]" if self.is_suspicious else "")
        
    def __repr__(self):
        """Bagajın detaylı string temsilini döndürür."""
        return f"Baggage(items={self.items}, suspicious={self.is_suspicious})"
