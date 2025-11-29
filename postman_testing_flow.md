# 🧪 DZ-TourGuide API - Complete Testing Flow Guide

This guide provides the **optimal testing sequence** to ensure proper data setup and dependency management for comprehensive API testing.

## 🎯 Pre-Testing Setup

### 1. Environment Setup
- ✅ Import both JSON files to Postman
- ✅ Select "🇩🇿 DZ-TourGuide Environment"
- ✅ Verify `base_url` = `http://localhost:8000`
- ✅ Start Django server: `python manage.py runserver`

---

## 📋 Phase 1: System Health & Foundation (No Dependencies)

### 1.1 Health Checks
```
🩺 Health Check
   GET {{base_url}}/v1/health/
   ✅ Expected: 200 OK, "status": "healthy"

🩺 Platform Metrics  
   GET {{base_url}}/v1/metrics/
   ✅ Expected: 200 OK, platform statistics
```

### 1.2 Location Data
```
🗺️ List All Wilayas
   GET {{base_url}}/v1/wilayas/
   ✅ Expected: 200 OK, list of Algerian wilayas
   📝 Note: Save a wilaya ID for later use

🗺️ Get Wilaya Details
   GET {{base_url}}/v1/wilayas/1/
   ✅ Expected: 200 OK, wilaya details (Adrar)
```

---

## 📋 Phase 2: User Registration & Authentication

### 2.1 User Registration (Create Test Accounts)
```
🔐 Register Tourist
   POST {{base_url}}/v1/auth/register/
   ✅ Expected: 201 Created
   📝 Save: user.id to tourist_id variable
   
🔐 Register Guide  
   POST {{base_url}}/v1/auth/register/
   ✅ Expected: 201 Created
   📝 Save: user.id to guide_id variable
```

### 2.2 Authentication Flow
```
🔐 Login (Tourist)
   POST {{base_url}}/v1/auth/login/
   ✅ Expected: 200 OK
   📝 Save: access token, refresh token
   
🔐 Get Current User Profile
   GET {{base_url}}/v1/auth/me/
   ✅ Expected: 200 OK, tourist profile data

🔐 Update Current User Profile
   PUT {{base_url}}/v1/auth/me/
   ✅ Expected: 200 OK, updated profile

🔐 Refresh Token
   POST {{base_url}}/v1/auth/refresh/
   ✅ Expected: 200 OK, new access token
```

---

## 📋 Phase 3: Profile Creation & Management

### 3.1 Tourist Profile Setup
```
👤 Get My Tourist Profile
   GET {{base_url}}/v1/profiles/tourists/me/
   ✅ Expected: 200 OK

👤 Update My Tourist Profile
   PUT {{base_url}}/v1/profiles/tourists/me/
   ✅ Expected: 200 OK, updated tourist profile
```

### 3.2 Guide Profile Setup (Switch to Guide Token)
```
🔐 Login (Guide) - Switch User
   POST {{base_url}}/v1/auth/login/
   📝 Use guide credentials, save new tokens

👤 Get My Guide Profile  
   GET {{base_url}}/v1/profiles/guides/me/
   ✅ Expected: 200 OK

👤 Update My Guide Profile
   PUT {{base_url}}/v1/profiles/guides/me/
   ✅ Expected: 200 OK, updated guide profile
   
👤 Get Guide Pricing Structure
   GET {{base_url}}/v1/profiles/guides/1/pricing/
   ✅ Expected: 200 OK, pricing details
```

### 3.3 Guide Certifications
```
👤 Add Guide Certification
   POST {{base_url}}/v1/profiles/guides/certifications/
   ✅ Expected: 201 Created
   📝 Save: certification ID

👤 List My Certifications
   GET {{base_url}}/v1/profiles/guides/certifications/
   ✅ Expected: 200 OK, list of certifications

👤 Get Certification Details
   GET {{base_url}}/v1/profiles/guides/certifications/1/
   ✅ Expected: 200 OK

👤 Update Certification
   PUT {{base_url}}/v1/profiles/guides/certifications/1/
   ✅ Expected: 200 OK

👤 Delete Certification
   DELETE {{base_url}}/v1/profiles/guides/certifications/1/
   ✅ Expected: 204 No Content
```

