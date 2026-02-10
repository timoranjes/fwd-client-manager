# FWD Client Management System

## ✅ Status - FULLY BUILT (2026-02-10)

A complete insurance client management web application built with Flask.

## Features Implemented

### Core Features
✅ **Dashboard** - Overview stats, recent clients, activity log
✅ **Client Database** - Add, edit, delete clients with contact info
✅ **Policy Tracking** - Link clients to policies (Life, Health, etc.)
✅ **Renewals Calendar** - Track upcoming renewals (30/60/90 days)
✅ **Activity Notes** - Log calls, meetings, emails, follow-ups
✅ **Search** - Search clients by name, email, phone, WeChat
✅ **Export** - Export all data to CSV
✅ **Reports** - Analytics on policy types and status

## Quick Start

### Option 1: One-click Startup
```bash
cd /home/timoliao/clawd/fwd-client-manager
./start.sh
```

### Option 2: Manual
```bash
cd /home/timoliao/clawd/fwd-client-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

### Access the Application
- **Local URL**: http://localhost:5000
- **Network URL**: http://0.0.0.0:5000

## Project Structure

```
fwd-client-manager/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── start.sh           # Startup script
├── database.db         # SQLite database (auto-created)
├── templates/          # HTML templates
│   ├── base.html      # Base layout
│   ├── dashboard.html # Dashboard
│   ├── clients.html   # Client list
│   ├── client_form.html    # Add/Edit client
│   ├── client_detail.html  # Client details + notes
│   ├── renewals.html  # Renewal tracking
│   ├── calendar.html  # Calendar view
│   └── reports.html   # Analytics
└── static/            # CSS/JS (for future)
```

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (built-in, no setup)
- **Frontend**: Bootstrap 5 + Font Awesome
- **Styling**: Custom CSS (clean, professional look)

## Data Fields

### Client Information
- Name, Email, Phone, WeChat
- Policy Type (Life, Health, Critical Illness, etc.)
- Coverage Amount (HKD)
- Policy Start/End Dates
- Status (Active, Expired, Pending, Lapsed, Cancelled)

### Activity Logging
- Activity Type (Call, WeChat, Email, Meeting, etc.)
- Description
- Timestamp

## Deployment Options

### 1. Cloudflare Pages
Upload files and use start.sh

### 2. PythonAnywhere
Upload files, set up virtualenv, point to app.py

### 3. Railway / Render
Connect GitHub repo, set start command: `python app.py`

## API Endpoints

- `GET /api/calendar_events` - Calendar event data
- `GET /export` - Download CSV

---

**Built**: 2026-02-10
**Location**: `/home/timoliao/clawd/fwd-client-manager/`
