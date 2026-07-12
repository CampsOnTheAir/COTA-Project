# COTA-Project
Camps On The Air (COTA) - A community driven amateur radio camping activity concept

## What is COTA?

Camps On The Air (COTA) is a proposed amateur radio activity designed to encourage portable operation from campgrounds and camping locations.

Unlike many existing award programs, COTA aims to be relaxed, accessible and community-driven. The idea is simple:

If you're going camping, bring a radio.

Whether you operate from a provincial campground, a forestry recreation site, a national park campground or a remote backcountry location, COTA is intended to celebrate portable radio, camping and exploration.

## Why?

Many amateur radio operators already enjoy:

- Camping
- Portable stations
- Vehicle builds
- Backpacking
- Overlanding
- Hiking
- Exploring

COTA brings those interests together.

## Vision

COTA is intended to encourage operators to bring amateur radio into their outdoor adventures.

Whether someone is operating with a handheld from a campsite, a portable HF station from the backcountry, or a vehicle-based setup from a remote location, all forms of portable operation are welcome.

The goal is simple:

Go camping. Bring a radio.

## Current Status

This is a community discussion project.

Rules, awards and systems are not final.

Feedback and contributions are welcome.

---

# COTA Database & Web System

## Overview

To support the COTA community, a comprehensive database system and web interface have been created to record amateur radio contacts made during campground activations. This system allows operators to log their contacts, reference park information, and suggest new campground locations for future activations.

## Features

### 📡 Contact Logging
- Log amateur radio contacts with detailed information
- Track frequency, mode, and signal reports
- Reference operator and park information
- Add notes and equipment details
- View recent contacts with filtering capabilities

### 🏕️ Park Management
- Maintain database of campgrounds and parks
- Store location coordinates and access information
- Track activation history by park
- View statistics by location
- Easily reference parks when logging contacts

### 💡 Campground Suggestion System
- Submit new campground suggestions through the web interface
- Track amenities (parking, power, water availability)
- Include access information and contact details
- Admin review and approval workflow
- Automatically convert approved suggestions into parks

### 📊 Statistics & Analytics
- Contact statistics by park
- Operator activity tracking
- Daily activation summaries
- Radio frequency usage reports
- Unique remote operators contacted per park

## Project Structure

```
COTA-Project/
├── database/
│   ├── schema.sql              # Main database schema with tables and views
│   └── schema_suggestions.sql   # Campground suggestions table schema
├── web/
│   └── index.html              # Interactive web interface for all functions
├── backend/
│   ├── app.py                  # Flask API backend with all endpoints
│   ├── requirements.txt         # Python dependencies
│   └── .env.example            # Environment configuration template
└── README.md
```

## Setup Instructions

### 1. Database Setup

Create the MySQL database and import the schema files:

```bash
# Create database and import main schema
mysql -u root -p < database/schema.sql

# Import suggestions table schema
mysql -u root -p < database/schema_suggestions.sql
```

### 2. Backend Setup

Install and run the Flask backend API:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env

# Edit .env with your database credentials
nano .env

# Start the Flask server
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Web Interface

Access the web interface through your browser:

- Open `web/index.html` directly in your web browser
- Or serve through a web server pointing to the web directory
- Configure API endpoint if running on different host/port

## Web Interface Tabs

### View Contacts
- Browse all logged radio contacts
- Filter by date, call sign, or park
- View contact details including frequency, mode, and signal reports
- See operator information and remote station details

### Log Contact
- Submit a new radio contact record
- Required fields: your call sign, contact date/time, park, remote call sign, frequency, and mode
- Optional fields: operator name, signal reports, remote location, notes
- Auto-creates operator record if first contact from call sign

### Suggest a Campground
- Submit new campground/park suggestions
- Provide location, description, and access information
- Include amenity information (parking, power, water)
- Add cell coverage details
- Optionally include GPS coordinates and website URL
- Suggestions enter pending review status

