# 🔥 DZ-TourGuide API - EXACT JSON TEST DATA FOR EVERY ENDPOINT

**Base URL:** `http://localhost:8000`
**Updated Features:** ✅ Weather API Integration | ✅ Messaging System | ✅ Advanced Calendar | ✅ Simplified Reviews

**Total Endpoints:** 75 (was 65)
**New Endpoints:** +10 messaging endpoints

---

## 🩺 **1. HEALTH & METRICS ENDPOINTS**

### **1.1 Health Check**
```
GET http://localhost:8000/v1/health/
```
**Headers:** None  
**Body:** None

### **1.2 Platform Metrics**
```
GET http://localhost:8000/v1/metrics/
```
**Headers:** None  
**Body:** None

---

## 🔐 **2. AUTHENTICATION ENDPOINTS**

### **2.1 Register Tourist**
```
POST http://localhost:8000/api/v1/auth/register/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
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

### **2.2 Register Guide**
```
POST http://localhost:8000/api/v1/auth/register/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
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

### **2.3 Register Second Tourist**
```
POST http://localhost:8000/api/v1/auth/register/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
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

### **2.4 Register Second Guide**
```
POST http://localhost:8000/api/v1/auth/register/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "username": "guide_fatima",
  "email": "fatima@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "Fatima",
  "last_name": "Zahra",
  "phone_number": "+213666789123",
  "user_type": "guide"
}
```

### **2.5 Login as Tourist**
```
POST http://localhost:8000/api/v1/auth/login/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "username": "tourist_sara",
  "password": "SecurePass123!"
}
```

### **2.6 Login as Guide**
```
POST http://localhost:8000/api/v1/auth/login/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "username": "guide_ahmed",
  "password": "SecurePass123!"
}
```

### **2.7 Get Current User Profile**
```
GET http://localhost:8000/api/v1/auth/me/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_ACCESS_TOKEN_HERE"
}
```
**Body:** None

### **2.8 Update User Profile**
```
PUT http://localhost:8000/api/v1/auth/me/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_ACCESS_TOKEN_HERE"
}
```
**Body:**
```json
{
  "email": "ahmed.updated@example.com",
  "first_name": "Ahmed",
  "last_name": "Benali Updated",
  "phone_number": "+213555999888"
}
```

### **2.9 Refresh Token**
```
POST http://localhost:8000/api/v1/auth/refresh/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "refresh": "YOUR_REFRESH_TOKEN_HERE"
}
```

### **2.10 Logout**
```
POST http://localhost:8000/api/v1/auth/logout/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_ACCESS_TOKEN_HERE"
}
```
**Body:**
```json
{
  "refresh": "YOUR_REFRESH_TOKEN_HERE"
}
```

---

## 🗺️ **3. LOCATION ENDPOINTS**

### **3.1 List All Wilayas**
```
GET http://localhost:8000/api/v1/wilayas/
```
**Headers:** None  
**Body:** None

### **3.2 Get Wilaya Details (Algiers - ID: 1)**
```
GET http://localhost:8000/api/v1/wilayas/1/
```
**Headers:** None  
**Body:** None

### **3.3 Get Wilaya Details (Oran - ID: 31)**
```
GET http://localhost:8000/api/v1/wilayas/31/
```
**Headers:** None  
**Body:** None

### **3.4 Get Wilaya Details (Constantine - ID: 25)**
```
GET http://localhost:8000/api/v1/wilayas/25/
```
**Headers:** None  
**Body:** None

### **3.5 Get Guides in Algiers**
```
GET http://localhost:8000/api/v1/wilayas/1/guides/
```
**Headers:** None  
**Body:** None

### **3.6 Get Guides in Oran**
```
GET http://localhost:8000/api/v1/wilayas/31/guides/
```
**Headers:** None  
**Body:** None

### **3.7 Get Tours in Algiers**
```
GET http://localhost:8000/api/v1/wilayas/1/tours/
```
**Headers:** None  
**Body:** None

### **3.8 Get Tours in Oran**
```
GET http://localhost:8000/api/v1/wilayas/31/tours/
```
**Headers:** None  
**Body:** None

---

## 👤 **4. PROFILE ENDPOINTS**

### **4.1 List All Guides**
```
GET http://localhost:8000/api/v1/profiles/guides/
```
**Headers:** None  
**Body:** None

### **4.2 Get Specific Guide Details (ID: 1)**
```
GET http://localhost:8000/api/v1/profiles/guides/1/
```
**Headers:** None  
**Body:** None

### **4.3 Get My Guide Profile**
```
GET http://localhost:8000/api/v1/profiles/guides/me/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

