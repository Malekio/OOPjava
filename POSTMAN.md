# 🚀 DZ-TourGuide API - Complete POSTMAN Collection

**Base URL:** `{{base_url}}` (Set to `http://localhost:8000` in Postman environment)

## 🔧 Environment Variables Setup

Create these variables in your Postman environment:
- `base_url`: `http://localhost:8000`
- `access_token`: (Will be set after login)
- `refresh_token`: (Will be set after login)
- `tourist_id`: (Will be set after tourist registration)
- `guide_id`: (Will be set after guide registration)
- `tour_id`: (Will be set after tour creation)
- `booking_id`: (Will be set after booking creation)
- `review_id`: (Will be set after review creation)
- `conversation_id`: (Will be set after conversation creation)

---

## 🩺 1. HEALTH & METRICS ENDPOINTS

### 1.1 Health Check
**Method:** `GET`  
**URL:** `{{base_url}}/v1/health/`  
**Authorization:** None  
**Body:** None

### 1.2 Platform Metrics
**Method:** `GET`  
**URL:** `{{base_url}}/v1/metrics/` 
**Authorization:** None  
**Body:** None

---

## 🔐 2. AUTHENTICATION ENDPOINTS (`/v1/auth/`)

### 2.1 Register Tourist
**Method:** `POST`  
**URL:** `{{base_url}}/v1/auth/register/`  
**Authorization:** None  
**Body (JSON):**
```json
{
  "username": "tourist_sara",
  "email": "sara@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Sara",
  "last_name": "Martin",
  "phone_number": "+33123456789",
  "user_type": "tourist"
}
```

### 2.2 Register Guide
**Method:** `POST`  
**URL:** `{{base_url}}/v1/auth/register/`  
**Authorization:** None  
**Body (JSON):**
```json
{
  "username": "guide_ahmed",
  "email": "ahmed@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Ahmed",
  "last_name": "Benali",
  "phone_number": "+213555123456",
  "user_type": "guide"
}
```

### 2.3 Login (Get Tokens)
**Method:** `POST`  
**URL:** `{{base_url}}/v1/auth/login/`  
**Authorization:** None  
**Body (JSON):**
```json
{
  "username": "guide_ahmed",
  "password": "SecurePass123!"
}
```
**Note:** Save `access` token to `access_token` variable and `refresh` token to `refresh_token` variable

### 2.4 Refresh Token
**Method:** `POST`  
**URL:** `{{base_url}}/v1/auth/refresh/`  
**Authorization:** None  
**Body (JSON):**
```json
{
  "refresh": "{{refresh_token}}"
}
```

### 2.5 Logout
**Method:** `POST`  
**URL:** `{{base_url}}/v1/auth/logout/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "refresh": "{{refresh_token}}"
}
```

### 2.6 Get Current User Profile
**Method:** `GET`  
**URL:** `{{base_url}}/v1/auth/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 2.7 Update Current User Profile
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/auth/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "first_name": "Ahmed Updated",
  "last_name": "Benali Updated",
  "phone_number": "+213555999888"
}
```

---

## 👤 3. PROFILES ENDPOINTS (`/v1/profiles/`)

### 3.1 List All Guides
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/`  
**Authorization:** None  
**Body:** None

### 3.2 Get Specific Guide Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/1/`  
**Authorization:** None  
**Body:** None

### 3.3 Get My Guide Profile
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 3.4 Update My Guide Profile
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/profiles/guides/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "bio": "Experienced tour guide specializing in Algerian history and culture. I have been guiding tourists through the beautiful landscapes and rich heritage of Algeria for over 5 years. Fluent in Arabic, French, and English.",
  "years_of_experience": 5,
  "languages": ["Arabic", "French", "English"],
  "coverage_area_ids": [1, 2, 3],
  "half_day_price": "5000.00",
  "full_day_price": "10000.00",
  "extra_hour_price": "1500.00"
}
```

### 3.5 Get Guide Pricing Structure
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/1/pricing/`  
**Authorization:** None  
**Body:** None

### 3.6 Add Guide Certification
**Method:** `POST`  
**URL:** `{{base_url}}/v1/profiles/guides/certifications/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (Form-Data):**
- `title`: "Professional Tour Guide License"
- `document`: [Upload file]

### 3.7 List My Certifications
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/certifications/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 3.8 Get Certification Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/guides/certifications/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 3.9 Update Certification
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/profiles/guides/certifications/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (Form-Data):**
- `title`: "Updated Professional Tour Guide License"
- `document`: [Upload new file]

### 3.10 Delete Certification
**Method:** `DELETE`  
**URL:** `{{base_url}}/v1/profiles/guides/certifications/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 3.11 Get My Tourist Profile
**Method:** `GET`  
**URL:** `{{base_url}}/v1/profiles/tourists/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 3.12 Update My Tourist Profile
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/profiles/tourists/me/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "bio": "Travel enthusiast exploring the beautiful countries of North Africa. Particularly interested in history, culture, and traditional cuisine.",
  "date_of_birth": "1990-05-15",
  "nationality": "French",
  "preferred_language": "French"
}
```

