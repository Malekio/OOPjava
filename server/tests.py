from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import GuideProfile, TouristProfile
from locations.models import Wilaya

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='tourist'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'tourist')
        self.assertTrue(user.is_tourist)
        self.assertFalse(user.is_guide)

class GuideProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='guide1',
            email='guide@example.com',
            password='testpass123',
            user_type='guide'
        )
        self.wilaya = Wilaya.objects.create(
            code='16',
            name_ar='الجزائر',
            name_en='Algiers',
            name_fr='Alger'
        )
        
    def test_guide_profile_creation(self):
        """Test creating a guide profile"""
        guide = GuideProfile.objects.create(
            user=self.user,
            bio='Experienced tour guide',
            half_day_price=50.00,
            full_day_price=100.00,
            extra_hour_price=15.00
        )
        guide.coverage_areas.add(self.wilaya)
        
        self.assertEqual(guide.user.username, 'guide1')
        self.assertEqual(guide.half_day_price, 50.00)
        self.assertTrue(guide.coverage_areas.filter(code='16').exists())
        
    def test_price_calculation(self):
        """Test tour price calculation based on duration"""
        guide = GuideProfile.objects.create(
            user=self.user,
            bio='Test guide',
            half_day_price=50.00,
            full_day_price=100.00,
            extra_hour_price=15.00
        )
        
        # Test half day price (3 hours)
        self.assertEqual(guide.calculate_tour_price(3), 50.00)
        
        # Test full day price (6 hours)
        self.assertEqual(guide.calculate_tour_price(6), 100.00)
        
        # Test with extra hours (10 hours)
        expected_price = 100.00 + (2 * 15.00)  # full day + 2 extra hours
        self.assertEqual(guide.calculate_tour_price(10), expected_price)