### **4.4 Update My Guide Profile**
```
PUT http://localhost:8000/api/v1/profiles/guides/me/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
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

### **4.5 Get Guide Pricing (ID: 1)**
```
GET http://localhost:8000/api/v1/profiles/guides/1/pricing/
```
**Headers:** None  
**Body:** None

### **4.6 Add Guide Certification**
```
POST http://localhost:8000/api/v1/profiles/guides/certifications/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "title": "Tourism Professional License"
}
```

### **4.7 Add Second Guide Certification**
```
POST http://localhost:8000/api/v1/profiles/guides/certifications/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "title": "First Aid Certification"
}
```

### **4.8 List My Certifications**
```
GET http://localhost:8000/api/v1/profiles/guides/certifications/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

### **4.9 Get Certification Details (ID: 1)**
```
GET http://localhost:8000/api/v1/profiles/guides/certifications/1/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

### **4.10 Update Certification**
```
PUT http://localhost:8000/api/v1/profiles/guides/certifications/1/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "title": "Tourism Professional License - Updated"
}
```

### **4.11 Delete Certification**
```
DELETE http://localhost:8000/api/v1/profiles/guides/certifications/2/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

### **4.12 Get My Tourist Profile**
```
GET http://localhost:8000/api/v1/profiles/tourists/me/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:** None

### **4.13 Update My Tourist Profile**
```
PUT http://localhost:8000/api/v1/profiles/tourists/me/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "bio": "Travel enthusiast exploring the beautiful countries of North Africa. Particularly interested in history, culture, and traditional cuisine.",
  "date_of_birth": "1990-05-15",
  "nationality": "French",
  "preferred_language": "French"
}
```

---

## 🏛️ **5. TOUR ENDPOINTS**

### **5.1 List All Tours**
```
GET http://localhost:8000/api/v1/tours/
```
**Headers:** None  
**Body:** None

### **5.2 Create First Tour (Casbah)**
```
POST http://localhost:8000/api/v1/tours/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
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

### **5.3 Create Second Tour (Sahara)**
```
POST http://localhost:8000/api/v1/tours/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "title": "Sahara Desert Adventure - Tassili n'Ajjer",
  "description": "Experience the breathtaking landscapes of the Sahara Desert and discover ancient rock art in Tassili n'Ajjer National Park. Journey through dramatic sandstone formations and prehistoric cave paintings.",
  "wilaya": 33,
  "duration_hours": 8.0,
  "max_group_size": 6,
  "included_services": ["4WD transportation", "Professional guide", "Traditional Tuareg lunch", "Safety equipment", "Bottled water"],
  "excluded_services": ["Accommodation", "International flights", "Personal travel insurance", "Camping gear"],
  "meeting_point": "Djanet Airport Terminal",
  "latitude": 24.5570,
  "longitude": 9.4844,
  "tags": ["sahara", "desert", "adventure", "rock-art", "nature", "prehistoric"]
}
```

### **5.4 Create Third Tour (Oran)**
```
POST http://localhost:8000/api/v1/tours/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "title": "Oran City Discovery Tour",
  "description": "Discover the pearl of western Algeria with visits to the historic Fort Santa Cruz, the beautiful seafront, and the vibrant city center. Experience the unique blend of Spanish, French, and Arabic influences.",
  "wilaya": 31,
  "duration_hours": 6.0,
  "max_group_size": 10,
  "included_services": ["Transportation", "Professional guide", "Fort entrance fees", "Refreshments"],
  "excluded_services": ["Lunch", "Personal shopping", "Additional museum visits"],
  "meeting_point": "Oran Railway Station",
  "tags": ["city-tour", "fort", "history", "seafront", "cultural-mix"]
}
```

