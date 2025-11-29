"""
Management command to create initial admin user and demo data for testing
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from profiles.models import GuideProfile, TouristProfile
from locations.models import Wilaya

User = get_user_model()

class Command(BaseCommand):
    help = 'Create initial admin user and demo data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@dztourguide.com',
            help='Admin email (default: admin@dztourguide.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Admin password (default: admin123)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Create superuser if it doesn't exist
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser {username} already exists')
            )

        # Create demo guide if it doesn't exist
        demo_guide_username = 'demo_guide'
        if not User.objects.filter(username=demo_guide_username).exists():
            guide_user = User.objects.create_user(
                username=demo_guide_username,
                email='guide@dztourguide.com',
                password='guide123',
                first_name='Ahmed',
                last_name='Benali'
            )
            
            # Create guide profile
            guide_profile = GuideProfile.objects.create(
                user=guide_user,
                bio='Experienced tour guide specializing in Algerian history and culture.',
                years_of_experience=5,
                languages=['Arabic', 'French', 'English'],
                verification_status='verified',
                half_day_price=5000.00,
                full_day_price=10000.00,
                extra_hour_price=1500.00
            )
            
            # Add coverage areas (if wilayas exist)
            if Wilaya.objects.exists():
                algiers = Wilaya.objects.filter(code='01').first()
                if algiers:
                    guide_profile.coverage_areas.add(algiers)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created demo guide: {demo_guide_username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Demo guide {demo_guide_username} already exists')
            )

        # Create demo tourist if it doesn't exist
        demo_tourist_username = 'demo_tourist'
        if not User.objects.filter(username=demo_tourist_username).exists():
            tourist_user = User.objects.create_user(
                username=demo_tourist_username,
                email='tourist@dztourguide.com',
                password='tourist123',
                first_name='Sara',
                last_name='Martin'
            )
            
            # Create tourist profile
            TouristProfile.objects.create(
                user=tourist_user,
                bio='Travel enthusiast exploring North Africa.',
                nationality='French',
                preferred_language='French'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created demo tourist: {demo_tourist_username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Demo tourist {demo_tourist_username} already exists')
            )

        self.stdout.write(
            self.style.SUCCESS(
                '\n=== DEMO ACCOUNTS CREATED ===\n'
                f'Admin: {username} / {password}\n'
                f'Guide: {demo_guide_username} / guide123\n'
                f'Tourist: {demo_tourist_username} / tourist123\n'
                '================================'
            )
        )
