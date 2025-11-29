# 🇩🇿 DZ-TourGuide Backend

A comprehensive Django REST Framework backend for DZ-TourGuide - a local tour guide booking platform for Algeria.

## 📋 Project Overview

DZ-TourGuide connects tourists with certified local guides for personalized tours across Algeria. The platform features dual user profiles (Tourists & Guides), tour management, booking system with approval workflow, and comprehensive review system.

### 🏗️ Core Features

- **Dual User Profiles**: Separate registration/login for Tourists and Guides
- **Guide Profiles**: Public profiles with photos, bio, languages, coverage areas, certifications
- **Tour Management**: Guides create predefined tours with GPS coordinates for weather integration
- **Tour Directory**: Tourists browse and search tours by city/wilaya
- **🌤️ Weather Integration**: Real-time weather forecasts for tour locations (5-day window)
- **📅 Advanced Calendar**: Time slot management (morning/afternoon/evening/full-day)
- **💬 Messaging System**: Tourist-Guide communication & custom tour requests
- **Booking System**: Request-based booking with guide approval and time slot validation
- **Flexible Pricing**: Half-day, full-day, and extra-hour pricing structure
- **Coverage Zones**: Guides specify covered wilayas with validation
- **⭐ Simplified Review System**: Streamlined 1-5 star rating system
- **Admin Panel**: Guide verification and platform management

## 🛠️ Technical Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Weather API**: OpenWeatherMap integration
- **File Storage**: Local (dev) / AWS S3 (production)
- **Caching**: Redis (includes weather data caching)
- **Task Queue**: Celery
- **API Documentation**: Auto-generated with DRF

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js (for frontend)
- PostgreSQL (production)
- Redis (caching & tasks)

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd TourGuideDZ
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database setup**
```bash
cd server
python manage.py migrate
python manage.py load_wilayas  # Load Algerian wilayas data
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`

## 🔗 API Endpoints

**Total Endpoints**: 101+ | **Complete Business Logic**: Booking workflows, Review system, Advanced search & filtering

### Authentication & User Management
```
POST   /api/v1/auth/register/        # User registration
POST   /api/v1/auth/login/           # User login (JWT)
POST   /api/v1/auth/logout/          # User logout
POST   /api/v1/auth/refresh/         # JWT token refresh
GET    /api/v1/auth/me/              # Current user profile
PUT    /api/v1/auth/me/              # Update user profile
```

### User Profiles
```
GET    /api/v1/profiles/guides/                    # List all guides
GET    /api/v1/profiles/guides/{id}/               # Guide details
GET    /api/v1/profiles/guides/me/                 # My guide profile
PUT    /api/v1/profiles/guides/me/                 # Update guide profile
POST   /api/v1/profiles/guides/certifications/    # Upload certifications
DELETE /api/v1/profiles/guides/certifications/{id}/ # Remove certification
GET    /api/v1/profiles/tourists/me/               # My tourist profile
PUT    /api/v1/profiles/tourists/me/               # Update tourist profile
GET    /api/v1/profiles/guides/{id}/pricing/       # Guide pricing structure
```

### Tours Management
```
GET    /api/v1/tours/                    # List all tours
POST   /api/v1/tours/                    # Create tour (guides only)
GET    /api/v1/tours/{id}/               # Tour details
PUT    /api/v1/tours/{id}/               # Update tour
DELETE /api/v1/tours/{id}/               # Delete tour
GET    /api/v1/tours/me/                 # My tours (guides)
GET    /api/v1/tours/search/             # Search tours
GET    /api/v1/tours/{id}/availability/  # Tour availability
POST   /api/v1/tours/{id}/calculate-price/ # Calculate custom pricing
```

### Booking System
```
GET    /api/v1/bookings/                     # My bookings
POST   /api/v1/bookings/                     # Create booking request
GET    /api/v1/bookings/{id}/                # Booking details
PUT    /api/v1/bookings/{id}/status/         # Update booking status
POST   /api/v1/bookings/{id}/cancel/         # Cancel booking
GET    /api/v1/bookings/{id}/invoice/        # Booking invoice
GET    /api/v1/bookings/guide/pending/       # Pending bookings (guides)
GET    /api/v1/bookings/tourist/upcoming/    # Upcoming tours (tourists)
GET    /api/v1/bookings/calendar/available/  # Guide availability
```

### Reviews & Ratings
```
GET    /api/v1/reviews/tours/{id}/reviews/      # Tour reviews
GET    /api/v1/reviews/guides/{id}/reviews/     # Guide reviews
POST   /api/v1/reviews/bookings/{id}/review/    # Create review
PUT    /api/v1/reviews/{id}/                    # Update review
DELETE /api/v1/reviews/{id}/                    # Delete review
```

### Location Data
```
GET    /api/v1/wilayas/              # List all wilayas
GET    /api/v1/wilayas/{id}/         # Wilaya details
GET    /api/v1/wilayas/{id}/guides/  # Guides in wilaya
GET    /api/v1/wilayas/{id}/tours/   # Tours in wilaya
```