### **5.5 Get Tour Details (ID: 1)**
```
GET http://localhost:8000/api/v1/tours/1/
```
**Headers:** None  
**Body:** None

### **5.6 Get Tour Details (ID: 2)**
```
GET http://localhost:8000/api/v1/tours/2/
```
**Headers:** None  
**Body:** None

### **5.7 Update Tour**
```
PUT http://localhost:8000/api/v1/tours/1/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
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
  "tags": ["history", "culture", "walking", "UNESCO", "premium", "exclusive", "crafts"]
}
```

### **5.8 Get My Tours (Guide)**
```
GET http://localhost:8000/api/v1/tours/me/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

### **5.9 Search Tours**
```
GET http://localhost:8000/api/v1/tours/search/?q=casbah
```
**Headers:** None  
**Body:** None

### **5.10 Search Tours (Desert)**
```
GET http://localhost:8000/api/v1/tours/search/?q=desert sahara
```
**Headers:** None  
**Body:** None

### **5.11 Calculate Custom Price**
```
POST http://localhost:8000/api/v1/tours/1/calculate-price/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "duration_hours": 6.5
}
```

### **5.12 Calculate Custom Price (Long Tour)**
```
POST http://localhost:8000/api/v1/tours/1/calculate-price/
```
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "duration_hours": 12.0
}
```

### **5.13 Delete Tour**
```
DELETE http://localhost:8000/api/v1/tours/3/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:** None

---

## 📅 **6. BOOKING ENDPOINTS**

### **6.1 Create First Booking**
```
POST http://localhost:8000/api/v1/bookings/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "tour": 1,
  "booking_date": "2024-12-15",
  "time_slot": "morning",
  "group_size": 2,
  "notes": "Please provide vegetarian options for tea break. One participant has slight mobility issues."
}
```

### **6.2 Create Second Booking**
```
POST http://localhost:8000/api/v1/bookings/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "tour": 2,
  "booking_date": "2024-12-20",
  "group_size": 4,
  "notes": "Birthday celebration trip - please suggest best photo spots for sunset. Group includes elderly participants."
}
```

### **6.3 Create Third Booking (Different Tourist)**
```
POST http://localhost:8000/api/v1/bookings/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_SECOND_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "tour": 1,
  "booking_date": "2024-12-25",
  "group_size": 3,
  "notes": "Christmas day tour - looking for unique cultural experience. Very interested in architecture details."
}
```

### **6.4 List My Bookings (Tourist)**
```
GET http://localhost:8000/api/v1/bookings/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:** None

### **6.5 Get Booking Details (ID: 1)**
```
GET http://localhost:8000/api/v1/bookings/1/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:** None

### **6.6 Get Booking Details (ID: 2)**
```
GET http://localhost:8000/api/v1/bookings/2/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:** None

### **6.7 Update Booking Status**
```
PUT http://localhost:8000/api/v1/bookings/1/status/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "status": "confirmed"
}
```

### **6.8 Cancel Booking**
```
PUT http://localhost:8000/api/v1/bookings/3/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_SECOND_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "status": "cancelled"
}
```

### **6.9 Mark Booking as Completed**
```
PUT http://localhost:8000/api/v1/bookings/1/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_GUIDE_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "status": "completed"
}
```

---

## ⭐ **7. REVIEW ENDPOINTS**