---

## 🏛️ 4. TOURS ENDPOINTS (`/v1/tours/`)

### 4.1 List All Tours
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/`  
**Authorization:** None  
**Body:** None

### 4.2 List Tours with Filters
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/?location=1&min_price=50&max_price=200&ordering=-created_at`  
**Authorization:** None  
**Body:** None

### 4.3 Create New Tour
**Method:** `POST`  
**URL:** `{{base_url}}/v1/tours/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body (JSON):**
```json
{
  "title": "Historic Casbah of Algiers Walking Tour",
  "description": "Explore the UNESCO World Heritage site of the Casbah, with its narrow winding streets, Ottoman palaces, traditional houses, and stunning views of the Mediterranean Sea. Discover the rich history spanning over a millennium.",
  "wilaya": 1,
  "duration_hours": 4.0,
  "max_group_size": 8,
  "included_services": ["Professional guide", "Historical commentary", "Photo stops", "Traditional tea break", "Map and brochure"],
  "excluded_services": ["Transportation to meeting point", "Meals", "Museum entries", "Personal expenses"],
  "meeting_point": "Place des Martyrs, Algiers City Center",
  "latitude": 36.7763,
  "longitude": 3.0586,
  "tags": ["history", "culture", "walking", "UNESCO", "architecture", "Ottoman"]
}
```

### 4.4 Get Tour Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/1/`  
**Authorization:** None  
**Body:** None

### 4.5 Get Tour Details with Weather
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/1/?date=2024-02-15`  
**Authorization:** None  
**Body:** None

### 4.6 Update Tour
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/tours/1/`  
**Authorization:** `Bearer {{access_token}}` (Tour owner only)  
**Body (JSON):**
```json
{
  "title": "Historic Casbah of Algiers - Premium Walking Tour",
  "description": "UPDATED: Explore the UNESCO World Heritage site with exclusive access to private courtyards and rooftop terraces. Includes visits to traditional craft workshops and authentic tea ceremony.",
  "wilaya": 1,
  "duration_hours": 5.0,
  "max_group_size": 6,
  "included_services": ["Professional guide", "Historical commentary", "Private courtyard access", "Traditional tea & pastries", "Craft workshop visit"],
  "excluded_services": ["Transportation to meeting point", "Personal purchases", "Additional meals"],
  "meeting_point": "Place des Martyrs, Algiers City Center",
  "latitude": 36.7763,
  "longitude": 3.0586,
  "tags": ["history", "culture", "walking", "UNESCO", "premium", "exclusive", "crafts"]
}
```

### 4.7 Delete Tour
**Method:** `DELETE`  
**URL:** `{{base_url}}/v1/tours/1/`  
**Authorization:** `Bearer {{access_token}}` (Tour owner only)  
**Body:** None

### 4.8 Search Tours
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/search/?q=casbah`  
**Authorization:** None  
**Body:** None

### 4.9 Advanced Tour Search
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/search/?q=casbah&min_price=50&max_price=200`  
**Authorization:** None  
**Body:** None

### 4.10 Get My Tours (Guide)
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/me/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body:** None

### 4.11 Calculate Tour Price with Group Size
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/1/calculate-price/?group_size=8`  
**Authorization:** None  
**Body:** None

### 4.12 Popular Tours (Function-based view - URL missing)
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/popular/` ⚠️ **URL NOT DEFINED YET**  
**Authorization:** None  
**Body:** None

### 4.13 Guide Dashboard (Function-based view - URL missing)
**Method:** `GET`  
**URL:** `{{base_url}}/v1/tours/guide/dashboard/` ⚠️ **URL NOT DEFINED YET**  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body:** None

---

## 📅 5. BOOKINGS ENDPOINTS (`/v1/bookings/`)

### 5.1 List My Bookings
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 5.2 Create Booking Request
**Method:** `POST`  
**URL:** `{{base_url}}/v1/bookings/`  
**Authorization:** `Bearer {{access_token}}` (Tourist only)  
**Body (JSON):**
```json
{
  "tour": 1,
  "booking_date": "2024-03-15",
  "time_slot": "morning",
  "group_size": 4,
  "notes": "We are particularly interested in the Ottoman architecture and would love to visit some traditional craft workshops if possible."
}
```

