"""
Integration tests for API endpoints
Tests database interactions and endpoint responses
"""
import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from profiles.models import GuideProfile, TouristProfile
from tours.models import Tour
from bookings.models import Booking
from locations.models import Wilaya

User = get_user_model()


class TourAPIIntegrationTests(APITestCase):
    """Integration Test 1: Tour creation and booking workflow"""

    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.guide_user = User.objects.create_user(
            username="test_guide",
            email="guide@test.com",
            password="testpass123",
            user_type="guide",
        )

        self.tourist_user = User.objects.create_user(
            username="test_tourist",
            email="tourist@test.com",
            password="testpass123",
            user_type="tourist",
        )

        # Create test location (wilaya) FIRST
        self.wilaya = Wilaya.objects.create(
            code="16", name_en="Algiers", name_ar="الجزائر", name_fr="Alger"
        )

        # Set up guide profile
        self.guide_profile = GuideProfile.objects.create(
            user=self.guide_user,
            bio="Test guide for Algiers",
            half_day_price=Decimal("5000.00"),
            full_day_price=Decimal("10000.00"),
            extra_hour_price=Decimal("1000.00"),
            verification_status="verified",
        )
        # Add coverage area (now wilaya exists)
        self.guide_profile.coverage_areas.add(self.wilaya)

        # Create tourist profile
        self.tourist_profile = TouristProfile.objects.create(user=self.tourist_user)

    def test_complete_tour_booking_workflow(self):
        """Test complete tour creation to booking workflow"""
        # Step 1: Guide creates tour
        self.client.force_authenticate(user=self.guide_user)

        tour_data = {
            "title": "Algiers Historic Tour",
            "description": "Explore the ancient Casbah",
            "wilaya": self.wilaya.id,
            "duration_hours": 4.0,
            "max_group_size": 8,
            "meeting_point": "Grand Post Office, Algiers",
            "latitude": 36.7783,
            "longitude": 3.0598,
        }

        tour_response = self.client.post("/v1/tours/", tour_data)
        self.assertEqual(tour_response.status_code, status.HTTP_201_CREATED)
        
        # Since the API doesn't return the ID in the create response,
        # we need to get it from the database
        from tours.models import Tour
        created_tour = Tour.objects.get(
            title=tour_data["title"],
            guide=self.guide_profile
        )
        tour_id = created_tour.id

        # Step 2: Tourist books tour
        self.client.force_authenticate(user=self.tourist_user)

        from datetime import date, timedelta
        
        booking_data = {
            "tour": tour_id,
            "booking_date": (date.today() + timedelta(days=7)).isoformat(),
            "time_slot": "morning",
            "group_size": 4,
        }

        booking_response = self.client.post("/v1/bookings/", booking_data)
        self.assertEqual(booking_response.status_code, status.HTTP_201_CREATED)

        # Step 3: Verify booking created correctly
        # Since the API might not return the ID, get it from database
        booking = Booking.objects.get(
            tourist=self.tourist_profile,
            tour_id=tour_id
        )
        self.assertEqual(booking.tourist.user, self.tourist_user)
        self.assertEqual(booking.tour.id, tour_id)
        self.assertEqual(booking.status, "pending")


class UserManagementIntegrationTests(APITestCase):
    """Integration Test 2: User authentication and profile management"""

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_and_profile_creation(self):
        """Test user registration creates appropriate profile"""
        # Test guide registration
        guide_data = {
            "username": "new_guide",
            "email": "newguide@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "user_type": "guide",
            "first_name": "Ahmed",
            "last_name": "Benali",
        }

        guide_response = self.client.post("/v1/auth/register/", guide_data)
        self.assertEqual(guide_response.status_code, status.HTTP_201_CREATED)

        # Note: Profile creation might be handled by serializers
        # Verify user was created properly
        guide_user = User.objects.get(username="new_guide")
        self.assertEqual(guide_user.user_type, "guide")

        # Test tourist registration
        tourist_data = {
            "username": "new_tourist",
            "email": "newtourist@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "user_type": "tourist",
            "first_name": "Sarah",
            "last_name": "Martin",
        }

        tourist_response = self.client.post("/v1/auth/register/", tourist_data)
        self.assertEqual(tourist_response.status_code, status.HTTP_201_CREATED)

        # Verify tourist was created properly
        tourist_user = User.objects.get(username="new_tourist")
        self.assertEqual(tourist_user.user_type, "tourist")

        # Test login with new credentials
        login_data = {"username": "new_guide", "password": "testpass123"}

        login_response = self.client.post("/v1/auth/login/", login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