### 3.4 Public Profile Views
```
👤 List All Guides
   GET {{base_url}}/v1/profiles/guides/
   ✅ Expected: 200 OK, paginated guide list

👤 Get Specific Guide Details
   GET {{base_url}}/v1/profiles/guides/1/
   ✅ Expected: 200 OK, public guide profile
```

---

## 📋 Phase 4: Tours Management

### 4.1 Tour Creation (Guide Authentication Required)
```
🏛️ Create New Tour
   POST {{base_url}}/v1/tours/
   ✅ Expected: 201 Created
   📝 Save: tour.id to tour_id variable

🏛️ Get Tour Details
   GET {{base_url}}/v1/tours/1/
   ✅ Expected: 200 OK, full tour details

🏛️ Get Tour Details with Weather
   GET {{base_url}}/v1/tours/1/?date=2024-12-05
   ✅ Expected: 200 OK, tour + weather forecast
   📝 Note: Date must be within 5 days
```

### 4.2 Tour Management
```
🏛️ Update Tour
   PUT {{base_url}}/v1/tours/1/
   ✅ Expected: 200 OK, updated tour

🏛️ Get My Tours (Guide)
   GET {{base_url}}/v1/tours/me/
   ✅ Expected: 200 OK, guide's tours list
```

### 4.3 Tour Discovery & Search
```
🏛️ List All Tours
   GET {{base_url}}/v1/tours/
   ✅ Expected: 200 OK, paginated tours

🏛️ List Tours with Filters
   GET {{base_url}}/v1/tours/?wilaya=1&min_price=50&max_price=200
   ✅ Expected: 200 OK, filtered results

🏛️ Search Tours
   GET {{base_url}}/v1/tours/search/?q=casbah
   ✅ Expected: 200 OK, search results

🏛️ Advanced Tour Search
   GET {{base_url}}/v1/tours/search/?q=casbah&min_price=50
   ✅ Expected: 200 OK, advanced search

🏛️ Calculate Tour Price with Group Size
   GET {{base_url}}/v1/tours/1/calculate-price/?group_size=8
   ✅ Expected: 200 OK, calculated pricing
```

### 4.4 Location-Based Tour Discovery
```
🗺️ Get Guides in Wilaya
   GET {{base_url}}/v1/wilayas/1/guides/
   ✅ Expected: 200 OK, guides in Adrar

🗺️ Get Tours in Wilaya
   GET {{base_url}}/v1/wilayas/1/tours/
   ✅ Expected: 200 OK, tours in Adrar
```

---

## 📋 Phase 5: Booking Workflow

### 5.1 Tourist Booking Process (Switch to Tourist Token)
```
🔐 Login (Tourist) - Switch Back
   POST {{base_url}}/v1/auth/login/
   📝 Use tourist credentials, save tokens

📅 Create Booking Request
   POST {{base_url}}/v1/bookings/
   ✅ Expected: 201 Created
   📝 Save: booking.id to booking_id variable

📅 Get Booking Details
   GET {{base_url}}/v1/bookings/1/
   ✅ Expected: 200 OK, booking details

📅 List My Bookings
   GET {{base_url}}/v1/bookings/
   ✅ Expected: 200 OK, tourist's bookings
   
📅 Tourist Upcoming Bookings
   GET {{base_url}}/v1/bookings/tourist/upcoming/
   ✅ Expected: 200 OK, upcoming bookings
```

### 5.2 Guide Booking Management (Switch to Guide Token)
```
🔐 Login (Guide) - Switch to Guide
   POST {{base_url}}/v1/auth/login/
   📝 Use guide credentials

📅 Guide Pending Bookings
   GET {{base_url}}/v1/bookings/guide/pending/
   ✅ Expected: 200 OK, pending approvals

📅 Update Booking Status (Approve)
   PUT {{base_url}}/v1/bookings/1/status/
   ✅ Expected: 200 OK, booking confirmed
   📝 Body: {"status": "confirmed", "guide_notes": "..."}

📅 Update Booking Status (Reject) - Create Another Booking First
   PUT {{base_url}}/v1/bookings/2/status/
   ✅ Expected: 200 OK, booking rejected
   📝 Body: {"status": "rejected", "guide_notes": "..."}
```

