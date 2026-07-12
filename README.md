# COTA - Camps On The Air Project

## Overview
COTA (Camps On The Air) is a community-driven amateur radio camping activity system that allows radio operators to log contacts while camping at various parks and campgrounds.

## Features

### 📡 Contact Logging
- Log amateur radio contacts with detailed information
- Track frequency, mode, and signal reports
- Reference operator and park information
- Add notes and equipment details
- View recent contacts with filtering

### 🏕️ Park Management
- Maintain database of campgrounds and parks
- Store location coordinates
- Track activation history by park
- View statistics by location

### 💡 Suggestion System
- Submit new campground suggestions
- Track amenities (parking, power, water)
- Include access information and contact details
- Admin review and approval workflow
- Convert approved suggestions to parks

### 📊 Statistics & Analytics
- Contact statistics by park
- Operator activity tracking
- Daily activation summaries
- Radio frequency usage reports

## Project Structure

```
COTA-Project/
├── database/
│   ├── schema.sql           # Main database schema
│   └── schema_suggestions.sql   # Suggestion table schema
├── web/
│   └── index.html           # Interactive web interface
├── backend/
│   ├── app.py              # Flask API backend
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment configuration
└── README.md
```

## Setup Instructions

### 1. Database Setup
```bash
# Create database
mysql -u root -p < database/schema.sql
mysql -u root -p < database/schema_suggestions.sql
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python app.py
```

### 3. Web Interface
- Open `web/index.html` in a web browser
- Or serve through a web server pointing to the web directory

## API Endpoints

### Contacts
- `GET /api/contacts` - List all contacts
- `POST /api/contacts` - Create new contact
- `GET /api/stats/operators` - Operator statistics

### Parks
- `GET /api/parks` - List all parks
- `POST /api/parks` - Create new park

### Suggestions
- `GET /api/suggestions` - List all suggestions
- `GET /api/suggestions/{id}` - Get suggestion details
- `POST /api/suggestions` - Submit new suggestion
- `PATCH /api/suggestions/{id}` - Update suggestion status (admin)

### Statistics
- `GET /api/stats/parks` - Park statistics
- `GET /api/stats/operators` - Operator statistics

## Database Schema

### Core Tables
- **parks** - Park/campground reference data
- **campgrounds** - Specific camping sites
- **operators** - Radio operators
- **contacts** - Individual radio contacts
- **activations** - Park activation sessions
- **equipment** - Radio equipment inventory
- **campground_suggestions** - User-submitted suggestions

### Views
- `v_recent_contacts` - Latest contacts with details
- `v_park_summary` - Park statistics
- `v_pending_suggestions` - Suggestions awaiting review

## Features Explained

### Log a Contact
1. Navigate to "Log Contact" tab
2. Enter your call sign and name
3. Select contact date/time
4. Choose the park where you made contact
5. Enter remote station details (call sign, location, etc.)
6. Specify frequency and mode
7. Add signal reports and notes
8. Submit

### Suggest a Campground
1. Navigate to "Suggest a Campground" tab
2. Provide campground details
3. Include amenities and access information
4. Add coordinates if known
5. Submit for admin review

### Admin Panel
1. View all pending and under-review suggestions
2. Click "Review" to see full details
3. Add admin notes
4. Approve (creates new park entry) or reject
5. Approved suggestions become available parks

## Technology Stack
- **Database**: MySQL/MariaDB
- **Backend**: Python/Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: RESTful JSON

## Contributing
Submit suggestions for new campgrounds through the web interface.

## Future Enhancements
- K4 Award integration
- ARRL Parks on the Air tracking
- Mobile app
- Email notifications for approved suggestions
- Advanced reporting and analytics
- User authentication and roles
- Integration with frequency databases