# 🚀 DZ-TourGuide - Quick Start Guide

## ⚡ Fast Development Setup (5 minutes)

### 1. **Environment Setup**
```bash
cd /home/malek/projects/TourGuideDZ
source .venv/bin/activate
cd server
```

### 2. **Start Development Server**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 3. **Test API Endpoints**

#### Health Check
```bash
curl http://localhost:8000/api/v1/health/
```

#### Get All Wilayas
```bash
curl http://localhost:8000/api/v1/wilayas/
```

#### Register a Guide
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "guide_ahmed",
    "email": "ahmed@example.com", 
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Ahmed",
    "last_name": "Benali",
    "phone_number": "+213555123456",
    "user_type": "guide"
  }'
```

#### Register a Tourist
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tourist_sara", 
    "email": "sara@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!", 
    "first_name": "Sara",
    "last_name": "Martin",
    "phone_number": "+33123456789",
    "user_type": "tourist"
  }'
```

#### Login and Get Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "guide_ahmed",
    "password": "SecurePass123!"
  }'
```

### 4. **Admin Panel Access**
- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin

### 5. **Database Management**

#### View Database
```bash
python manage.py dbshell
```

#### Create New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Load Sample Data
```bash
python manage.py load_wilayas  # Already loaded
```

## 🔧 **Development Commands**

### Database Operations
```bash
# Reset database (be careful!)
rm db.sqlite3
python manage.py migrate
python manage.py load_wilayas
python manage.py createsuperuser

# Backup database  
cp db.sqlite3 db_backup.sqlite3

# View migrations
python manage.py showmigrations
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test profiles

# Run with verbosity
python manage.py test --verbosity=2
```

### Development Utils
```bash
# Django shell
python manage.py shell

# Check for problems
python manage.py check

# Collect static files
python manage.py collectstatic

# Create sample data (if needed)
python manage.py shell
```

## 📊 **Useful Database Queries**

```python
# In Django shell (python manage.py shell)

from accounts.models import User
from profiles.models import GuideProfile, TouristProfile  
from locations.models import Wilaya
from tours.models import Tour
from bookings.models import Booking

# Check users
User.objects.all()
User.objects.filter(user_type='guide').count()
User.objects.filter(user_type='tourist').count()

# Check wilayas
Wilaya.objects.all().count()  # Should be 58
Wilaya.objects.get(code='16')  # Algiers

# Check profiles
GuideProfile.objects.all().count()
TouristProfile.objects.all().count()
```

## 🌐 **API Testing with Browser**

### Health Check
- http://localhost:8000/api/v1/health/

### Wilayas List
- http://localhost:8000/api/v1/wilayas/

### Specific Wilaya (Algiers)
- http://localhost:8000/api/v1/wilayas/16/

### Platform Metrics
- http://localhost:8000/api/v1/metrics/

## 🔍 **Debugging Tips**

### Check Server Logs
```bash
tail -f logs/django.log
```

### Django Debug Toolbar (if needed)
```bash
pip install django-debug-toolbar
# Add to INSTALLED_APPS and MIDDLEWARE in settings.py
```

### Check Database Connection
```bash
python manage.py dbshell
.tables  # SQLite command to list tables
```

### Validate Models
```bash
python manage.py check
python manage.py makemigrations --dry-run
```

## 🚨 **Common Issues & Solutions**

### "ModuleNotFoundError" 
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
pip install -r requirements.txt
```

### "CSRF verification failed"
```bash
# For API calls, use proper headers or disable CSRF for API endpoints
# Already configured in settings.py
```

### "Permission denied" 
```bash
# Check user permissions in views
# Use proper authentication headers:
# Authorization: Bearer <jwt_token>
```

### Database locked (SQLite)
```bash
# Stop server and restart
# Or switch to PostgreSQL for production
```

## 🎯 **Development Workflow**

1. **Start development server**: `python manage.py runserver`
2. **Make code changes** in your preferred editor
3. **Test changes** using browser or curl
4. **Run tests**: `python manage.py test`
5. **Create migrations** if model changes: `python manage.py makemigrations`
6. **Apply migrations**: `python manage.py migrate`
7. **Commit changes** to git

## 📝 **Next Development Steps**

1. **Complete booking workflow logic**
2. **Implement tour search filters**  
3. **Add real-time notifications**
4. **Create admin dashboard**
5. **Write comprehensive tests**
6. **Add API documentation**

---

**Happy coding! 🚀 The foundation is solid - now build amazing features on top of it!**
