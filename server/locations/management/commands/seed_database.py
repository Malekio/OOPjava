"""
Comprehensive database seeding command
Creates demo data for all aspects of the DZ-TourGuide platform
"""
import random
from decimal import Decimal
from datetime import date, timedelta, datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker

from accounts.models import User
from profiles.models import (
    GuideProfile,
    TouristProfile,
    GuideAvailability,
    GuideCertification,
)
from locations.models import Wilaya, City, Tourist_Place
from tours.models import Tour, TourItinerary
from bookings.models import Booking
from reviews.models import Review
from messaging.models import Message

fake = Faker(["fr_FR", "ar_DZ"])  # French and Arabic locales for Algeria


class Command(BaseCommand):
    help = "Seeds the database with comprehensive demo data for DZ-TourGuide platform"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=50,
            help="Number of users to create (split between tourists and guides)",
        )
        parser.add_argument(
            "--tours", type=int, default=30, help="Number of tours to create"
        )
        parser.add_argument(
            "--bookings", type=int, default=100, help="Number of bookings to create"
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("🇩🇿 Starting DZ-TourGuide database seeding...")
        )

        with transaction.atomic():
            self.create_locations()
            users = self.create_users(options["users"])
            tours = self.create_tours(options["tours"])
            self.create_bookings(options["bookings"], tours)
            self.create_reviews()
            self.create_messages()

        self.stdout.write(
            self.style.SUCCESS("✅ Database seeding completed successfully!")
        )
        self.print_summary()

    def create_locations(self):
        """Create Algerian wilayas, cities, and tourist places"""
        self.stdout.write("Creating locations data...")

        # Algerian Wilayas (provinces)
        wilaya_data = [
            ("Alger", "الجزائر", "Capital wilaya with historic Casbah"),
            ("Oran", "وهران", "Western port city with Spanish influence"),
            ("Constantine", "قسنطينة", "City of bridges in eastern Algeria"),
            ("Annaba", "عنابة", "Coastal city with Roman ruins"),
            ("Blida", "البليدة", "City of roses in the Atlas foothills"),
            ("Batna", "باتنة", "Gateway to Aurès Mountains"),
            ("Béjaïa", "بجاية", "Berber coastal city"),
            ("Biskra", "بسكرة", "Saharan oasis city"),
            ("Béchar", "بشار", "Desert town near Morocco"),
            ("Bouira", "البويرة", "Mountain wilaya south of Algiers"),
        ]

        wilayas = []
        for name_fr, name_ar, desc in wilaya_data:
            wilaya, created = Wilaya.objects.get_or_create(
                name=name_fr, defaults={"name_arabic": name_ar, "description": desc}
            )
            wilayas.append(wilaya)

        # Cities and tourist places
        locations_data = [
            # Algiers
            (
                "Alger",
                "Algiers",
                [
                    (
                        "Casbah of Algiers",
                        "UNESCO World Heritage ancient citadel",
                        36.7783,
                        3.0598,
                    ),
                    (
                        "Notre Dame d'Afrique",
                        "Basilica overlooking the Mediterranean",
                        36.7667,
                        3.0500,
                    ),
                    (
                        "Martyrs Memorial",
                        "Monument commemorating independence war",
                        36.7539,
                        3.0588,
                    ),
                    (
                        "National Museum of Bardo",
                        "Prehistoric and ethnographic museum",
                        36.7556,
                        3.0419,
                    ),
                    (
                        "Botanical Garden of Hamma",
                        "Historic botanical garden",
                        36.7383,
                        3.0622,
                    ),
                ],
            ),
            # Oran
            (
                "Oran",
                "Oran",
                [
                    (
                        "Santa Cruz Fort",
                        "Spanish colonial fortress on Mount Murdjadjo",
                        35.7167,
                        -0.6167,
                    ),
                    ("Ahmed Bey Palace", "Ottoman-era palace", 35.6911, -0.6417),
                    (
                        "Great Mosque of Oran",
                        "Historic mosque in city center",
                        35.6956,
                        -0.6333,
                    ),
                    (
                        "Oran Opera House",
                        "Beautiful Belle Époque theater",
                        35.6944,
                        -0.6333,
                    ),
                    (
                        "Les Andalouses Beach",
                        "Popular coastal resort area",
                        35.7833,
                        -0.7833,
                    ),
                ],
            ),
            # Constantine
            (
                "Constantine",
                "Constantine",
                [
                    (
                        "Sidi M'Cid Bridge",
                        "Spectacular suspension bridge over Rhumel gorges",
                        36.3650,
                        6.6147,
                    ),
                    (
                        "Palace of Ahmed Bey",
                        "Magnificent Ottoman palace",
                        36.3667,
                        6.6167,
                    ),
                    (
                        "Emir Abdelkader Mosque",
                        "Modern mosque with traditional architecture",
                        36.3531,
                        6.6261,
                    ),
                    (
                        "Constantine Museum",
                        "Archaeological and art museum",
                        36.3667,
                        6.6167,
                    ),
                    (
                        "Rhumel Gorges",
                        "Dramatic limestone gorges dividing the city",
                        36.3667,
                        6.6167,
                    ),
                ],
            ),
        ]

        self.cities = []
        self.places = []

        for wilaya_name, city_name, places_data in locations_data:
            wilaya = next(w for w in wilayas if w.name == wilaya_name)

            city, created = City.objects.get_or_create(
                name=city_name,
                defaults={
                    "wilaya": wilaya,
                    "description": f"Major city in {wilaya_name} wilaya",
                },
            )
            self.cities.append(city)

            for place_name, desc, lat, lng in places_data:
                place, created = Tourist_Place.objects.get_or_create(
                    name=place_name,
                    defaults={
                        "city": city,
                        "description": desc,
                        "latitude": lat,
                        "longitude": lng,
                    },
                )
                self.places.append(place)

        self.stdout.write(
            f"  ✓ Created {len(wilayas)} wilayas, {len(self.cities)} cities, {len(self.places)} places"
        )

    def create_users(self, count):
        """Create diverse users (tourists and guides)"""
        self.stdout.write(f"Creating {count} users...")

        users = []

        # Algerian guide names
        algerian_guide_names = [
            ("Karim", "Benali"),
            ("Amina", "Boumediene"),
            ("Youcef", "Zeroual"),
            ("Fatima", "Hadj"),
            ("Mohammed", "Benaissa"),
            ("Aicha", "Mokrani"),
            ("Rachid", "Khelifi"),
            ("Samira", "Ouali"),
            ("Abderrahmane", "Cherif"),
            ("Zahia", "Benahmed"),
            ("Omar", "Djillali"),
            ("Leila", "Brahimi"),
        ]

        # International tourist names
        tourist_countries = [
            "France",
            "Spain",
            "Germany",
            "Italy",
            "UK",
            "USA",
            "Canada",
            "Morocco",
            "Tunisia",
        ]

        # Create guides (40% of users)
        guide_count = int(count * 0.4)
        for i in range(guide_count):
            first_name, last_name = random.choice(algerian_guide_names)
            username = f"{first_name.lower()}_{last_name.lower()}_{i}"

            user = User.objects.create_user(
                username=username,
                email=f"{username}@tourguide.dz",
                password="demo123",
                user_type="guide",
                first_name=first_name,
                last_name=last_name,
                phone_number=f"+213{random.randint(500000000, 799999999)}",
            )

            # Create guide profile
            profile = GuideProfile.objects.get(user=user)
            profile.bio = fake.text(max_nb_chars=800)
            profile.years_of_experience = random.randint(1, 15)
            profile.languages = random.sample(
                ["Arabic", "French", "English", "Berber", "Spanish"],
                k=random.randint(2, 4),
            )
            profile.half_day_price = Decimal(random.randint(2000, 6000))
            profile.full_day_price = Decimal(int(profile.half_day_price * 1.8))
            profile.extra_hour_price = Decimal(random.randint(800, 2000))
            profile.verification_status = random.choice(
                ["verified", "verified", "pending"]
            )  # More verified
            profile.average_rating = Decimal(random.uniform(3.5, 5.0)).quantize(
                Decimal("0.01")
            )
            profile.total_reviews = random.randint(0, 50)
            profile.total_tours_completed = random.randint(0, 200)
            profile.save()

            # Add coverage areas
            profile.coverage_areas.set(
                random.sample(list(Wilaya.objects.all()), k=random.randint(1, 3))
            )

            users.append(user)

        # Create tourists (60% of users)
        tourist_count = count - guide_count
        for i in range(tourist_count):
            country = random.choice(tourist_countries)
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}_{last_name.lower()}_{i}"

            user = User.objects.create_user(
                username=username,
                email=f"{username}@email.com",
                password="demo123",
                user_type="tourist",
                first_name=first_name,
                last_name=last_name,
                phone_number=fake.phone_number(),
            )

            # Create tourist profile
            profile = TouristProfile.objects.get(user=user)
            profile.bio = fake.text(max_nb_chars=300)
            profile.nationality = country
            profile.preferred_language = random.choice(["French", "English", "Arabic"])
            profile.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
            profile.save()

            users.append(user)

        self.stdout.write(
            f"  ✓ Created {guide_count} guides and {tourist_count} tourists"
        )
        return users

    def create_tours(self, count):
        """Create diverse tours across all locations"""
        self.stdout.write(f"Creating {count} tours...")

        tour_templates = [
            (
                "Historic Casbah Walking Tour",
                "Explore the ancient streets and Ottoman architecture",
                3.5,
                8,
            ),
            (
                "Colonial Architecture Discovery",
                "Discover French colonial buildings and boulevards",
                4.0,
                10,
            ),
            (
                "Sahara Desert Adventure",
                "Camel trekking and desert camping experience",
                8.0,
                6,
            ),
            (
                "Mountain Hiking Expedition",
                "Trek through Atlas Mountains and Berber villages",
                6.0,
                8,
            ),
            ("Coastal Sunset Tour", "Mediterranean beaches and seaside towns", 4.5, 12),
            (
                "Archaeological Heritage Tour",
                "Visit Roman ruins and ancient sites",
                5.0,
                10,
            ),
            (
                "Traditional Crafts Workshop",
                "Learn pottery, weaving, and metalwork",
                3.0,
                6,
            ),
            ("Culinary Discovery Tour", "Taste authentic Algerian cuisine", 4.0, 8),
            (
                "Islamic Heritage Tour",
                "Historic mosques and Islamic architecture",
                3.5,
                10,
            ),
            (
                "Nature and Wildlife Safari",
                "Explore national parks and endemic species",
                7.0,
                8,
            ),
        ]

        guides = User.objects.filter(
            user_type="guide", guide_profile__verification_status="verified"
        )
        tours = []

        for i in range(count):
            template = random.choice(tour_templates)
            guide = random.choice(guides)
            city = random.choice(self.cities)

            # Create base tour
            tour = Tour.objects.create(
                guide=guide,
                title=f"{city.name} {template[0]}",
                description=f"{template[1]} in the beautiful city of {city.name}. {fake.text(max_nb_chars=200)}",
                duration_hours=template[2] + random.uniform(-0.5, 1.0),
                max_group_size=template[3] + random.randint(-2, 2),
                is_active=random.choice([True, True, True, False]),  # Mostly active
            )

            # Add random places from the same city
            city_places = [p for p in self.places if p.city == city]
            if city_places:
                tour.places.set(
                    random.sample(
                        city_places, k=min(len(city_places), random.randint(1, 3))
                    )
                )

            tours.append(tour)

        self.stdout.write(f"  ✓ Created {len(tours)} tours")
        return tours

    def create_bookings(self, count, tours):
        """Create realistic bookings with various statuses"""
        self.stdout.write(f"Creating {count} bookings...")

        tourists = User.objects.filter(user_type="tourist")
        active_tours = [t for t in tours if t.is_active]

        # Generate bookings across the past year and future months
        start_date = date.today() - timedelta(days=365)
        end_date = date.today() + timedelta(days=90)

        for i in range(count):
            tourist = random.choice(tourists)
            tour = random.choice(active_tours)

            # Generate realistic booking date
            random_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )

            # Status distribution (realistic workflow)
            status_weights = [
                ("pending", 0.15),
                ("confirmed", 0.40),
                ("completed", 0.35),
                ("cancelled", 0.10),
            ]
            status = random.choices(
                [s[0] for s in status_weights], weights=[s[1] for s in status_weights]
            )[0]

            booking = Booking.objects.create(
                tourist=tourist,
                tour=tour,
                requested_date=random_date,
                time_slot=random.choice(["morning", "afternoon", "evening"]),
                group_size=random.randint(1, min(tour.max_group_size, 8)),
                notes=fake.text(max_nb_chars=200) if random.random() > 0.3 else "",
                status=status,
                total_price=tour.guide.guide_profile.calculate_tour_price(
                    tour.duration_hours
                ),
            )

        self.stdout.write(f"  ✓ Created {count} bookings")

    def create_reviews(self):
        """Create reviews for completed bookings"""
        self.stdout.write("Creating reviews...")

        completed_bookings = Booking.objects.filter(status="completed")
        review_count = 0

        for booking in completed_bookings:
            # 80% chance of getting a review
            if random.random() <= 0.8:
                rating = random.choices(
                    [1, 2, 3, 4, 5],
                    weights=[0.05, 0.10, 0.15, 0.35, 0.35],  # Skewed positive
                )[0]

                review_templates = {
                    5: [
                        "Absolutely amazing experience! {} was incredibly knowledgeable and passionate.",
                        "Perfect tour! {} showed us hidden gems we never would have found alone.",
                        "Outstanding guide! {} made the history come alive with great storytelling.",
                    ],
                    4: [
                        "Great tour overall. {} was professional and the sites were beautiful.",
                        "Really enjoyed the experience. {} was helpful and accommodating.",
                        "Good value for money. {} knew a lot about local culture.",
                    ],
                    3: [
                        "Decent tour. {} was okay but could be more engaging.",
                        "Average experience. {} covered the basics well enough.",
                        "It was fine. {} was on time and knew the locations.",
                    ],
                    2: [
                        "Tour was disappointing. {} seemed unprepared.",
                        "Expected better. {} was not very enthusiastic.",
                        "Overpriced for what we got. {} needs improvement.",
                    ],
                    1: [
                        "Very poor experience. {} was unprofessional.",
                        "Would not recommend. {} was late and uninformed.",
                        "Terrible tour. {} was rude and dismissive.",
                    ],
                }

                comment = (
                    random.choice(review_templates[rating]).format(
                        booking.tour.guide.first_name
                    )
                    + " "
                    + fake.text(max_nb_chars=100)
                )

                Review.objects.create(booking=booking, rating=rating, comment=comment)
                review_count += 1

        self.stdout.write(f"  ✓ Created {review_count} reviews")

    def create_messages(self):
        """Create sample messages between users"""
        self.stdout.write("Creating messages...")

        tourists = list(User.objects.filter(user_type="tourist")[:20])
        guides = list(User.objects.filter(user_type="guide")[:15])

        message_count = 0
        for _ in range(100):  # Create 100 message exchanges
            tourist = random.choice(tourists)
            guide = random.choice(guides)

            # Tourist inquires about tour
            Message.objects.create(
                sender=tourist,
                recipient=guide,
                content=f"Hello {guide.first_name}, I'm interested in your tours around {random.choice(self.cities).name}. {fake.text(max_nb_chars=150)}",
            )

            # Guide responds (70% of the time)
            if random.random() <= 0.7:
                Message.objects.create(
                    sender=guide,
                    recipient=tourist,
                    content=f"Hello {tourist.first_name}! I'd be happy to help you explore. {fake.text(max_nb_chars=120)}",
                )
                message_count += 2
            else:
                message_count += 1

        self.stdout.write(f"  ✓ Created {message_count} messages")

    def print_summary(self):
        """Print database statistics"""
        self.stdout.write("\n📊 Database Summary:")
        self.stdout.write(f"  Users: {User.objects.count()}")
        self.stdout.write(
            f'    - Guides: {User.objects.filter(user_type="guide").count()}'
        )
        self.stdout.write(
            f'    - Tourists: {User.objects.filter(user_type="tourist").count()}'
        )
        self.stdout.write(
            f"  Locations: {Tourist_Place.objects.count()} places in {City.objects.count()} cities"
        )
        self.stdout.write(
            f"  Tours: {Tour.objects.count()} ({Tour.objects.filter(is_active=True).count()} active)"
        )
        self.stdout.write(f"  Bookings: {Booking.objects.count()}")
        self.stdout.write(f"  Reviews: {Review.objects.count()}")
        self.stdout.write(f"  Messages: {Message.objects.count()}")

        # Performance insights
        self.stdout.write("\n⚡ Performance Notes:")
        self.stdout.write("  - All models have strategic database indexes")
        self.stdout.write("  - User queries indexed by type and verification status")
        self.stdout.write("  - Location queries optimized with geographic indexes")
        self.stdout.write("  - Booking queries indexed by status and date ranges")
        self.stdout.write("  - Review aggregations optimized for guide ratings")
