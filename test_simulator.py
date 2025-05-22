import unittest
from main import SimulationController
from models.queue import PassengerQueue
from models.stack import BaggageStack
from models.linkedlist import LinkedList
from models.yolcu import Passenger
from utils.olasilik import generate_random_baggage, esya_tehlikeli_mi

class TestLuggageSimulator(unittest.TestCase):
    def setUp(self):
        """Her test öncesi çalıştırılır"""
        self.controller = SimulationController()
        # GUI olmadan test için
        self.controller.gui_manager = None

    def test_passenger_creation(self):
        """Yolcu oluşturma ve kuyruğa ekleme testi"""
        passenger = self.controller.yolcu_olustur_ve_ekle()
        self.assertIsInstance(passenger, Passenger)
        self.assertEqual(self.controller.passenger_queue.size(), 1)

    def test_blacklist_check(self):
        """Kara liste kontrolü testi"""
        # Kara listeye bir yolcu ekle
        test_id = "Yolcu #999"
        self.controller.blacklist.append(test_id)
        
        # Test yolcusu oluştur
        passenger = Passenger()
        passenger.passenger_id = test_id
        
        # Kontrol et
        is_blacklisted = self.controller.kara_listede_mi(test_id)
        self.assertTrue(is_blacklisted)

    def test_dangerous_item_detection(self):
        """Tehlikeli eşya tespiti testi"""
        # Tehlikeli eşya içeren bagaj oluştur
        dangerous_baggage = ["Bıçak", "Kitap", "Laptop"]
        passenger = Passenger(baggage=dangerous_baggage)
        
        # Bagaj tarama testi
        passed = self.controller.bagaj_tarama(passenger)
        self.assertFalse(passed)  # Tehlikeli eşya varsa False dönmeli
        self.assertEqual(self.controller.baggage_stack.size(), 3)  # Tüm eşyalar stack'e eklenmeli

    def test_full_simulation(self):
        """Tam simülasyon testi"""
        # 5 yolcu ekle
        for _ in range(5):
            self.controller.yolcu_olustur_ve_ekle()
        
        # Tüm kuyruğu işle
        while not self.controller.passenger_queue.is_empty():
            self.controller.simulasyon_adimini_calistir()
        
        # İstatistikleri kontrol et
        self.assertEqual(self.controller.total_passengers_processed, 5)
        self.assertTrue(self.controller.passenger_queue.is_empty())

    def test_stack_inspection(self):
        """Stack inceleme testi"""
        # Stack'e bazı eşyalar ekle
        items = ["Bıçak", "Kitap", "Laptop"]
        for item in items:
            self.controller.baggage_stack.push(item)
        
        # Stack'i incele
        self.controller.stack_taramasi()
        
        # Stack boş olmalı
        self.assertTrue(self.controller.baggage_stack.is_empty())

if __name__ == '__main__':
    unittest.main() 