### **7.1 Create Review for Completed Booking**
```
POST http://localhost:8000/api/v1/reviews/bookings/1/review/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "rating": 5,
  "title": "Absolutely Amazing Casbah Experience!",
  "comment": "Ahmed is an exceptional guide with incredible depth of knowledge about Algerian history and culture. The Casbah tour exceeded all our expectations! He showed us hidden gems that we never would have found on our own, shared fascinating stories about Ottoman architecture, and made the history come alive. The tea break at a traditional house was magical - felt like stepping back in time. Ahmed was also very considerate of our pace and dietary requirements. This was the highlight of our trip to Algeria. Highly recommend to anyone visiting Algiers!",
  "communication_rating": 5,
  "knowledge_rating": 5,
  "punctuality_rating": 5,
  "value_rating": 5
}
```

### **7.2 Create Second Review**
```
POST http://localhost:8000/api/v1/reviews/bookings/2/review/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "rating": 4,
  "title": "Great Desert Adventure with Minor Issues",
  "comment": "The Sahara desert tour was incredible - the landscapes are breathtaking and Ahmed knows all the best spots for photography. The rock art sites were fascinating and his explanations about prehistoric cultures were very informative. The traditional lunch was delicious. Only minor issue was the timing - we started a bit late which affected our sunset viewing. Otherwise, a memorable experience that I'd recommend to adventure seekers!",
  "communication_rating": 4,
  "knowledge_rating": 5,
  "punctuality_rating": 3,
  "value_rating": 4
}
```

### **7.3 Get Tour Reviews (Tour ID: 1)**
```
GET http://localhost:8000/api/v1/reviews/tours/1/reviews/
```
**Headers:** None  
**Body:** None

### **7.4 Get Tour Reviews (Tour ID: 2)**
```
GET http://localhost:8000/api/v1/reviews/tours/2/reviews/
```
**Headers:** None  
**Body:** None

### **7.5 Get Guide Reviews (Guide ID: 1)**
```
GET http://localhost:8000/api/v1/reviews/guides/1/reviews/
```
**Headers:** None  
**Body:** None

### **7.6 Get Review Details (ID: 1)**
```
GET http://localhost:8000/api/v1/reviews/1/
```
**Headers:** None  
**Body:** None

### **7.7 Update Review**
```
PUT http://localhost:8000/api/v1/reviews/1/
```
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:**
```json
{
  "rating": 5,
  "title": "Absolutely Amazing Casbah Experience - Updated!",
  "comment": "UPDATED: Ahmed is an exceptional guide with incredible depth of knowledge about Algerian history and culture. The Casbah tour exceeded all our expectations! He showed us hidden gems that we never would have found on our own, shared fascinating stories about Ottoman architecture, and made the history come alive. The tea break at a traditional house was magical - felt like stepping back in time. Ahmed was also very considerate of our pace and dietary requirements. UPDATE: I also want to mention that he followed up after our tour with additional reading recommendations and tips for our next visit. This level of service is outstanding! This was definitely the highlight of our trip to Algeria. Highly recommend to anyone visiting Algiers!",
  "communication_rating": 5,
  "knowledge_rating": 5,
  "punctuality_rating": 5,
  "value_rating": 5
}
```

### **7.8 Delete Review**
```
DELETE http://localhost:8000/api/v1/reviews/2/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_ACCESS_TOKEN"
}
```
**Body:** None

---

## 🔍 **8. ADVANCED FILTERING & SEARCH**

### **8.1 Filter Guides by Minimum Rating**
```
GET http://localhost:8000/api/v1/profiles/guides/?min_rating=4.0
```
**Headers:** None  
**Body:** None

### **8.2 Filter Guides by Maximum Price**
```
GET http://localhost:8000/api/v1/profiles/guides/?max_price=8000
```
**Headers:** None  
**Body:** None

### **8.3 Filter Guides by Wilaya (Algiers)**
```
GET http://localhost:8000/api/v1/profiles/guides/?wilaya=1
```
**Headers:** None  
**Body:** None

### **8.4 Filter Guides by Language**
```
GET http://localhost:8000/api/v1/profiles/guides/?language=French
```
**Headers:** None  
**Body:** None

### **8.5 Filter Guides by Experience**
```
GET http://localhost:8000/api/v1/profiles/guides/?years_experience=3
```
**Headers:** None  
**Body:** None