### Admin Panel
- View all campground suggestions with status indicators
- Filter suggestions by status (pending, under review, approved, rejected)
- Click "Review" to see full suggestion details
- Add admin notes
- Approve suggestions (automatically creates park entry) or reject
- Track review history

## API Endpoints

### Contacts
- `GET /api/contacts` - List all contacts with operator and park information
- `POST /api/contacts` - Create new contact record
- `GET /api/stats/operators` - Get operator statistics and activity

### Parks
- `GET /api/parks` - List all parks for selection in forms
- `POST /api/parks` - Create new park record

### Suggestions
- `GET /api/suggestions` - List all suggestions with optional status filter
- `GET /api/suggestions/{id}` - Get full details of specific suggestion
- `POST /api/suggestions` - Submit new campground suggestion
- `PATCH /api/suggestions/{id}` - Update suggestion status and add admin notes

### Statistics
- `GET /api/stats/parks` - Get comprehensive park statistics
- `GET /api/stats/operators` - Get comprehensive operator statistics

## Database Schema

### Core Tables

- **parks** - Park and campground reference data with coordinates
- **campgrounds** - Specific camping sites within parks
- **operators** - Amateur radio operators with call signs
- **contacts** - Individual radio contact records
- **activations** - Park activation sessions with duration tracking
- **equipment** - Radio equipment inventory per operator
- **campground_suggestions** - User-submitted campground suggestions with admin workflow

### Database Views

- `v_recent_contacts` - Latest contacts with all related information
- `v_park_summary` - Park statistics including contact counts
- `v_pending_suggestions` - Suggestions awaiting review or under review

## How to Use

### Logging a Contact

1. Navigate to "Log Contact" tab
2. Enter your call sign (required)
3. Enter your name (optional, auto-filled on subsequent logins)
4. Select contact date and time (defaults to current time)
5. Choose the park where you made contact (required)
6. Enter remote station call sign (required)
7. Enter remote operator name (optional)
8. Specify frequency in MHz (required)
9. Select transmission mode: SSB, CW, FM, AM, DIGITAL, RTTY, PSK31 (required)
10. Enter signal reports sent and received (RST format, optional)
11. Add remote location details (optional)
12. Add notes about the contact (optional)
13. Click "Log Contact" to submit

### Suggesting a Campground

1. Navigate to "Suggest a Campground" tab
2. Enter your name (required)
3. Enter your email (optional, for contact if questions arise)
4. Enter your call sign (optional)
5. Enter campground name (required)
6. Enter location details (required)
7. Enter state/province and country
8. Add GPS coordinates if available (latitude and longitude)
9. Provide description of the campground
10. Include access information (fees, permits, hours)
11. Check amenities available (parking, power, water)
12. Select cell coverage quality
13. Add radio club contact if applicable
14. Include website URL if applicable
15. Click "Submit Suggestion"

### Reviewing Suggestions (Admin)

1. Navigate to "Admin Panel" tab
2. Filter by status if desired (pending, under review, approved, rejected)
3. Click "Review" on suggestion of interest
4. Review all submitted details in modal window
5. Add admin notes if needed
6. Click "Approve" to add to parks database or "Reject" with reason
7. Approved suggestions automatically create new park entries

## Technology Stack

- **Database**: MySQL/MariaDB relational database
- **Backend**: Python with Flask web framework
- **Frontend**: HTML5, CSS3, and JavaScript (no frameworks required)
- **API**: RESTful JSON API with CORS support
- **Styling**: Responsive design with mobile support

## Contributing

The COTA community welcomes contributions and feedback:

- Submit suggestions for new campgrounds through the web interface
- Log your portable operation contacts to build community data
- Provide feedback on the system functionality
- Help identify and correct park information

## Future Enhancements

Planned features and integrations:

- K4 Award integration for qualifying contacts
- ARRL Parks on the Air (POTA) tracking and verification
- Mobile application for easier field logging
- Email notifications for approved suggestions
- Advanced reporting and analytics dashboard
- User authentication and account management
- Integration with frequency databases
- Map visualization of parks and contact locations
- Automated badge/certificate generation
- API documentation and webhooks for third-party integration