### 5.3 Booking Operations
```
📅 Get Booking Invoice
   GET {{base_url}}/v1/bookings/1/invoice/
   ✅ Expected: 200 OK, invoice details

📅 Cancel Booking
   PUT {{base_url}}/v1/bookings/1/cancel/
   ✅ Expected: 200 OK, booking cancelled
   📝 Note: Only within 24-hour policy

📅 Guide Availability Calendar
   GET {{base_url}}/v1/bookings/calendar/available/
   ✅ Expected: 200 OK, availability data
```

---

## 📋 Phase 6: Reviews & Ratings

### 6.1 Review Creation (Tourist - After Completing Booking)
```
🔐 Login (Tourist) - Switch Back
   POST {{base_url}}/v1/auth/login/

⭐ Create Review for Completed Booking
   POST {{base_url}}/v1/reviews/bookings/1/review/
   ✅ Expected: 201 Created
   📝 Save: review.id to review_id variable
   📝 Note: Only works for completed bookings
```

### 6.2 Review Management
```
⭐ Get Review Details
   GET {{base_url}}/v1/reviews/1/
   ✅ Expected: 200 OK

⭐ Update My Review
   PUT {{base_url}}/v1/reviews/1/
   ✅ Expected: 200 OK, updated review

⭐ Get Tour Reviews
   GET {{base_url}}/v1/reviews/tours/1/reviews/
   ✅ Expected: 200 OK, all tour reviews

⭐ Get Guide Reviews
   GET {{base_url}}/v1/reviews/guides/1/reviews/
   ✅ Expected: 200 OK, all guide reviews
```

### 6.3 Guide Review Response (Switch to Guide)
```
🔐 Login (Guide) - Switch to Guide
   POST {{base_url}}/v1/auth/login/

⚠️ MISSING ENDPOINTS (Need URL patterns):
⭐ Guide Respond to Review
   POST {{base_url}}/v1/reviews/1/guide-response/
   ❌ URL pattern not defined yet

⭐ Review Statistics for Guide
   GET {{base_url}}/v1/reviews/guides/1/statistics/
   ❌ URL pattern not defined yet
```

---

## 📋 Phase 7: Messaging System

### 7.1 Conversation Management (Tourist)
```
🔐 Login (Tourist) - Switch Back
   POST {{base_url}}/v1/auth/login/

💬 Create/Get Conversation
   POST {{base_url}}/v1/messaging/conversations/
   ✅ Expected: 201 Created
   📝 Save: conversation.id

💬 List My Conversations
   GET {{base_url}}/v1/messaging/conversations/
   ✅ Expected: 200 OK

💬 Get Conversation Details
   GET {{base_url}}/v1/messaging/conversations/1/
   ✅ Expected: 200 OK
```

### 7.2 Messaging Flow
```
💬 Send Message
   POST {{base_url}}/v1/messaging/conversations/1/send_message/
   ✅ Expected: 201 Created

💬 Get Messages in Conversation
   GET {{base_url}}/v1/messaging/conversations/1/messages/
   ✅ Expected: 200 OK, message history

💬 Mark Messages as Read
   POST {{base_url}}/v1/messaging/conversations/1/mark_read/
   ✅ Expected: 200 OK
```

### 7.3 Custom Tour Requests
```
💬 Create Custom Tour Request
   POST {{base_url}}/v1/messaging/custom-requests/
   ✅ Expected: 201 Created
   📝 Save: request ID

💬 List Custom Tour Requests
   GET {{base_url}}/v1/messaging/custom-requests/
   ✅ Expected: 200 OK

💬 Get Custom Tour Request Details
   GET {{base_url}}/v1/messaging/custom-requests/1/
   ✅ Expected: 200 OK

💬 Update Custom Tour Request
   PUT {{base_url}}/v1/messaging/custom-requests/1/
   ✅ Expected: 200 OK
```