### **8.6 Filter Tours by Wilaya (Algiers)**
```
GET http://localhost:8000/api/v1/tours/?wilaya=1
```
**Headers:** None  
**Body:** None

### **8.7 Filter Tours by Maximum Price**
```
GET http://localhost:8000/api/v1/tours/?max_price=12000
```
**Headers:** None  
**Body:** None

### **8.8 Filter Tours by Duration**
```
GET http://localhost:8000/api/v1/tours/?duration=4
```
**Headers:** None  
**Body:** None

### **8.9 Filter Tours by Guide**
```
GET http://localhost:8000/api/v1/tours/?guide_id=1
```
**Headers:** None  
**Body:** None

### **8.10 Complex Tour Filter**
```
GET http://localhost:8000/api/v1/tours/?wilaya=1&max_price=15000&duration__lte=6
```
**Headers:** None  
**Body:** None

---

## 📊 **9. FINAL VERIFICATION ENDPOINTS**

### **9.1 Updated Platform Metrics**
```
GET http://localhost:8000/v1/metrics/
```
**Headers:** None  
**Body:** None

### **9.2 All Guides in Algiers (After Profile Creation)**
```
GET http://localhost:8000/api/v1/wilayas/1/guides/
```
**Headers:** None  
**Body:** None

### **9.3 All Tours in Algiers (After Tour Creation)**
```
GET http://localhost:8000/api/v1/wilayas/1/tours/
```
**Headers:** None  
**Body:** None

### **9.4 Complete Guide Profile with Stats**
```
GET http://localhost:8000/api/v1/profiles/guides/1/
```
**Headers:** None  
**Body:** None

### **9.5 All Guide Reviews**
```
GET http://localhost:8000/api/v1/reviews/guides/1/reviews/
```
**Headers:** None  
**Body:** None

---

## 💬 **10. MESSAGING SYSTEM ENDPOINTS [NEW]**

### **10.1 Create Conversation**
```
POST http://localhost:8000/api/v1/messaging/conversations/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "guide_id": 1
}
```

### **10.2 List Tourist Conversations**
```
GET http://localhost:8000/api/v1/messaging/conversations/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN"
}
```
**Body:** None

### **10.3 Get Conversation Messages**
```
GET http://localhost:8000/api/v1/messaging/conversations/1/messages/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN"
}
```
**Body:** None

### **10.4 Send Message**
```
POST http://localhost:8000/api/v1/messaging/conversations/1/send_message/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "content": "Hello! I'm interested in your Casbah tour. Is it available next weekend?"
}
```

### **10.5 Mark Messages as Read**
```
POST http://localhost:8000/api/v1/messaging/conversations/1/mark_read/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_JWT_TOKEN"
}
```
**Body:** None

### **10.6 Create Custom Tour Request**
```
POST http://localhost:8000/api/v1/messaging/custom-requests/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "guide": 1,
  "title": "Custom Photography Tour of Algiers",
  "description": "I want a specialized photography tour focusing on architectural heritage and street photography in Algiers. Looking for golden hour shots and unique perspectives.",
  "preferred_date": "2024-02-15",
  "duration_hours": 6,
  "group_size": 2,
  "budget": 12000.00,
  "special_requirements": "Need help with camera settings and composition tips. Prefer early morning start."
}
```

### **10.7 List Tourist Custom Requests**
```
GET http://localhost:8000/api/v1/messaging/custom-requests/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN"
}
```
**Body:** None

### **10.8 List Guide Custom Requests**
```
GET http://localhost:8000/api/v1/messaging/custom-requests/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN"
}
```
**Body:** None

### **10.9 Guide Accept Custom Request**
```
POST http://localhost:8000/api/v1/messaging/custom-requests/1/respond/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "action": "accept",
  "proposed_price": 15000.00,
  "alternative_date": "2024-02-16",
  "guide_response": "I'd love to do this photography tour! I can offer great spots for golden hour and architectural shots. Proposed slight date change for better lighting conditions."
}
```

