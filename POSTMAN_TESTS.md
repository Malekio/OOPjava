# 🚀 DZ-TourGuide API - Complete Postman Test Collection

## 📋 **SETUP INSTRUCTIONS**

### **Base URL**
```
http://localhost:8000
```

### **Environment Variables (Create in Postman)**
```javascript
// Set these in Postman Environment
base_url: http://localhost:8000
access_token: {{will_be_set_after_login}}
tourist_id: {{will_be_set_after_registration}}
guide_id: {{will_be_set_after_registration}}
tour_id: {{will_be_set_after_tour_creation}}
booking_id: {{will_be_set_after_booking}}
```

---

## 🔥 **TEST FLOW ORDER** (Execute in this sequence)

### **Step 1: Health & Metrics**
### **Step 2: User Registration & Authentication**  
### **Step 3: Profile Management**
### **Step 4: Location Data**
### **Step 5: Tour Management**
### **Step 6: Booking System**
### **Step 7: Review System**

---

## 🩺 **1. HEALTH & METRICS ENDPOINTS**

### **1.1 Health Check**
```http
GET {{base_url}}/v1/health/
```
**Expected Response:**
```json
{
  "status": "healthy",
  "message": "DZ-TourGuide API is running"
}
```

### **1.2 Platform Metrics**
```http
GET {{base_url}}/v1/metrics/
```
**Expected Response:**
```json
{
  "total_users": 0,
  "total_guides": 0,
  "total_tours": 0,
  "total_bookings": 0,
  "completed_bookings": 0
}
```

---

## 🔐 **2. AUTHENTICATION & USER MANAGEMENT**

### **2.1 Register Tourist**
```http
POST {{base_url}}/v1/auth/register/
Content-Type: application/json

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
**Save `user.id` as `tourist_id` from response**

### **2.2 Register Guide**
```http
POST {{base_url}}/v1/auth/register/
Content-Type: application/json

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
**Save `user.id` as `guide_id` from response**

### **2.3 Register Second Tourist**
```http
POST {{base_url}}/v1/auth/register/
Content-Type: application/json

{
  "username": "tourist_john",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1234567890",
  "user_type": "tourist"
}
```

### **2.4 Login as Guide**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "guide_ahmed",
  "password": "SecurePass123!"
}
```
**Save `access` token as `access_token` in environment**

### **2.5 Get Current User Profile**
```http
GET {{base_url}}/v1/auth/me/
Authorization: Bearer {{access_token}}
```

### **2.6 Update User Profile**
```http
PUT {{base_url}}/v1/auth/me/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "email": "ahmed.updated@example.com",
  "first_name": "Ahmed",
  "last_name": "Benali",
  "phone_number": "+213555999888"
}
```

### **2.7 Refresh Token**
```http
POST {{base_url}}/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "{{refresh_token_from_login}}"
}
```

### **2.8 Logout**
```http
POST {{base_url}}/v1/auth/logout/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "refresh": "{{refresh_token_from_login}}"
}
```

---

## 🗺️ **3. LOCATION DATA**

### **3.1 List All Wilayas**
```http
GET {{base_url}}/v1/wilayas/
```

### **3.2 Get Specific Wilaya (Algiers)**
```http
GET {{base_url}}/v1/wilayas/1/
```

### **3.3 Get Guides in Wilaya (will be empty initially)**
```http
GET {{base_url}}/v1/wilayas/1/guides/
```

### **3.4 Get Tours in Wilaya (will be empty initially)**
```http
GET {{base_url}}/v1/wilayas/1/tours/
```

---

## 👤 **4. PROFILE MANAGEMENT**

**Note: Re-login as guide first**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "guide_ahmed",
  "password": "SecurePass123!"
}
```

### **4.1 Get Guide Profile (My Profile)**
```http
GET {{base_url}}/v1/profiles/guides/me/
Authorization: Bearer {{access_token}}
```