### 5.3 Get Booking Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 5.4 Update Booking Status (Guide Approval/Rejection)
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/bookings/1/status/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body (JSON) - Approve:**
```json
{
  "status": "confirmed",
  "guide_notes": "Looking forward to showing you the beautiful sites of Algiers! I've arranged special access to some private courtyards."
}
```
**Body (JSON) - Reject:**
```json
{
  "status": "rejected",
  "guide_notes": "Unfortunately, I'm not available on this date. Please check my availability calendar for alternative dates."
}
```

### 5.5 Cancel Booking
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/bookings/1/cancel/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "cancellation_reason": "Change of travel plans due to work commitments"
}
```

### 5.6 Get Booking Invoice
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/1/invoice/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 5.7 Guide Pending Bookings
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/guide/pending/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body:** None

### 5.8 Tourist Upcoming Bookings
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/tourist/upcoming/`  
**Authorization:** `Bearer {{access_token}}` (Tourist only)  
**Body:** None

### 5.9 Guide Availability Calendar
**Method:** `GET`  
**URL:** `{{base_url}}/v1/bookings/calendar/available/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body:** None

---

## ⭐ 6. REVIEWS ENDPOINTS (`/v1/reviews/`)

### 6.1 Get Tour Reviews
**Method:** `GET`  
**URL:** `{{base_url}}/v1/reviews/tours/1/reviews/`  
**Authorization:** None  
**Body:** None

### 6.2 Get Guide Reviews
**Method:** `GET`  
**URL:** `{{base_url}}/v1/reviews/guides/1/reviews/`  
**Authorization:** None  
**Body:** None

### 6.3 Create Review for Completed Booking
**Method:** `POST`  
**URL:** `{{base_url}}/v1/reviews/bookings/1/review/`  
**Authorization:** `Bearer {{access_token}}` (Tourist only)  
**Body (JSON):**
```json
{
  "rating": 5,
  "title": "Amazing experience in the Casbah!",
  "comment": "Ahmed was incredibly knowledgeable about the history and showed us hidden gems. Highly recommend this tour for anyone visiting Algiers!"
}
```

### 6.4 Get Review Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/reviews/1/`  
**Authorization:** None  
**Body:** None

### 6.5 Update My Review
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/reviews/1/`  
**Authorization:** `Bearer {{access_token}}` (Review owner only)  
**Body (JSON):**
```json
{
  "rating": 5,
  "title": "Updated: Amazing experience in the Casbah!",
  "comment": "Updated review: Ahmed was incredibly knowledgeable about the history and showed us hidden gems. The traditional tea break was a perfect touch. Highly recommend this tour for anyone visiting Algiers!"
}
```

### 6.6 Delete My Review
**Method:** `DELETE`  
**URL:** `{{base_url}}/v1/reviews/1/`  
**Authorization:** `Bearer {{access_token}}` (Review owner only)  
**Body:** None

### 6.7 Guide Respond to Review (Function-based view - URL missing)
**Method:** `POST`  
**URL:** `{{base_url}}/v1/reviews/1/guide-response/` ⚠️ **URL NOT DEFINED YET**  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body (JSON):**
```json
{
  "guide_response": "Thank you Sara for the wonderful review! It was my pleasure to share the rich history of our beautiful Casbah with you. Hope to see you again in Algeria!"
}
```

### 6.8 Review Statistics for Guide (Function-based view - URL missing)
**Method:** `GET`  
**URL:** `{{base_url}}/v1/reviews/guides/1/statistics/` ⚠️ **URL NOT DEFINED YET**  
**Authorization:** None  
**Body:** None

---

## 🗺️ 7. LOCATIONS ENDPOINTS (`/v1/wilayas/`)

### 7.1 List All Wilayas
**Method:** `GET`  
**URL:** `{{base_url}}/v1/wilayas/`  
**Authorization:** None  
**Body:** None

### 7.2 Get Wilaya Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/wilayas/1/`  
**Authorization:** None  
**Body:** None

### 7.3 Get Guides in Wilaya
**Method:** `GET`  
**URL:** `{{base_url}}/v1/wilayas/1/guides/`  
**Authorization:** None  
**Body:** None

### 7.4 Get Tours in Wilaya
**Method:** `GET`  
**URL:** `{{base_url}}/v1/wilayas/1/tours/`  
**Authorization:** None  
**Body:** None

---

## 💬 8. MESSAGING ENDPOINTS (`/v1/messaging/`)

### 8.1 List My Conversations
**Method:** `GET`  
**URL:** `{{base_url}}/v1/messaging/conversations/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.2 Create/Get Conversation
**Method:** `POST`  
**URL:** `{{base_url}}/v1/messaging/conversations/`  
**Authorization:** `Bearer {{access_token}}` (Tourist only)  
**Body (JSON):**
```json
{
  "guide_id": 1
}
```

### 8.3 Get Conversation Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.4 Update Conversation
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "title": "Updated Conversation Title"
}
```

