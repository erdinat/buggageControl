from models.bagaj import Baggage

class Passenger:
    """Simülasyondaki bir yolcuyu temsil eder."""
    _id_counter = 1 # Tüm yolcular için benzersiz ID sağlamak üzere sınıf seviyesinde sayaç

    def __init__(self, baggage=None):
        """Yeni bir yolcu nesnesi oluşturur."""
        # Eğer ilk yolcuysa sayacı sıfırla
        if Passenger._id_counter > 1000:  # Güvenlik için bir üst limit
            Passenger._id_counter = 1
            
        self.passenger_id = f"Yolcu #{Passenger._id_counter}"
        Passenger._id_counter += 1
        # Baggage sınıfını kullan
        self.baggage = Baggage(baggage) if baggage is not None else Baggage()
        self.is_risky = False # Başlangıçta riskli değil
        print(f"Oluşturuldu: {self}") # Oluşturma logu

    def add_item(self, item):
        """Yolcunun bagajına bir eşya ekler."""
        self.baggage.add_item(item)

    def set_risky(self, status=True):
        """Yolcunun risk durumunu ayarlar."""
        self.is_risky = status
        print(f"{self.passenger_id} risk durumu güncellendi: {status}")

    def __str__(self):
        """Yolcunun kolay okunabilir string temsilini döndürür."""
        risk_str = " (Riskli!)" if self.is_risky else ""
        return f"{self.passenger_id}{risk_str} - {self.baggage}"

    def __repr__(self):
        """Nesnenin repr gösterimi (debug için faydalı)."""
        return f"Passenger(id={self.passenger_id}, baggage={self.baggage}, risky={self.is_risky})"