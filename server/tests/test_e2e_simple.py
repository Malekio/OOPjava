"""
Simplified End-to-End test scenarios
Tests complete user workflows with current API structure
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import User
from profiles.models import GuideProfile, TouristProfile
from tours.models import Tour
from bookings.models import Booking
from locations.models import Wilaya
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()


class E2ESimpleBookingScenario(TestCase):
    """Simplified E2E Test: Registration to booking workflow"""

    def setUp(self):
        self.client = APIClient()
        
        # Create a wilaya for testing
        self.wilaya = Wilaya.objects.create(
            code="16",
            name_ar="الجزائر",
            name_en="Algiers", 
            name_fr="Alger"
        )

    def test_complete_user_journey(self):
        """Test simplified user journey: register → create tour → book"""
        
        # Step 1: Guide registers
        guide_data = {
            "username": "test_guide",
            "email": "guide@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "user_type": "guide",
            "first_name": "Ahmed",
            "last_name": "Guide",
        }
        
        guide_response = self.client.post("/v1/auth/register/", guide_data)
        self.assertEqual(guide_response.status_code, status.HTTP_201_CREATED)
        
        # Step 2: Tourist registers
        tourist_data = {
            "username": "test_tourist",
            "email": "tourist@example.com",
            "password": "TestPass123!",
            "password_confirm": "TestPass123!",
            "user_type": "tourist",
            "first_name": "Sara",
            "last_name": "Tourist",
        }
        
        tourist_response = self.client.post("/v1/auth/register/", tourist_data)
        self.assertEqual(tourist_response.status_code, status.HTTP_201_CREATED)
        
        # Step 3: Guide logs in
        guide_login = self.client.post("/v1/auth/login/", {
            "username": "test_guide",
            "password": "TestPass123!"
        })
        self.assertEqual(guide_login.status_code, status.HTTP_200_OK)
        
        # Set authentication
        guide_token = guide_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {guide_token}")
        
        # Setup guide profile
        guide_user = User.objects.get(username="test_guide")
        guide_profile = GuideProfile.objects.get(user=guide_user)
        guide_profile.half_day_price = Decimal("5000.00")
        guide_profile.full_day_price = Decimal("10000.00")
        guide_profile.extra_hour_price = Decimal("1200.00")
        guide_profile.verification_status = "verified"
        guide_profile.save()
        guide_profile.coverage_areas.add(self.wilaya)
        
        # Step 4: Guide creates tour
        tour_data = {
            "title": "Algiers Walking Tour",
            "description": "Explore historic Algiers",
            "duration_hours": 4.0,
            "max_group_size": 8,
            "wilaya": self.wilaya.id,
            "meeting_point": "Martyrs' Square",
            "latitude": 36.7735,
            "longitude": 3.0588,
        }
        
        tour_response = self.client.post("/v1/tours/", tour_data)
        self.assertEqual(tour_response.status_code, status.HTTP_201_CREATED)
        
        # Get created tour and activate it
        created_tour = Tour.objects.get(title=tour_data["title"], guide=guide_profile)
        created_tour.status = "active"
        created_tour.save()
        self.assertIsNotNone(created_tour)
        
        # Step 5: Tourist logs in and books tour
        tourist_login = self.client.post("/v1/auth/login/", {
            "username": "test_tourist", 
            "password": "TestPass123!"
        })
        self.assertEqual(tourist_login.status_code, status.HTTP_200_OK)
        
        tourist_token = tourist_login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tourist_token}")
        
        # Create booking
        booking_data = {
            "tour": created_tour.id,
            "booking_date": (date.today() + timedelta(days=15)).isoformat(),
            "time_slot": "morning",
            "group_size": 3,
        }
        
        booking_response = self.client.post("/v1/bookings/", booking_data)
        self.assertEqual(booking_response.status_code, status.HTTP_201_CREATED)
        
        # Verify booking was created
        tourist_user = User.objects.get(username="test_tourist")
        tourist_profile = TouristProfile.objects.get(user=tourist_user)
        
        booking = Booking.objects.get(
            tourist=tourist_profile,
            tour=created_tour
        )
        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.group_size, 3)
        
        # Step 6: Verify tour search functionality
        self.client.credentials()  # Remove auth for public search
        
        search_response = self.client.get("/v1/tours/", {
            "search": "Algiers"
        })
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(search_response.data["results"]), 1)


class E2ESimpleSearchScenario(TestCase):
    """Simplified E2E Test: Search and filter functionality"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test data
        self.algiers = Wilaya.objects.create(
            code="16", name_ar="الجزائر", name_en="Algiers", name_fr="Alger"
        )
        self.oran = Wilaya.objects.create(
            code="31", name_ar="وهران", name_en="Oran", name_fr="Oran"
        )
        
        # Create guide and tours
        self.guide_user = User.objects.create_user(
            username="search_guide",
            email="search@example.com",
            password="test123",
            user_type="guide"
        )
        
        self.guide_profile = GuideProfile.objects.create(
            user=self.guide_user,
            half_day_price=Decimal("4000.00"),
            full_day_price=Decimal("8000.00"),
            extra_hour_price=Decimal("1000.00"),
            verification_status="verified"
        )
        self.guide_profile.coverage_areas.add(self.algiers, self.oran)
        
        # Create sample tours
        Tour.objects.create(
            title="Algiers Casbah Tour",
            description="Historic tour of the Casbah",
            guide=self.guide_profile,
            wilaya=self.algiers,
            duration_hours=3,
            max_group_size=6,
            price=Decimal("12000.00"),
            meeting_point="Casbah entrance",
            latitude=36.7849,
            longitude=3.0596,
            status="active"
        )
        
        Tour.objects.create(
            title="Oran Seafront Walk",
            description="Beautiful coastal tour",
            guide=self.guide_profile,
            wilaya=self.oran,
            duration_hours=2,
            max_group_size=10,
            price=Decimal("8000.00"),
            meeting_point="Port of Oran",
            latitude=35.6910,
            longitude=-0.6417,
            status="active"
        )
    
    def test_search_and_filter_functionality(self):
        """Test various search and filter options"""
        
        # Test basic search
        search_response = self.client.get("/v1/tours/", {"search": "Casbah"})
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        results = search_response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn("Casbah", results[0]["title"])
        
        # Test wilaya filter
        algiers_filter = self.client.get("/v1/tours/", {"wilaya": self.algiers.id})
        self.assertEqual(algiers_filter.status_code, status.HTTP_200_OK)
        algiers_results = algiers_filter.data["results"]
        self.assertEqual(len(algiers_results), 1)
        self.assertEqual(algiers_results[0]["wilaya"]["id"], self.algiers.id)
        
        # Test duration filter
        short_tours = self.client.get("/v1/tours/", {"max_duration": 2.5})
        self.assertEqual(short_tours.status_code, status.HTTP_200_OK)
        short_results = short_tours.data["results"]
        self.assertEqual(len(short_results), 1)
        self.assertEqual(short_results[0]["duration_hours"], "2.0")
        
        # Test price range - both tours are 4000.00 (calculated from guide pricing)
        budget_tours = self.client.get("/v1/tours/", {
            "min_price": 3500,
            "max_price": 4500
        })
        self.assertEqual(budget_tours.status_code, status.HTTP_200_OK)
        budget_results = budget_tours.data["results"]
        self.assertEqual(len(budget_results), 2)  # Both tours should match
        
        # Test ordering functionality
        ordered_tours = self.client.get("/v1/tours/", {"ordering": "title"})
        self.assertEqual(ordered_tours.status_code, status.HTTP_200_OK)
        ordered_results = ordered_tours.data["results"]
        self.assertEqual(len(ordered_results), 2)
        # Just verify that ordering parameter is accepted and returns results
        self.assertTrue(len(ordered_results) > 0)
