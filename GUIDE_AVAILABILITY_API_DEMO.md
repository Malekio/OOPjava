# 🗓️ Guide Availability Calendar API - Complete Demo

## 📚 **Overview**
This system allows guides to manage their availability calendar through a comprehensive REST API.

## 🎯 **API Endpoints Summary**

### Base URL: `/v1/profiles/guides/availability/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/availability/` | View your availability (next 60 days) |
| `POST` | `/availability/` | Create single availability slot |
| `PUT` | `/availability/` | Update existing slot |
| `DELETE` | `/availability/` | Remove availability slot |
| `POST` | `/availability/bulk/` | Create multiple slots at once |

---

## 📝 **Request Examples**

### **1. View Current Availability**
```bash
curl -X GET "http://localhost:8000/v1/profiles/guides/availability/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "date": "2025-12-01",
      "time_slot": "morning",
      "is_available": true,
      "created_at": "2025-11-29T10:30:00Z"
    }
  ],
  "total_slots": 15
}
```

---

### **2. Create Single Availability Slot**
```bash
curl -X POST "http://localhost:8000/v1/profiles/guides/availability/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "date": "2025-12-15",
       "time_slot": "morning",
       "is_available": true
     }'
```

**Response:**
```json
{
  "success": true,
  "message": "Availability slot created successfully",
  "data": {
    "id": 123,
    "date": "2025-12-15",
    "time_slot": "morning",
    "is_available": true,
    "created_at": "2025-11-29T10:30:00Z"
  }
}
```

---

### **3. Update Existing Slot**
```bash
curl -X PUT "http://localhost:8000/v1/profiles/guides/availability/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 123,
       "is_available": false
     }'
```

---

### **4. Delete Availability Slot**
```bash
curl -X DELETE "http://localhost:8000/v1/profiles/guides/availability/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "id": 123
     }'
```

---

### **5. Bulk Create Multiple Slots**
```bash
curl -X POST "http://localhost:8000/v1/profiles/guides/availability/bulk/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "start_date": "2025-12-01",
       "end_date": "2025-12-07",
       "time_slots": ["morning", "afternoon"],
       "is_available": true
     }'
```

**Response:**
```json
{
  "success": true,
  "message": "Bulk operation completed",
  "summary": {
    "created": 14,
    "skipped": 0
  },
  "created_slots": [
    {
      "id": 124,
      "date": "2025-12-01",
      "time_slot": "morning",
      "is_available": true,
      "created_at": "2025-11-29T10:30:00Z"
    }
    // ... more slots
  ],
  "skipped_slots": []
}
```

---

## ⏰ **Time Slot Options**

| Value | Description | Time Range |
|-------|-------------|------------|
| `"morning"` | Morning tours | 8:00-12:00 |
| `"afternoon"` | Afternoon tours | 13:00-17:00 |
| `"evening"` | Evening tours | 18:00-22:00 |
| `"full_day"` | Full day tours | 8:00-17:00 |

---

## 🚦 **Common Use Cases**

### **Scenario 1: Guide Sets Weekly Schedule**
```json
// Monday to Friday mornings available
{
  "start_date": "2025-12-02",
  "end_date": "2025-12-06",
  "time_slots": ["morning"],
  "is_available": true
}
```

### **Scenario 2: Guide Blocks Vacation Days**
```json
// Mark unavailable for vacation week
{
  "start_date": "2025-12-15",
  "end_date": "2025-12-22",
  "time_slots": ["morning", "afternoon", "evening"],
  "is_available": false
}
```

### **Scenario 3: Guide Changes Single Day**
```json
// Update specific day
{
  "id": 123,
  "is_available": false
}
```

---

## ✅ **Validation Rules**

1. **Date Validation:**
   - Cannot set availability for past dates
   - Date range cannot exceed 90 days (bulk operations)

2. **Duplicate Prevention:**
   - Each guide can only have one slot per date/time_slot combination
   - System will skip existing slots in bulk operations

3. **Authentication:**
   - Only authenticated guides can manage availability
   - Guides can only manage their own availability

---

## 📱 **Frontend Integration Examples**

### **React/JavaScript Example:**
```javascript
// Create availability slot
const createAvailability = async (dateData) => {
  const response = await fetch('/v1/profiles/guides/availability/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dateData)
  });
  
  return await response.json();
};

// Usage
createAvailability({
  date: '2025-12-15',
  time_slot: 'morning',
  is_available: true
});
```

### **Flutter/Dart Example:**
```dart
// Create availability
Future<Map<String, dynamic>> createAvailability(Map<String, dynamic> data) async {
  final response = await http.post(
    Uri.parse('$baseUrl/v1/profiles/guides/availability/'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: json.encode(data),
  );
  
  return json.decode(response.body);
}
```

---

## 🔗 **Integration with Booking System**

The availability calendar integrates seamlessly with the existing booking system:

1. **Tourist Views:** Available slots shown in `/v1/bookings/calendar/available/`
2. **Booking Creation:** System checks availability before confirming bookings
3. **Auto-Updates:** Confirmed bookings automatically mark slots as unavailable

---

## 🛡️ **Security & Permissions**

- ✅ JWT Authentication required
- ✅ Guide-only access (role validation)
- ✅ Own data access only
- ✅ Input validation and sanitization
- ✅ Rate limiting (Django default)

---

## 📊 **Response Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | Success | Operation completed |
| `201` | Created | New slots created |
| `400` | Bad Request | Invalid data format |
| `401` | Unauthorized | Invalid/missing token |
| `403` | Forbidden | Not a guide user |
| `404` | Not Found | Slot doesn't exist |

---

**🎉 Ready to use! Guides now have complete control over their availability calendar.**