### **4.2 Update Guide Profile**
```http
PUT {{base_url}}/v1/profiles/guides/me/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "bio": "Experienced tour guide specializing in Algerian history and culture. Fluent in Arabic, French, and English.",
  "years_of_experience": 5,
  "languages": ["Arabic", "French", "English"],
  "coverage_area_ids": [1, 2, 3],
  "half_day_price": "5000.00",
  "full_day_price": "10000.00", 
  "extra_hour_price": "1500.00"
}
```

### **4.3 List All Guides**
```http
GET {{base_url}}/v1/profiles/guides/
```

### **4.4 Get Specific Guide Details**
```http
GET {{base_url}}/v1/profiles/guides/1/
```

### **4.5 Get Guide Pricing**
```http
GET {{base_url}}/v1/profiles/guides/1/pricing/
```

### **4.6 Add Guide Certification**
```http
POST {{base_url}}/v1/profiles/guides/certifications/
Authorization: Bearer {{access_token}}
Content-Type: multipart/form-data

title: Tourism License
document: [Upload a PDF file]
```

### **4.7 List Guide Certifications**
```http
GET {{base_url}}/v1/profiles/guides/certifications/
Authorization: Bearer {{access_token}}
```

**Now login as tourist:**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "tourist_sara",
  "password": "SecurePass123!"
}
```

### **4.8 Get Tourist Profile**
```http
GET {{base_url}}/v1/profiles/tourists/me/
Authorization: Bearer {{access_token}}
```

### **4.9 Update Tourist Profile**
```http
PUT {{base_url}}/v1/profiles/tourists/me/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "bio": "Travel enthusiast exploring North Africa",
  "date_of_birth": "1990-05-15",
  "nationality": "French",
  "preferred_language": "French"
}
```

---

## 🏛️ **5. TOUR MANAGEMENT**

**Login as guide again:**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "guide_ahmed", 
  "password": "SecurePass123!"
}
```

### **5.1 Create Tour**
```http
POST {{base_url}}/v1/tours/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Historic Casbah of Algiers Walking Tour",
  "description": "Explore the UNESCO World Heritage site of the Casbah, with its narrow streets, Ottoman palaces, and stunning views of the Mediterranean.",
  "wilaya": 1,
  "duration_hours": 4.0,
  "max_group_size": 8,
  "included_services": ["Professional guide", "Historical commentary", "Photo stops", "Traditional tea break"],
  "excluded_services": ["Transportation", "Meals", "Museum entries"],
  "meeting_point": "Place des Martyrs, Algiers",
  "tags": ["history", "culture", "walking", "UNESCO", "architecture"]
}
```
**Save `id` as `tour_id`**

### **5.2 Create Second Tour**
```http
POST {{base_url}}/v1/tours/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Sahara Desert Adventure - Tassili n'Ajjer",
  "description": "Experience the breathtaking landscapes of the Sahara and discover ancient rock art in Tassili n'Ajjer National Park.",
  "wilaya": 33,
  "duration_hours": 8.0,
  "max_group_size": 6,
  "included_services": ["4WD transportation", "Professional guide", "Traditional lunch", "Equipment"],
  "excluded_services": ["Accommodation", "International flights", "Personal insurance"],
  "meeting_point": "Djanet Airport",
  "tags": ["sahara", "desert", "adventure", "rock-art", "nature"]
}
```

### **5.3 List All Tours**
```http
GET {{base_url}}/v1/tours/
```

### **5.4 Search Tours**
```http
GET {{base_url}}/v1/tours/search/?q=casbah
```

### **5.5 Filter Tours by Wilaya**
```http
GET {{base_url}}/v1/tours/?wilaya=1
```

### **5.6 Get My Tours (Guide)**
```http
GET {{base_url}}/v1/tours/me/
Authorization: Bearer {{access_token}}
```

### **5.7 Get Tour Details**
```http
GET {{base_url}}/v1/tours/{{tour_id}}/
```