### 8.5 Delete Conversation
**Method:** `DELETE`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.6 Get Messages in Conversation
**Method:** `GET`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/messages/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.7 Send Message
**Method:** `POST`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/send_message/`  
**Authorization:** `Bearer {{access_token}}`  
**Body (JSON):**
```json
{
  "content": "Hello! I'm interested in booking your Casbah tour. Do you have availability for next weekend?"
}
```

### 8.8 Mark Messages as Read
**Method:** `POST`  
**URL:** `{{base_url}}/v1/messaging/conversations/1/mark_read/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.9 List Custom Tour Requests
**Method:** `GET`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.10 Create Custom Tour Request
**Method:** `POST`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/`  
**Authorization:** `Bearer {{access_token}}` (Tourist only)  
**Body (JSON):**
```json
{
  "guide": 1,
  "title": "Photography Tour of Algiers",
  "description": "I'm a professional photographer looking for a guided tour that focuses on the most photogenic spots in Algiers, including sunrise/sunset locations, architectural details, and street photography opportunities.",
  "preferred_date": "2024-03-20",
  "duration_hours": 6,
  "group_size": 2,
  "budget": "150.00",
  "special_requirements": "Early morning start (6 AM) for golden hour photography. Need access to elevated viewpoints."
}
```

### 8.11 Get Custom Tour Request Details
**Method:** `GET`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/1/`  
**Authorization:** `Bearer {{access_token}}`  
**Body:** None

### 8.12 Update Custom Tour Request
**Method:** `PUT`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/1/`  
**Authorization:** `Bearer {{access_token}}` (Request owner only)  
**Body (JSON):**
```json
{
  "title": "Updated Photography Tour of Algiers",
  "description": "Updated description with more specific requirements...",
  "preferred_date": "2024-03-22",
  "duration_hours": 8,
  "group_size": 2,
  "budget": "180.00"
}
```

### 8.13 Delete Custom Tour Request
**Method:** `DELETE`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/1/`  
**Authorization:** `Bearer {{access_token}}` (Request owner only)  
**Body:** None

### 8.14 Guide Respond to Custom Tour Request
**Method:** `POST`  
**URL:** `{{base_url}}/v1/messaging/custom-requests/1/respond/`  
**Authorization:** `Bearer {{access_token}}` (Guide only)  
**Body (JSON) - Accept:**
```json
{
  "action": "accept",
  "proposed_price": "180.00",
  "alternative_date": "2024-03-22",
  "guide_response": "I'd love to do this photography tour! I know all the best spots and can arrange early access to some locations."
}
```
**Body (JSON) - Reject:**
```json
{
  "action": "reject",
  "guide_response": "Thank you for your interest, but I'm not available on those dates. Please check my regular tours."
}
```

---

## ⚠️ MISSING URL ENDPOINTS

The following endpoints exist as views but don't have URL patterns defined yet:

1. **Popular Tours:**
   - Function: `popular_tours` in `tours/views.py`
   - Missing URL: `path('popular/', views.popular_tours, name='popular-tours')`

2. **Guide Dashboard:**
   - Function: `guide_dashboard` in `tours/views.py`
   - Missing URL: `path('guide/dashboard/', views.guide_dashboard, name='guide-dashboard')`

3. **Guide Respond to Review:**
   - Function: `guide_respond_to_review` in `reviews/views.py`
   - Missing URL: `path('<int:review_id>/guide-response/', views.guide_respond_to_review, name='guide-respond-review')`

4. **Review Statistics:**
   - Function: `review_statistics` in `reviews/views.py`
   - Missing URL: `path('guides/<int:guide_id>/statistics/', views.review_statistics, name='review-statistics')`

---

## 📝 Testing Notes

1. **Authentication Flow:**
   - Register → Login → Save tokens → Use Bearer token for authenticated endpoints

2. **Role-based Access:**
   - Some endpoints are role-specific (Tourist/Guide only)
   - Test with appropriate user type tokens

3. **Data Dependencies:**
   - Create wilayas → Register users → Create profiles → Create tours → Create bookings → Create reviews

4. **File Uploads:**
   - Use form-data for certification uploads
   - Include proper file types (PDF, JPG, PNG)

5. **Query Parameters:**
   - Many endpoints support filtering via query parameters
   - Test different combinations for comprehensive coverage

**Total Endpoints:** 60+ (58 implemented + 4 missing URLs)

🎯 **All endpoints are documented with exact methods, URLs, authorization requirements, and request bodies for comprehensive API testing in Postman!**