### Messaging System [NEW]
```
GET    /api/v1/messaging/conversations/          # List conversations
POST   /api/v1/messaging/conversations/          # Create conversation
GET    /api/v1/messaging/conversations/{id}/messages/  # Get messages
POST   /api/v1/messaging/conversations/{id}/send_message/  # Send message
POST   /api/v1/messaging/conversations/{id}/mark_read/     # Mark as read
GET    /api/v1/messaging/custom-requests/        # List custom requests
POST   /api/v1/messaging/custom-requests/        # Create custom request
POST   /api/v1/messaging/custom-requests/{id}/respond/    # Guide response
```

### Weather Integration [NEW]
```
GET    /api/v1/tours/{id}/?date=YYYY-MM-DD      # Tour with weather forecast
```

### System Health
```
GET    /api/v1/health/               # Health check
GET    /api/v1/metrics/              # Platform metrics
```

## 💰 Business Rules

### Pricing System (Flexible Tariff Grid)
- **Half-day**: Up to 4 hours
- **Full-day**: 4-8 hours  
- **Extra hours**: Beyond 8 hours (per hour rate)
- Automatic price calculation based on tour duration

### Coverage Zones
- Guides specify covered wilayas
- Tours must be within guide's coverage areas
- Search filters by wilaya

### Booking Workflow
1. Tourist requests booking for specific date/time
2. Booking created with "pending" status
3. Guide has 24 hours to respond (accept/reject/propose alternative)
4. Only confirmed bookings can be reviewed

### Data Validation
- Future booking dates only
- Group size within tour limits
- Reviews only for completed bookings
- Users can only modify their own data

## 🔒 Security Features

- JWT-based authentication with refresh tokens
- Argon2 password hashing
- Rate limiting on authentication endpoints
- Input validation on all endpoints
- File type validation for uploads
- Permission-based access control
- SQL injection prevention (Django ORM)
- XSS protection
- CSRF protection

## 📊 Database Models

### Core Models
- **User**: Custom user model with type field (tourist/guide/admin)
- **Wilaya**: Algerian administrative divisions (58 wilayas)
- **TouristProfile**: Tourist preferences and info
- **GuideProfile**: Guide details, pricing, coverage areas
- **GuideAvailability**: [NEW] Time slot calendar management
- **Tour**: Tour packages with GPS coordinates for weather integration
- **Booking**: Booking system with time slot support
- **Review**: Simplified rating system (1-5 stars)
- **Conversation**: [NEW] Tourist-Guide messaging
- **Message**: [NEW] Messages within conversations  
- **CustomTourRequest**: [NEW] Custom tour request system
- **GuideCertification**: Guide certification documents
- **Tour**: Tour packages with pricing, details, and single image
- **Booking**: Simple booking system
- **Review**: Tourist reviews and ratings

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run tests with coverage:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # HTML report in htmlcov/
```

## 📱 Development

### Adding New Endpoints

1. **Create serializers** in `app_name/serializers.py`
2. **Create views** in `app_name/views.py`  
3. **Add URL patterns** in `app_name/urls.py`
4. **Write tests** in `app_name/tests.py`

### Database Changes

1. **Modify models** in `app_name/models.py`
2. **Create migrations**: `python manage.py makemigrations`
3. **Apply migrations**: `python manage.py migrate`

### Management Commands

Load wilayas data:
```bash
python manage.py load_wilayas
```

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
REDIS_URL=redis://production-redis:6379/0
OPENWEATHER_API_KEY=your-openweather-api-key
```

2. **Database Migration**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py load_wilayas
```

3. **Web Server Configuration**
- Use Gunicorn or uWSGI for WSGI
- Configure Nginx for static files and reverse proxy
- Set up SSL certificates

4. **Monitoring & Logging**
- Configure structured logging
- Set up error monitoring (Sentry)
- Monitor performance metrics

## 📝 API Documentation

Interactive API documentation available at:
- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use Django naming conventions
- Write docstrings for classes and methods
- Add type hints where applicable

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎯 Roadmap

### Phase 1 ✅
- [x] User authentication and profiles
- [x] Basic tour CRUD operations
- [x] Location data (wilayas)
- [x] Guide/Tourist profile management

### Phase 2 ✅ (COMPLETED)
- [x] Complete booking system with guide approval workflow
- [x] Review and rating system with business logic
- [x] Advanced search and filtering
- [x] Weather API integration
- [x] Messaging system
- [x] Time slot management
- [x] Price calculation with group discounts
- [x] Guide dashboard with statistics
- [x] Business rule enforcement (24-hour cancellation, etc.)

### Phase 3 📋 (Future Enhancements)
- [ ] Real-time notifications
- [ ] Payment integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app API optimization
- [ ] Multi-language support
- [ ] Push notifications

---

**Built with ❤️ for Algeria's tourism industry**