### **5.8 Update Tour**
```http
PUT {{base_url}}/v1/tours/{{tour_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "title": "Historic Casbah of Algiers - Premium Walking Tour",
  "description": "Updated: Explore the UNESCO World Heritage site with exclusive access to private courtyards and rooftops.",
  "wilaya": 1,
  "duration_hours": 5.0,
  "max_group_size": 6,
  "included_services": ["Professional guide", "Historical commentary", "Private access", "Traditional tea & pastries"],
  "excluded_services": ["Transportation", "Meals", "Personal expenses"],
  "meeting_point": "Place des Martyrs, Algiers",
  "tags": ["history", "culture", "walking", "UNESCO", "premium", "exclusive"]
}
```

### **5.9 Calculate Custom Price**
```http
POST {{base_url}}/v1/tours/{{tour_id}}/calculate-price/
Content-Type: application/json

{
  "duration_hours": 6.5
}
```

---

## 📅 **6. BOOKING SYSTEM**

**Login as tourist:**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "tourist_sara",
  "password": "SecurePass123!"
}
```

### **6.1 Create Booking Request**
```http
POST {{base_url}}/v1/bookings/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "tour": {{tour_id}},
  "booking_date": "2024-12-15",
  "group_size": 2,
  "notes": "Please provide vegetarian options for tea break. One participant has mobility issues."
}
```
**Save `id` as `booking_id`**

### **6.2 Create Second Booking**
```http
POST {{base_url}}/v1/bookings/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "tour": {{tour_id}},
  "booking_date": "2024-12-20",
  "group_size": 4,
  "notes": "Birthday celebration - please suggest photo spots"
}
```

### **6.3 List My Bookings (Tourist)**
```http
GET {{base_url}}/v1/bookings/
Authorization: Bearer {{access_token}}
```

### **6.4 Get Booking Details**
```http
GET {{base_url}}/v1/bookings/{{booking_id}}/
Authorization: Bearer {{access_token}}
```

### **6.5 Update Booking Status**
```http
PUT {{base_url}}/v1/bookings/{{booking_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "status": "confirmed"
}
```

### **6.6 Cancel Booking**
```http
PUT {{base_url}}/v1/bookings/2/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "status": "cancelled"
}
```

---
## Not Yet.
## ⭐ **7. REVIEW SYSTEM**

**First, mark booking as completed (Guide):**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "guide_ahmed",
  "password": "SecurePass123!"
}
```

```http
PUT {{base_url}}/v1/bookings/{{booking_id}}/status/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "status": "completed",
  "guide_notes": "Tour completed successfully! Great group, very engaged with the history."
}
```

**Now login as tourist to review:**
```http
POST {{base_url}}/v1/auth/login/
Content-Type: application/json

{
  "username": "tourist_sara",
  "password": "SecurePass123!"
}
```

### **7.1 Create Review**
```http
POST {{base_url}}/v1/reviews/bookings/{{booking_id}}/review/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "rating": 5,
  "title": "Absolutely Amazing Casbah Experience!",
  "comment": "Ahmed is an exceptional guide with deep knowledge of Algerian history. The Casbah tour exceeded all expectations. He showed us hidden gems and shared fascinating stories about Ottoman architecture. The tea break at a traditional house was magical. Highly recommend!",
  "communication_rating": 5,
  "knowledge_rating": 5,
  "punctuality_rating": 5,
  "value_rating": 5
}
```
**Save `id` as `review_id`**

### **7.2 Get Tour Reviews**
```http
GET {{base_url}}/v1/reviews/tours/{{tour_id}}/reviews/
```

### **7.3 Get Guide Reviews**
```http
GET {{base_url}}/v1/reviews/guides/1/reviews/
```

### **7.4 Update Review**
```http
PUT {{base_url}}/v1/reviews/{{review_id}}/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "rating": 5,
  "title": "Absolutely Amazing Casbah Experience - Updated!",
  "comment": "Updated: Ahmed is an exceptional guide with deep knowledge of Algerian history. The Casbah tour exceeded all expectations. He showed us hidden gems and shared fascinating stories about Ottoman architecture. The tea break at a traditional house was magical. Also appreciated his flexibility with our dietary requirements. Highly recommend!",
  "communication_rating": 5,
  "knowledge_rating": 5,
  "punctuality_rating": 5,
  "value_rating": 5
}
```