### 7.4 Guide Response to Custom Requests (Switch to Guide)
```
🔐 Login (Guide) - Switch to Guide
   POST {{base_url}}/v1/auth/login/

💬 Guide Respond to Custom Tour Request (Accept)
   POST {{base_url}}/v1/messaging/custom-requests/1/respond/
   ✅ Expected: 200 OK
   📝 Body: {"action": "accept", "proposed_price": "180.00", ...}

💬 Guide Respond to Custom Tour Request (Reject)
   POST {{base_url}}/v1/messaging/custom-requests/2/respond/
   ✅ Expected: 200 OK
   📝 Body: {"action": "reject", "guide_response": "..."}
```

### 7.5 Conversation Management
```
💬 Update Conversation
   PUT {{base_url}}/v1/messaging/conversations/1/
   ✅ Expected: 200 OK

💬 Delete Conversation
   DELETE {{base_url}}/v1/messaging/conversations/1/
   ✅ Expected: 204 No Content

💬 Delete Custom Tour Request
   DELETE {{base_url}}/v1/messaging/custom-requests/1/
   ✅ Expected: 204 No Content
```

---

## 📋 Phase 8: Advanced Features & Analytics

### 8.1 Missing Endpoints (Need URL Implementation)
```
⚠️ ENDPOINTS REQUIRING URL PATTERNS:

🏛️ Popular Tours
   GET {{base_url}}/v1/tours/popular/
   ❌ Missing URL: path('popular/', views.popular_tours)

🏛️ Guide Dashboard  
   GET {{base_url}}/v1/tours/guide/dashboard/
   ❌ Missing URL: path('guide/dashboard/', views.guide_dashboard)

⭐ Guide Respond to Review
   POST {{base_url}}/v1/reviews/1/guide-response/
   ❌ Missing URL: path('<int:review_id>/guide-response/', views.guide_respond_to_review)

⭐ Review Statistics
   GET {{base_url}}/v1/reviews/guides/1/statistics/
   ❌ Missing URL: path('guides/<int:guide_id>/statistics/', views.review_statistics)
```

---

## 📋 Phase 9: Cleanup & Deletion Tests

### 9.1 Destructive Operations (Test Last)
```
⭐ Delete My Review
   DELETE {{base_url}}/v1/reviews/1/
   ✅ Expected: 204 No Content

🏛️ Delete Tour
   DELETE {{base_url}}/v1/tours/1/
   ✅ Expected: 204 No Content
   📝 Note: Only if no active bookings

🔐 Logout
   POST {{base_url}}/v1/auth/logout/
   ✅ Expected: 200 OK
```

---

## 🎯 Testing Summary

### ✅ **Total Endpoints to Test: 62**
- **Implemented & Working**: 58 endpoints
- **Missing URL Patterns**: 4 endpoints

### 📊 **Testing Categories:**
1. **Health & Metrics**: 2 endpoints
2. **Authentication**: 7 endpoints  
3. **Profiles**: 12 endpoints
4. **Tours**: 13 endpoints
5. **Bookings**: 9 endpoints
6. **Reviews**: 8 endpoints
7. **Locations**: 4 endpoints
8. **Messaging**: 14 endpoints

### 🔧 **Common Issues to Watch For:**
1. **Token Expiration**: Refresh tokens when needed
2. **Role Permissions**: Switch between tourist/guide tokens
3. **Data Dependencies**: Follow the sequence (user → profile → tour → booking → review)
4. **Missing URLs**: 4 endpoints need URL patterns added
5. **File Uploads**: Use form-data for certification uploads

### 🚀 **Quick Full Test:**
Run the entire collection in Postman using "Run collection" for automated testing of all endpoints in sequence!

---

**🎉 Happy Testing! This flow ensures comprehensive API coverage with proper data setup and dependency management.**