### **10.10 Guide Reject Custom Request**
```
POST http://localhost:8000/api/v1/messaging/custom-requests/2/respond/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "action": "reject",
  "guide_response": "Unfortunately, I'm not available during that period and don't specialize in photography tours."
}
```

---

## 🌤️ **11. WEATHER API INTEGRATION [NEW]**

### **11.1 Get Tour with Weather Forecast**
```
GET http://localhost:8000/api/v1/tours/1/?date=2024-02-15
```
**Headers:** None  
**Body:** None
**Note:** Weather forecast will be included in response if date is within 5 days

---

## 🎯 **TOTAL ENDPOINTS TO TEST: 75**

### **Breakdown:**
- ✅ Health & Metrics: 2 endpoints
- ✅ Authentication: 10 endpoints  
- ✅ Locations: 8 endpoints
- ✅ Profiles: 13 endpoints
- ✅ Tours: 12 endpoints (with weather integration)
- ✅ Bookings: 6 endpoints (with time slots)
- ✅ Reviews: 8 endpoints (simplified)
- ✅ Messaging: 10 endpoints [NEW]
- ✅ Weather Integration: 1 endpoint [NEW]
- ✅ Filtering: 5 endpoints

## 🎯 **NEW BUSINESS LOGIC ENDPOINTS** (Added in Latest Update)

### **Advanced Booking Management**

#### **Guide Pending Bookings Dashboard**
```
GET http://localhost:8000/api/v1/bookings/guide/pending/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```

#### **Update Booking Status (Guide Approval/Rejection)**
```
PUT http://localhost:8000/api/v1/bookings/1/status/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body (Approve):**
```json
{
  "status": "confirmed",
  "guide_notes": "Looking forward to showing you the beautiful sites of Algiers!"
}
```
**Body (Reject):**
```json
{
  "status": "rejected",
  "guide_notes": "Unfortunately, I'm not available on this date. Please check my availability calendar."
}
```

#### **Tourist Booking History**
```
GET http://localhost:8000/api/v1/bookings/tourist/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN",
  "Content-Type": "application/json"
}
```

#### **Cancel Booking (24-hour policy)**
```
POST http://localhost:8000/api/v1/bookings/1/cancel/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "cancellation_reason": "Change of travel plans due to work commitments"
}
```

### **Advanced Tour Management**

#### **Advanced Tour Search**
```
GET http://localhost:8000/api/v1/tours/search/?q=casbah&location=1&min_price=50&max_price=200&difficulty=medium&min_rating=4
```

#### **Tour Price Calculator with Group Discounts**
```
GET http://localhost:8000/api/v1/tours/1/calculate-price/?group_size=8
```
**Expected Response:**
```json
{
  "tour_id": 1,
  "tour_title": "Historic Casbah Walking Tour",
  "group_size": 8,
  "base_price_per_person": 75.00,
  "subtotal": 600.00,
  "discount_percentage": 10.0,
  "discount_amount": 60.00,
  "final_price": 540.00,
  "currency": "DZD",
  "min_group_size": 2,
  "max_group_size": 12
}
```

#### **Popular Tours**
```
GET http://localhost:8000/api/v1/tours/popular/
```

#### **Guide Tour Dashboard**
```
GET http://localhost:8000/api/v1/tours/guide/dashboard/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Expected Response:**
```json
{
  "guide_info": {
    "name": "Ahmed Benali",
    "rating": 4.7,
    "total_reviews": 23
  },
  "statistics": {
    "total_tours": 5,
    "active_tours": 4,
    "total_bookings": 47,
    "completed_bookings": 42,
    "completion_rate": 89.36
  },
  "tours": [...],
  "recent_bookings": [...]
}
```

### **Complete Review System**

#### **Create Review for Completed Booking**
```
POST http://localhost:8000/api/v1/reviews/booking/1/create/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_TOURIST_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "rating": 5,
  "title": "Amazing experience in the Casbah!",
  "comment": "Ahmed was incredibly knowledgeable about the history and showed us hidden gems. Highly recommend this tour for anyone visiting Algiers!"
}
```

