# MEDFIND – Smart Medicine Availability Finder
**Hackathon Software Project Prototype**

> **Tagline:** *"Find Medicines. Save Time. Stay Informed."*

---

## 1. Executive Summary & Problem Solved

Patients and caregivers frequently experience extreme stress and wasted hours hopping from pharmacy to pharmacy searching for urgently prescribed medicines. Because individual pharmacies carry varying stocks, patients often discover a medicine is out of stock only after traveling to the store.

**MEDFIND** provides a centralized, transparent platform where:
- Patients can instantly check real-time medicine availability across local pharmacies.
- Patients can view available stock counts before traveling.
- Patients can compare prices across pharmacies and locate the lowest-cost dispensary.
- Patients can view phone numbers, addresses, and hours, and call directly with one click.
- Pharmacy administrators have a dedicated, secure dashboard to update their stock quantities, adjust prices, monitor low-stock warnings, and register new medicines.

---

## 2. Technology Stack

- **Backend:** Python 3 & Flask (Lightweight, robust web framework)
- **Database:** SQLite 3 (ACID-compliant, zero-configuration relational database)
- **Frontend:** HTML5, CSS3, Modern Responsive Healthcare UI
- **Interactivity:** Vanilla JavaScript (Live search autocomplete, dynamic modals, auto-sorting)
- **Security:** Werkzeug password hashing (scrypt / pbkdf2:sha256) and parameterized SQL queries

---

## 3. Project File Structure

```text
MedFind/
│
├── app.py                     # Main Flask web application, routing, and controller logic
├── database.py                # Database connection, schemas, queries, and sample seeding
├── requirements.txt           # Python dependencies (Flask, Werkzeug)
├── README.md                  # Comprehensive setup, user guide, and hackathon documentation
├── medfind.db                 # SQLite database file (automatically created on first run)
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Patient homepage (search, how it works, stats, about, contact)
│   ├── search_results.html    # Search results cards, price comparison, alternative suggestions
│   ├── admin_login.html       # Secure pharmacy administrator login portal
│   ├── admin_dashboard.html   # Pharmacy inventory management, stock updater, and metrics
│   └── pharmacy_details.html  # Full pharmacy profile and comprehensive listed medicines
│
└── static/                    # Static frontend assets
    ├── css/
    │   └── style.css          # Medical green theme, responsive layouts, badges, and modals
    ├── js/
    │   └── script.js          # Live autocomplete, modal handling, credential quick-fillers
    └── images/
        └── logo.png           # MEDFIND branding logo
```

---

## 4. Setup and Installation Instructions

### Step 1: Open Terminal / Command Prompt
Navigate to the project directory:
```bash
cd "C:\Users\USHA  THOMAS\OneDrive\Documents\Hack\MedFind"
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```
*(Flask and Werkzeug are the only external requirements; SQLite and hashlib are part of the standard Python library).*

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Open in Web Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 5. Sample Demonstration Administrator Accounts

For the hackathon presentation and live evaluation, five demonstration chemist accounts are pre-configured:

| Pharmacy Name | City / Location | Admin Username | Default Password |
|---|---|---|---|
| **Apex Health Pharmacy** | Downtown | `apex_admin` | `admin123` |
| **Metro Care Chemist** | North Hills | `metro_admin` | `admin123` |
| **Wellness Forever Pharmacy** | Westside | `wellness_admin` | `admin123` |
| **Green Cross Medical Store** | University District | `greencross_admin` | `admin123` |
| **Lifeline Pharma Hub** | East Park | `lifeline_admin` | `admin123` |

> **Pro-Tip for Hackathon Demo:** The login page at `http://127.0.0.1:5000/admin/login` features clickable quick-fill chips. Clicking any pharmacy chip automatically fills the username and password fields!

---

## 6. Key Innovative Features Implemented

1. **Smart Medicine Search & Autocomplete:**
   - Type in the search box to get instant real-time suggestions of medicines, active formulas, and therapeutic classes.