### **7.5 Get Review Details**
```http
GET {{base_url}}/v1/reviews/{{review_id}}/
```

---

## 🔧 **8. ADVANCED FILTERING & SEARCH**

### **8.1 Filter Guides by Rating**
```http
GET {{base_url}}/v1/profiles/guides/?min_rating=4.0
```

### **8.2 Filter Guides by Wilaya**
```http
GET {{base_url}}/v1/profiles/guides/?wilaya=1
```

### **8.3 Filter Guides by Language**
```http
GET {{base_url}}/v1/profiles/guides/?language=French
```

### **8.4 Filter Tours by Price Range**
```http
GET {{base_url}}/v1/tours/?max_price=8000
```

### **8.5 Filter Tours by Duration**
```http
GET {{base_url}}/v1/tours/?duration=4
```

### **8.6 Search Tours by Keyword**
```http
GET {{base_url}}/v1/tours/search/?q=desert sahara
```

### **8.7 Complex Tour Search**
```http
GET {{base_url}}/v1/tours/?wilaya=1&max_price=12000&duration__lte=6
```

---

## 📊 **9. FINAL VERIFICATION**

### **9.1 Updated Metrics**
```http
GET {{base_url}}/v1/metrics/
```
**Should show increased counts**

### **9.2 All Wilayas with Guides**
```http
GET {{base_url}}/v1/wilayas/1/guides/
```

### **9.3 All Wilayas with Tours**
```http
GET {{base_url}}/v1/wilayas/1/tours/
```

---

## 🎯 **POSTMAN COLLECTION SETUP**

### **Create Environment with these variables:**
```javascript
{
  "base_url": "http://localhost:8000",
  "access_token": "",
  "refresh_token": "",
  "tourist_id": "",
  "guide_id": "",
  "tour_id": "",
  "booking_id": "",
  "review_id": ""
}
```

### **Pre-request Script for Login endpoints:**
```javascript
// Save tokens from login response
pm.test("Save tokens", function () {
    var jsonData = pm.response.json();
    if (jsonData.access) {
        pm.environment.set("access_token", jsonData.access);
        pm.environment.set("refresh_token", jsonData.refresh);
    }
    if (jsonData.user && jsonData.user.id) {
        if (jsonData.user.user_type === "tourist") {
            pm.environment.set("tourist_id", jsonData.user.id);
        } else if (jsonData.user.user_type === "guide") {
            pm.environment.set("guide_id", jsonData.user.id);
        }
    }
});
```

### **Pre-request Script for Creation endpoints:**
```javascript
// Save IDs from creation responses
pm.test("Save created IDs", function () {
    var jsonData = pm.response.json();
    if (jsonData.id) {
        // Determine what was created based on endpoint
        var url = pm.request.url.toString();
        if (url.includes('/tours/')) {
            pm.environment.set("tour_id", jsonData.id);
        } else if (url.includes('/bookings/')) {
            pm.environment.set("booking_id", jsonData.id);
        } else if (url.includes('/reviews/')) {
            pm.environment.set("review_id", jsonData.id);
        }
    }
});
```

---

## 🚨 **TESTING NOTES**

1. **Execute tests in order** - some endpoints depend on data from previous tests
2. **Save IDs** from responses to use in subsequent tests
3. **Check status codes** - 200/201 for success, 400/401/403/404 for errors
4. **Validate response structure** - ensure all expected fields are present
5. **Test error cases** - try invalid data, unauthorized access, etc.

## 🎉 **SUCCESS CRITERIA**

After running all tests, you should have:
- ✅ 2 registered users (1 tourist, 1 guide)
- ✅ 1 complete guide profile with pricing
- ✅ 2 tours created
- ✅ 2 booking requests (1 confirmed, 1 rejected)
- ✅ 1 review submitted
- ✅ All endpoints returning expected responses

**Total Endpoints Tested: 40+**

This comprehensive test suite covers every single endpoint in your DZ-TourGuide API! 🇩🇿🚀