#### **Guide Response to Review**
```
POST http://localhost:8000/api/v1/reviews/1/guide-response/
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```
**Body:**
```json
{
  "guide_response": "Thank you Sara for the wonderful review! It was my pleasure to share the rich history of our beautiful Casbah with you. Hope to see you again in Algeria!"
}
```

#### **Tour Reviews List**
```
GET http://localhost:8000/api/v1/reviews/tour/1/?ordering=-created_at&is_approved=true
```

#### **Guide Reviews List**
```
GET http://localhost:8000/api/v1/reviews/guide/1/?min_rating=4
```

#### **Review Statistics for Guide**
```
GET http://localhost:8000/api/v1/reviews/guide/1/statistics/
```
**Expected Response:**
```json
{
  "total_reviews": 23,
  "average_rating": 4.7,
  "rating_distribution": {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 8,
    "5": 12
  }
}
```

### **Advanced Tour Filtering**

#### **Multi-Criteria Tour Search**
```
GET http://localhost:8000/api/v1/tours/?search=casbah&location=1&difficulty=medium&min_price=50&max_price=150&min_duration=2&max_duration=6&min_group_size=4&max_group_size=10&min_rating=4&ordering=-average_rating
```

#### **My Tours (Guide)**
```
GET http://localhost:8000/api/v1/tours/my-tours/?is_active=true&ordering=-created_at
```
**Headers:**
```json
{
  "Authorization": "Bearer YOUR_GUIDE_JWT_TOKEN",
  "Content-Type": "application/json"
}
```

### **Business Logic Validation Examples**

#### **Booking Validation Errors**
```
POST http://localhost:8000/api/v1/bookings/
```
**Body (Invalid - past date):**
```json
{
  "tour": 1,
  "booking_date": "2023-01-01",
  "group_size": 4,
  "special_requests": "Can we start earlier?"
}
```
**Expected Error:**
```json
{
  "booking_date": ["Booking date cannot be in the past"]
}
```

#### **Review Validation Errors**
```
POST http://localhost:8000/api/v1/reviews/booking/1/create/
```
**Body (Booking not completed):**
```json
{
  "rating": 5,
  "title": "Great tour!",
  "comment": "Loved it!"
}
```
**Expected Error:**
```json
{
  "error": "You can only review completed bookings"
}
```

#### **Tour Deletion Validation**
```
DELETE http://localhost:8000/api/v1/tours/1/
```
**Expected Error (if active bookings exist):**
```json
{
  "error": "Cannot delete tour with active bookings"
}
```

**EVERY SINGLE ENDPOINT IS COVERED WITH EXACT JSON DATA! 🔥**

## 📊 **ENDPOINT SUMMARY (Updated)**

- ✅ Authentication: 10 endpoints  
- ✅ Locations: 8 endpoints
- ✅ Profiles: 13 endpoints
- ✅ Tours: 18 endpoints (enhanced with business logic)
- ✅ Bookings: 12 endpoints (complete workflow)
- ✅ Reviews: 14 endpoints (complete system)
- ✅ Messaging: 10 endpoints [Existing]
- ✅ Weather Integration: 1 endpoint [Existing]
- ✅ Business Logic: 15 new endpoints [NEW]

**Total: 101 Endpoints** (Previously 75)

## 🔑 **IMPORTANT NOTES:**

1. **Replace tokens**: Use actual JWT tokens from login responses
2. **Replace IDs**: Use actual IDs returned from creation endpoints  
3. **Test in order**: Some endpoints depend on data from previous tests
4. **Save responses**: Keep track of tokens and IDs for subsequent tests
5. **Check status codes**: 200/201 = success, 400/401/403/404 = errors
6. **Business Logic**: New endpoints include comprehensive validation and business rules
7. **Role Permissions**: Some endpoints are role-specific (tourist vs guide)

**NOW GO TEST EVERY SINGLE ENDPOINT INCLUDING THE NEW BUSINESS LOGIC! 🚀🇩🇿**