2. **Stock Availability Checker:**
   - Visual badges: **In Stock** (Green), **Low Stock** (Yellow/Amber: $\le 10$ units), **Out of Stock** (Red: 0 units).
3. **Nearby Pharmacy Finder & Location Filter:**
   - Filter results by specific zones (Downtown, North Hills, Westside, University District, East Park) or view citywide.
4. **Price Comparison & "Best Price" Ribbon:**
   - Compares unit prices across all dispensing pharmacies and highlights the lowest available price.
5. **Low Stock Alert Notification:**
   - Pharmacy admins have a dedicated filter and dashboard card highlighting all medicines that have 10 or fewer units remaining.
6. **Last Updated Indicator:**
   - Displays real-time humanized update timestamps (e.g., *"Updated 5 mins ago"* or *"Just now"*).
7. **Out of Stock Suggestions:**
   - If a medicine is out of stock in a queried location, MEDFIND automatically surfaces alternative nearby pharmacies that carry verified stock.
8. **Decentralized Pharmacy Isolation:**
   - Each pharmacy admin can only view, edit, and delete their own inventory records.
9. **Instant Live Synchronization:**
   - When an administrator updates stock or price in the dashboard, changes immediately reflect in the public patient search results without requiring server restarts.

---

## 7. How Each Code File Works

- **`app.py`:**
  The Flask application controller. Sets up route endpoints (`/`, `/search`, `/pharmacy/<id>`, `/api/autocomplete`, `/admin/login`, `/admin/dashboard`, etc.), session management, authorization decorators (`@login_required`), flash notifications, and custom Jinja filters (`time_ago`, `currency`).
- **`database.py`:**
  Database abstraction layer. Handles SQLite table creation, foreign key constraints, connection factories, parameterized queries to prevent SQL injection, password verification, and seeding of demonstration data.
- **`static/css/style.css`:**
  Clean healthcare UI styled with CSS variables (Medical Green `#059669`, Medical Blue `#0284c7`, Light Grey `#f8fafc`). Includes responsive flex/grid layouts, card ribbons, and custom modal overlays.
- **`static/js/script.js`:**
  Client-side interaction engine. Implements debounced autocomplete queries to `/api/autocomplete`, dynamic modal open/close handling, quick-chip triggers, and login pre-fill helpers.
- **`templates/`:**
  Jinja2 templates providing semantic HTML structure, accessibility standards, and clean mobile responsiveness.

---

## 8. College Hackathon Presentation Script

1. **Introduction (1 min):**
   - *"Good morning judges. How many times have you or your loved ones gone to a chemist with a prescription, waited in line, only to hear: 'Sorry, this medicine is not in stock'? In healthcare emergencies, this delay can be dangerous."*
2. **Patient Demo (2 mins):**
   - Open `http://127.0.0.1:5000`.
   - Start typing `Para` in the search bar — show the live autocomplete selecting `Paracetamol 650mg`.
   - Click **Find Medicines**.
   - Show the results:
     - Point out the **Best Price** ribbon on Green Cross Medical Store ($3.10 vs $3.95).
     - Point out the **Low Stock** warning on Metro Care Chemist (only 8 units remaining).
     - Point out the **Out of Stock** card and the **Alternative Nearby Pharmacies** section.
     - Click **Call Store** to show one-click dialing.
3. **Chemist Admin Demo (1.5 mins):**
   - Click **Pharmacy Admin** in the header.
   - Click the `Apex Health (Downtown)` quick-fill chip and log in.
   - Show the admin dashboard: total medicines, in-stock count, low-stock alerts.
   - Click **Update** on any medicine: change stock quantity from `4` to `60` and price to `$2.99`.
   - Go back to public search in an incognito or new tab — show that the medicine is now immediately displayed as **In Stock** and **Best Price**!
4. **Conclusion (30 secs):**
   - *"MEDFIND democratizes medicine accessibility, saves patients valuable time, and empowers local community pharmacies. Thank you!"*

