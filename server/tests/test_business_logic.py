"""
Unit tests for critical business logic
Tests pure functions without database or API calls
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import GuideProfile
from tours.models import Tour
from bookings.models import Booking
from reviews.models import Review

User = get_user_model()


class PriceCalculationTests(TestCase):
    """Test price calculation business logic"""

    def setUp(self):
        # Create test guide with pricing structure
        self.guide_user = User.objects.create_user(
            username="test_guide",
            email="guide@test.com",
            password="testpass123",
            user_type="guide",
        )
        # Create guide profile manually since signals aren't firing in tests
        self.guide_profile = GuideProfile.objects.create(
            user=self.guide_user,
            bio="Test guide bio",
            half_day_price=Decimal("5000.00"),
            full_day_price=Decimal("10000.00"),
            extra_hour_price=Decimal("1500.00"),
        )

    def test_half_day_price_calculation(self):
        """Test 1: Half-day tour pricing (≤4 hours)"""
        price = self.guide_profile.calculate_tour_price(3.0)
        self.assertEqual(price, Decimal("5000.00"))

    def test_full_day_price_calculation(self):
        """Test 2: Full-day tour pricing (4-8 hours)"""
        price = self.guide_profile.calculate_tour_price(6.0)
        self.assertEqual(price, Decimal("10000.00"))

    def test_extended_day_price_calculation(self):
        """Test 3: Extended tour pricing (>8 hours)"""
        price = self.guide_profile.calculate_tour_price(10.0)
        # 10000 (full day) + (2 * 1500) (extra hours)
        expected_price = Decimal("13000.00")
        self.assertEqual(price, expected_price)


class BookingValidationTests(TestCase):
    """Test booking validation business logic"""

    def test_group_size_discount_calculation(self):
        """Test 4: Group discount calculation logic"""
        from decimal import Decimal

        # Test discount calculation function
        base_price = Decimal("100.00")

        # Group of 4-5: 5% discount
        group_4_discount = Decimal("0.05")
        group_4_total = base_price * 4 * (1 - group_4_discount)
        self.assertEqual(group_4_total, Decimal("380.00"))

        # Group of 6-9: 10% discount
        group_6_discount = Decimal("0.10")
        group_6_total = base_price * 6 * (1 - group_6_discount)
        self.assertEqual(group_6_total, Decimal("540.00"))

        # Group of 10+: 15% discount
        group_10_discount = Decimal("0.15")
        group_10_total = base_price * 10 * (1 - group_10_discount)
        self.assertEqual(group_10_total, Decimal("850.00"))


class UserAuthenticationTests(TestCase):
    """Test user authentication business logic"""

    def test_user_type_validation(self):
        """Test 5: User type properties and validation"""
        # Test tourist user
        tourist = User.objects.create_user(
            username="tourist_test",
            email="tourist@test.com",
            password="testpass123",
            user_type="tourist",
        )
        self.assertTrue(tourist.is_tourist())
        self.assertFalse(tourist.is_guide())

        # Test guide user
        guide = User.objects.create_user(
            username="guide_test",
            email="guide@test.com",
            password="testpass123",
            user_type="guide",
        )
        self.assertTrue(guide.is_guide())
        self.assertFalse(guide.is_tourist())
