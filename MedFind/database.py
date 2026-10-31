"""
database.py - Database Management Module for MEDFIND
Handles SQLite database connection, table creation, sample demonstration data seeding,
and structured queries for medicines, pharmacies, stock, and administrator accounts.
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Path to the SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medfind.db')


def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Configures row_factory so query results can be accessed like dictionaries.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign key support in SQLite
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initializes the database schema by creating the required tables:
    1. Pharmacies
    2. Medicines
    3. Medicine_Stock
    4. Admin_Users
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table 1: Pharmacies
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            opening_hours TEXT DEFAULT '8:00 AM - 10:00 PM',
            rating REAL DEFAULT 4.6,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Table 2: Medicines (Central catalog of medicines)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            generic_name TEXT NOT NULL,
            category TEXT NOT NULL,
            dosage_form TEXT NOT NULL,
            manufacturer TEXT,
            prescription_required INTEGER DEFAULT 0,
            description TEXT
        )
    """)

    # Table 3: Medicine_Stock (Pharmacy inventory linking pharmacies & medicines)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Medicine_Stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pharmacy_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_demo_data INTEGER DEFAULT 1,
            FOREIGN KEY (pharmacy_id) REFERENCES Pharmacies (id) ON DELETE CASCADE,
            FOREIGN KEY (medicine_id) REFERENCES Medicines (id) ON DELETE CASCADE,
            UNIQUE(pharmacy_id, medicine_id)
        )
    """)

    # Table 4: Admin_Users (Pharmacy owners & administrators)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admin_Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            pharmacy_id INTEGER NOT NULL,
            role TEXT DEFAULT 'pharmacy_admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pharmacy_id) REFERENCES Pharmacies (id) ON DELETE CASCADE
        )
    """)

    # Table 5: Reservations (Patient medicine hold requests)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_code TEXT UNIQUE NOT NULL,
            pharmacy_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            patient_name TEXT NOT NULL,
            patient_phone TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pharmacy_id) REFERENCES Pharmacies (id) ON DELETE CASCADE,
            FOREIGN KEY (medicine_id) REFERENCES Medicines (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("[Database] Tables initialized successfully.")


def seed_sample_data():
    """
    Populates the database with realistic demonstration sample data:
    - 5+ Pharmacies across different locations
    - 15+ Medicines covering varied medical categories
    - Varying stock quantities (high, low, and out of stock)
    - Different medicine prices for accurate price comparison
    - Pharmacy administrator user accounts with hashed passwords
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if data already exists to avoid duplicate seeding
    cursor.execute("SELECT COUNT(*) FROM Pharmacies")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    print("[Database] Seeding sample demonstration data...")

    # 1. Sample Pharmacies (5 verified locations)
    pharmacies = [
        (
            1,
            "Apex Health Pharmacy",
            "142 Central Avenue, Downtown",
            "Downtown",
            "+1 (555) 234-5678",
            "info@apexhealthpharma.com",
            "Open 24/7",
            4.8
        ),
        (
            2,
            "Metro Care Chemist",
            "78 Parkview Avenue, North Hills",
            "North Hills",
            "+1 (555) 345-6789",
            "contact@metrocarechem.com",
            "8:00 AM - 10:30 PM",
            4.6
        ),
        (
            3,
            "Wellness Forever Pharmacy",
            "405 Oakwood Boulevard, Westside Plaza",
            "Westside",
            "+1 (555) 456-7890",
            "support@wellnessforever.com",
            "Open 24/7",
            4.9
        ),
        (
            4,
            "Green Cross Medical Store",
            "12 College Road, University District",
            "University District",
            "+1 (555) 567-8901",
            "greencross@univmed.com",
            "7:30 AM - 11:00 PM",
            4.5
        ),
        (
            5,
            "Lifeline Pharma Hub",
            "99 Sunset Boulevard, East Park",
            "East Park",
            "+1 (555) 678-9012",
            "help@lifelinepharmahub.com",
            "8:00 AM - 9:30 PM",
            4.4
        )
    ]

    cursor.executemany("""
        INSERT INTO Pharmacies (id, name, address, city, phone, email, opening_hours, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, pharmacies)

    # 2. Sample Medicines (17 essential medicines across multiple therapeutic classes)
    medicines = [
        (
            1,
            "Paracetamol 650mg",
            "Acetaminophen",
            "Analgesic & Antipyretic",
            "Tablet",
            "HealthCorp Labs",
            0,
            "Relieves mild to moderate pain and reduces high fever."
        ),
        (
            2,
            "Amoxicillin 500mg",
            "Amoxicillin Trihydrate",
            "Antibiotic",
            "Capsule",
            "BioPharma Global",
            1,
            "Broad-spectrum antibiotic used to treat bacterial infections."
        ),
        (
            3,
            "Metformin 500mg",
            "Metformin Hydrochloride",
            "Antidiabetic",
            "Tablet",
            "SunCare Life Sciences",
            1,
            "First-line medication for the treatment of type 2 diabetes."
        ),
        (
            4,
            "Azithromycin 500mg",
            "Azithromycin",
            "Antibiotic",
            "Tablet",
            "Apex Remedies",
            1,
            "Macrolide antibiotic for chest infections, throat and sinus issues."
        ),
        (
            5,
            "Cetirizine 10mg",
            "Cetirizine Hydrochloride",
            "Antihistamine",
            "Tablet",
            "Allergo Cure Ltd",
            0,
            "Relieves allergy symptoms like watery eyes, runny nose, and sneezing."
        ),
        (
            6,
            "Pantoprazole 40mg",
            "Pantoprazole Sodium",
            "Antacid / PPI",
            "Tablet",
            "GastroHealth Pharma",
            1,
            "Reduces stomach acid, treats acid reflux and GERD."
        ),
        (
            7,
            "Atorvastatin 20mg",
            "Atorvastatin Calcium",
            "Cardiovascular",
            "Tablet",
            "CardioPulse Labs",
            1,
            "Lowers bad cholesterol and triglycerides, reducing cardiovascular risk."
        ),
        (
            8,
            "Amlodipine 5mg",
            "Amlodipine Besylate",
            "Antihypertensive",
            "Tablet",
            "NovaCare Pharma",
            1,
            "Calcium channel blocker used to treat high blood pressure (hypertension)."
        ),
        (
            9,
            "Ibuprofen 400mg",
            "Ibuprofen",
            "NSAID / Pain Relief",
            "Tablet",
            "ReliefMed Formulations",
            0,
            "Anti-inflammatory painkiller for headache, dental pain, and arthritis."
        ),
        (
            10,
            "Montelukast 10mg",
            "Montelukast Sodium",
            "Respiratory",
            "Tablet",
            "AeroBreathe Labs",
            1,
            "Leukotriene receptor antagonist for asthma management and seasonal allergies."
        ),
        (
            11,
            "Omeprazole 20mg",
            "Omeprazole",
            "Gastrointestinal",
            "Capsule",
            "PureHealth Pharma",
            0,
            "Relieves heartburn, treats acid indigestion and stomach ulcers."
        ),
        (
            12,
            "Vitamin D3 60,000 IU",
            "Cholecalciferol",
            "Nutritional Supplement",
            "Capsule",
            "VitaVitality",
            0,
            "High-potency vitamin D supplement for bone density and immune support."
        ),
        (
            13,
            "Cough Relief Syrup 100ml",
            "Dextromethorphan + Guaifenesin",
            "Cough & Cold",
            "Syrup",
            "ChestCare Products",
            0,
            "Dual-action formula relieving dry cough and loosening chest congestion."
        ),
        (
            14,
            "Insulin Glargine 100 IU/ml",
            "Insulin Glargine (rDNA origin)",
            "Diabetes Management",
            "Injection Cartridge",
            "BioGenetics Lab",
            1,
            "Long-acting basal human insulin analogue for glycemic control."
        ),
        (
            15,
            "Losartan Potassium 50mg",
            "Losartan Potassium",
            "Antihypertensive",
            "Tablet",
            "VascularMed Corp",
            1,
            "Angiotensin II receptor blocker used to lower blood pressure and protect kidneys."
        ),
        (
            16,
            "Ciprofloxacin 500mg",
            "Ciprofloxacin",
            "Antibiotic",
            "Tablet",
            "Zenith Life Sciences",
            1,
            "Fluoroquinolone antibiotic for urinary tract and gastrointestinal infections."
        ),
        (
            17,
            "Oral Rehydration Salts (ORS)",
            "WHO Recommended Formulation",
            "Electrolyte Replenisher",
            "Sachet",
            "HydroLife Essentials",
            0,
            "Restores body fluids and essential minerals lost through dehydration."
        )
    ]

    cursor.executemany("""
        INSERT INTO Medicines (id, name, generic_name, category, dosage_form, manufacturer, prescription_required, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, medicines)

    # 3. Medicine Stock records across pharmacies (pharmacy_id, medicine_id, stock_quantity, price, is_demo_data)
    # Notice the realistic variations: some high stock, some low (< 10), some out of stock (0) for comparison
    stock_records = [
        # Pharmacy 1: Apex Health Pharmacy (Downtown)
        (1, 1, 45, 3.50, 1),    # Paracetamol 650mg
        (1, 2, 28, 9.80, 1),    # Amoxicillin 500mg
        (1, 3, 50, 6.20, 1),    # Metformin 500mg
        (1, 4, 15, 14.50, 1),   # Azithromycin 500mg
        (1, 5, 80, 4.00, 1),    # Cetirizine 10mg
        (1, 6, 35, 7.50, 1),    # Pantoprazole 40mg
        (1, 7, 22, 12.00, 1),   # Atorvastatin 20mg
        (1, 8, 40, 5.50, 1),    # Amlodipine 5mg
        (1, 9, 65, 4.25, 1),    # Ibuprofen 400mg
        (1, 10, 4, 11.20, 1),   # Montelukast 10mg (LOW STOCK: 4)
        (1, 11, 30, 6.80, 1),   # Omeprazole 20mg
        (1, 12, 18, 8.50, 1),   # Vitamin D3
        (1, 13, 25, 6.00, 1),   # Cough Relief Syrup
        (1, 14, 8, 42.00, 1),   # Insulin Glargine (LOW STOCK: 8)
        (1, 15, 30, 8.10, 1),   # Losartan 50mg
        (1, 17, 100, 1.50, 1),  # ORS

        # Pharmacy 2: Metro Care Chemist (North Hills)
        (2, 1, 8, 3.20, 1),     # Paracetamol (LOW STOCK: 8, lower price)
        (2, 2, 12, 10.50, 1),   # Amoxicillin
        (2, 3, 35, 5.90, 1),    # Metformin
        (2, 4, 0, 15.00, 1),    # Azithromycin (OUT OF STOCK: 0)
        (2, 5, 50, 3.75, 1),    # Cetirizine
        (2, 6, 6, 7.80, 1),     # Pantoprazole (LOW STOCK: 6)
        (2, 7, 18, 11.50, 1),   # Atorvastatin
        (2, 8, 25, 5.25, 1),    # Amlodipine
        (2, 9, 40, 4.10, 1),    # Ibuprofen
        (2, 11, 20, 6.50, 1),   # Omeprazole
        (2, 12, 14, 8.20, 1),   # Vitamin D3
        (2, 13, 10, 5.80, 1),   # Cough Relief Syrup
        (2, 15, 16, 7.90, 1),   # Losartan 50mg
        (2, 16, 22, 13.50, 1),  # Ciprofloxacin

        # Pharmacy 3: Wellness Forever Pharmacy (Westside)
        (3, 1, 120, 3.95, 1),   # Paracetamol
        (3, 2, 45, 9.40, 1),    # Amoxicillin
        (3, 3, 80, 6.00, 1),    # Metformin
        (3, 4, 30, 13.90, 1),   # Azithromycin (Best Price!)
        (3, 5, 110, 3.50, 1),   # Cetirizine (Best Price!)
        (3, 6, 60, 7.20, 1),    # Pantoprazole (Best Price!)
        (3, 7, 45, 11.00, 1),   # Atorvastatin (Best Price!)
        (3, 8, 55, 5.00, 1),    # Amlodipine (Best Price!)
        (3, 9, 90, 3.90, 1),    # Ibuprofen (Best Price!)
        (3, 10, 25, 10.50, 1),  # Montelukast
        (3, 11, 50, 6.20, 1),   # Omeprazole
        (3, 12, 35, 8.00, 1),   # Vitamin D3
        (3, 13, 40, 6.25, 1),   # Cough Relief Syrup
        (3, 14, 15, 39.50, 1),  # Insulin Glargine (Best Price!)
        (3, 15, 40, 7.80, 1),   # Losartan 50mg
        (3, 16, 35, 12.80, 1),  # Ciprofloxacin (Best Price!)
        (3, 17, 150, 1.40, 1),  # ORS

        # Pharmacy 4: Green Cross Medical Store (University District)
        (4, 1, 35, 3.10, 1),    # Paracetamol (Best Price: $3.10!)
        (4, 2, 20, 9.60, 1),    # Amoxicillin
        (4, 3, 25, 5.80, 1),    # Metformin (Best Price!)
        (4, 4, 10, 14.80, 1),   # Azithromycin
        (4, 5, 45, 3.80, 1),    # Cetirizine
        (4, 6, 20, 7.60, 1),    # Pantoprazole
        (4, 7, 0, 12.50, 1),    # Atorvastatin (OUT OF STOCK: 0)
        (4, 8, 30, 5.40, 1),    # Amlodipine
        (4, 9, 50, 4.00, 1),    # Ibuprofen
        (4, 10, 18, 10.90, 1),  # Montelukast
        (4, 12, 3, 8.75, 1),    # Vitamin D3 (LOW STOCK: 3)
        (4, 13, 15, 5.50, 1),   # Cough Relief Syrup (Best Price!)
        (4, 15, 20, 8.00, 1),   # Losartan
        (4, 16, 18, 13.00, 1),  # Ciprofloxacin
        (4, 17, 60, 1.25, 1),   # ORS (Best Price: $1.25!)

        # Pharmacy 5: Lifeline Pharma Hub (East Park)
        (5, 1, 0, 3.75, 1),     # Paracetamol (OUT OF STOCK: 0 - demonstrates out-of-stock suggestions!)
        (5, 2, 15, 10.00, 1),   # Amoxicillin
        (5, 3, 40, 6.10, 1),    # Metformin
        (5, 4, 12, 14.20, 1),   # Azithromycin
        (5, 5, 30, 4.20, 1),    # Cetirizine
        (5, 6, 25, 7.90, 1),    # Pantoprazole
        (5, 7, 15, 12.20, 1),   # Atorvastatin
        (5, 8, 18, 5.60, 1),    # Amlodipine
        (5, 9, 20, 4.30, 1),    # Ibuprofen
        (5, 10, 5, 11.50, 1),   # Montelukast (LOW STOCK: 5)
        (5, 11, 22, 6.90, 1),   # Omeprazole
        (5, 12, 20, 8.40, 1),   # Vitamin D3
        (5, 13, 0, 5.90, 1),    # Cough Relief (OUT OF STOCK: 0)
        (5, 14, 6, 44.00, 1),   # Insulin Glargine (LOW STOCK: 6)
        (5, 15, 12, 8.30, 1),   # Losartan
        (5, 16, 14, 13.40, 1),  # Ciprofloxacin
        (5, 17, 45, 1.50, 1)    # ORS
    ]

    cursor.executemany("""
        INSERT INTO Medicine_Stock (pharmacy_id, medicine_id, stock_quantity, price, is_demo_data)
        VALUES (?, ?, ?, ?, ?)
    """, stock_records)

    # 4. Pharmacy Administrator Accounts (Secure password hashing)
    # Default demonstration password for all demo admins: 'admin123'
    hashed_pwd = generate_password_hash("admin123")

    admins = [
        (1, "apex_admin", hashed_pwd, 1, "pharmacy_admin"),
        (2, "metro_admin", hashed_pwd, 2, "pharmacy_admin"),
        (3, "wellness_admin", hashed_pwd, 3, "pharmacy_admin"),
        (4, "greencross_admin", hashed_pwd, 4, "pharmacy_admin"),
        (5, "lifeline_admin", hashed_pwd, 5, "pharmacy_admin")
    ]

    cursor.executemany("""
        INSERT INTO Admin_Users (id, username, password_hash, pharmacy_id, role)
        VALUES (?, ?, ?, ?, ?)
    """, admins)

    conn.commit()
    conn.close()
    print("[Database] Sample data seeded successfully with 5 pharmacies, 17 medicines, and 5 admin accounts.")


# =====================================================================
# QUERY AND BUSINESS LOGIC FUNCTIONS
# =====================================================================

def search_medicines(query=None, location=None, sort_by='availability'):
    """
    Core Search Engine:
    Searches across medicines and pharmacy inventories.
    Returns pharmacies stocking the medicine, with quantity, price, location,
    contact info, and stock status.
    
    Sorting options:
    - 'availability': In stock first (higher stock), then out of stock
    - 'price_asc': Lowest price first (price comparison)
    - 'price_desc': Highest price first
    - 'stock_desc': Highest stock quantity first
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            m.id AS medicine_id,
            m.name AS medicine_name,
            m.generic_name,
            m.category,
            m.dosage_form,
            m.prescription_required,
            m.description,
            p.id AS pharmacy_id,
            p.name AS pharmacy_name,
            p.address AS pharmacy_address,
            p.city AS pharmacy_city,
            p.phone AS pharmacy_phone,
            p.opening_hours,
            p.rating AS pharmacy_rating,
            s.id AS stock_id,
            s.stock_quantity,
            s.price,
            s.last_updated,
            s.is_demo_data,
            CASE
                WHEN s.stock_quantity > 10 THEN 'In Stock'
                WHEN s.stock_quantity > 0 THEN 'Low Stock'
                ELSE 'Out of Stock'
            END AS availability_status
        FROM Medicine_Stock s
        JOIN Medicines m ON s.medicine_id = m.id
        JOIN Pharmacies p ON s.pharmacy_id = p.id
        WHERE 1=1
    """
    params = []

    # Filter by medicine name or generic name (case-insensitive substring match)
    if query and query.strip():
        sql += " AND (m.name LIKE ? OR m.generic_name LIKE ? OR m.category LIKE ?)"
        term = f"%{query.strip()}%"
        params.extend([term, term, term])

    # Filter by pharmacy location / city
    if location and location.strip() and location.strip().lower() != 'all':
        sql += " AND (p.city LIKE ? OR p.address LIKE ?)"
        loc_term = f"%{location.strip()}%"
        params.extend([loc_term, loc_term])

    # Dynamic sorting
    if sort_by == 'price_asc':
        # Best price first (available items prioritized)
        sql += " ORDER BY (s.stock_quantity > 0) DESC, s.price ASC, s.stock_quantity DESC"
    elif sort_by == 'price_desc':
        sql += " ORDER BY (s.stock_quantity > 0) DESC, s.price DESC"
    elif sort_by == 'stock_desc':
        sql += " ORDER BY s.stock_quantity DESC, s.price ASC"
    else:  # 'availability' (default)
        # Show in-stock items first, then low-stock, then out-of-stock
        sql += " ORDER BY (s.stock_quantity > 0) DESC, s.stock_quantity DESC, s.price ASC"

    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()

    # Convert rows to python dicts and identify lowest price for highlighting
    results_list = [dict(row) for row in results]

    # Calculate best price among available items
    available_prices = [r['price'] for r in results_list if r['stock_quantity'] > 0]
    min_price = min(available_prices) if available_prices else None

    # Realistic simulated distance mapping per pharmacy id
    dist_map = {1: 0.8, 2: 1.4, 3: 2.1, 4: 1.1, 5: 2.7}

    for item in results_list:
        item['is_best_price'] = (min_price is not None and item['price'] == min_price and item['stock_quantity'] > 0)
        item['distance_miles'] = dist_map.get(item['pharmacy_id'], 1.5)
        # Visual stock gauge percentage (relative to a typical healthy stock of 50 units)
        qty = item['stock_quantity']
        item['stock_percent'] = min(100, int((qty / 50.0) * 100)) if qty > 0 else 0
        item['is_open_247'] = "24/7" in item.get('opening_hours', '')

    return results_list


def get_alternative_pharmacies(medicine_name, exclude_pharmacy_id=None):
    """
    Innovative Feature: Out of Stock Suggestions
    If a medicine is out of stock at a selected pharmacy or location,
    find other nearby pharmacies that currently have available stock.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            m.name AS medicine_name,
            p.id AS pharmacy_id,
            p.name AS pharmacy_name,
            p.city AS pharmacy_city,
            p.phone AS pharmacy_phone,
            p.address AS pharmacy_address,
            s.stock_quantity,
            s.price,
            s.last_updated
        FROM Medicine_Stock s
        JOIN Medicines m ON s.medicine_id = m.id
        JOIN Pharmacies p ON s.pharmacy_id = p.id
        WHERE m.name LIKE ? AND s.stock_quantity > 0
    """
    params = [f"%{medicine_name}%"]

    if exclude_pharmacy_id:
        sql += " AND p.id != ?"
        params.append(exclude_pharmacy_id)

    sql += " ORDER BY s.stock_quantity DESC, s.price ASC LIMIT 4"

    cursor.execute(sql, params)
    alternatives = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return alternatives


def get_all_locations():
    """Returns a distinct list of pharmacy locations/cities for the filter dropdown."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT city FROM Pharmacies ORDER BY city ASC")
    locations = [row['city'] for row in cursor.fetchall()]
    conn.close()
    return locations


def get_medicine_autocomplete(term):
    """
    Innovative Feature: Autocomplete
    Returns quick suggestions of medicine names matching user input.
    """
    if not term or len(term.strip()) < 1:
        return []
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT name, generic_name, category 
        FROM Medicines 
        WHERE name LIKE ? OR generic_name LIKE ?
        ORDER BY name ASC 
        LIMIT 8
    """, (f"%{term.strip()}%", f"%{term.strip()}%"))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results


def get_pharmacy_by_id(pharmacy_id):
    """Returns details for a single pharmacy."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pharmacies WHERE id = ?", (pharmacy_id,))
    pharmacy = cursor.fetchone()
    conn.close()
    return dict(pharmacy) if pharmacy else None


def get_pharmacy_inventory(pharmacy_id, filter_low_stock=False, search_term=None):
    """
    Returns inventory listed by a specific pharmacy.
    Allows filtering by low stock (< 10) and searching within pharmacy stock.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            s.id AS stock_id,
            s.stock_quantity,
            s.price,
            s.last_updated,
            s.is_demo_data,
            m.id AS medicine_id,
            m.name AS medicine_name,
            m.generic_name,
            m.category,
            m.dosage_form,
            m.prescription_required,
            m.manufacturer,
            CASE
                WHEN s.stock_quantity > 10 THEN 'In Stock'
                WHEN s.stock_quantity > 0 THEN 'Low Stock'
                ELSE 'Out of Stock'
            END AS availability_status
        FROM Medicine_Stock s
        JOIN Medicines m ON s.medicine_id = m.id
        WHERE s.pharmacy_id = ?
    """
    params = [pharmacy_id]

    if filter_low_stock:
        sql += " AND s.stock_quantity <= 10"

    if search_term and search_term.strip():
        sql += " AND (m.name LIKE ? OR m.generic_name LIKE ?)"
        term = f"%{search_term.strip()}%"
        params.extend([term, term])

    sql += " ORDER BY s.stock_quantity ASC, m.name ASC"

    cursor.execute(sql, params)
    inventory = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return inventory


def get_all_medicines_catalog():
    """Returns all available medicines from the central catalog for pharmacy admins to add."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Medicines ORDER BY name ASC")
    medicines = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return medicines


def add_or_update_stock(pharmacy_id, medicine_id, quantity, price):
    """
    Adds a new medicine to pharmacy inventory or updates existing stock quantity and price.
    Immediately updates the last_updated timestamp and marks it as live (is_demo_data = 0).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if this medicine is already in pharmacy's inventory
    cursor.execute("""
        SELECT id FROM Medicine_Stock 
        WHERE pharmacy_id = ? AND medicine_id = ?
    """, (pharmacy_id, medicine_id))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE Medicine_Stock 
            SET stock_quantity = ?, price = ?, last_updated = ?, is_demo_data = 0
            WHERE id = ?
        """, (quantity, price, now, existing['id']))
    else:
        cursor.execute("""
            INSERT INTO Medicine_Stock (pharmacy_id, medicine_id, stock_quantity, price, last_updated, is_demo_data)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (pharmacy_id, medicine_id, quantity, price, now))

    conn.commit()
    conn.close()
    return True


def delete_stock_item(stock_id, pharmacy_id):
    """Removes a medicine listing from a pharmacy's inventory (only if owned by this pharmacy)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM Medicine_Stock 
        WHERE id = ? AND pharmacy_id = ?
    """, (stock_id, pharmacy_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0


def update_pharmacy_profile(pharmacy_id, name, phone, address, city, opening_hours):
    """Updates the pharmacy's contact and operational information."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Pharmacies 
        SET name = ?, phone = ?, address = ?, city = ?, opening_hours = ?
        WHERE id = ?
    """, (name, phone, address, city, opening_hours, pharmacy_id))
    conn.commit()
    conn.close()
    return True


def create_new_medicine(name, generic_name, category, dosage_form, manufacturer, description, prescription_req=0):
    """Adds a new medicine to the master catalog."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Medicines (name, generic_name, category, dosage_form, manufacturer, description, prescription_required)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, generic_name, category, dosage_form, manufacturer, description, prescription_req))
    med_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return med_id


def authenticate_admin(username, password):
    """
    Validates pharmacy admin login credentials.
    Returns admin row dictionary (including pharmacy details) if valid, else None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.username, a.password_hash, a.pharmacy_id, a.role,
               p.name AS pharmacy_name, p.city AS pharmacy_city
        FROM Admin_Users a
        JOIN Pharmacies p ON a.pharmacy_id = p.id
        WHERE a.username = ?
    """, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None


def get_dashboard_metrics(pharmacy_id):
    """
    Returns summary statistics for the admin dashboard:
    - Total items
    - In-stock count
    - Low-stock count (<= 10)
    - Out-of-stock count (0)
    - Active reservations count
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_medicines,
            SUM(CASE WHEN stock_quantity > 10 THEN 1 ELSE 0 END) AS in_stock_count,
            SUM(CASE WHEN stock_quantity > 0 AND stock_quantity <= 10 THEN 1 ELSE 0 END) AS low_stock_count,
            SUM(CASE WHEN stock_quantity = 0 THEN 1 ELSE 0 END) AS out_of_stock_count
        FROM Medicine_Stock
        WHERE pharmacy_id = ?
    """, (pharmacy_id,))
    metrics = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*) AS active_reservations
        FROM Reservations
        WHERE pharmacy_id = ? AND status = 'Active'
    """, (pharmacy_id,))
    res_row = cursor.fetchone()
    conn.close()

    res_dict = dict(metrics) if metrics else {
        'total_medicines': 0,
        'in_stock_count': 0,
        'low_stock_count': 0,
        'out_of_stock_count': 0
    }
    res_dict['active_reservations'] = res_row['active_reservations'] if res_row else 0
    return res_dict


def create_reservation(pharmacy_id, medicine_id, patient_name, patient_phone, quantity=1):
    """
    Innovative Feature: 2-Hour Pickup Hold
    Allows patients to lock in medicine stock for 2 hours before driving.
    Generates a unique reservation tracking code (e.g. MED-8421).
    """
    import random
    code = f"MED-{random.randint(1000, 9999)}"
    conn = get_db_connection()
    cursor = conn.cursor()

    # Decrement stock by reserved quantity if available
    cursor.execute("""
        UPDATE Medicine_Stock 
        SET stock_quantity = MAX(0, stock_quantity - ?),
            last_updated = CURRENT_TIMESTAMP
        WHERE pharmacy_id = ? AND medicine_id = ?
    """, (quantity, pharmacy_id, medicine_id))

    cursor.execute("""
        INSERT INTO Reservations (reservation_code, pharmacy_id, medicine_id, patient_name, patient_phone, quantity, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Active')
    """, (code, pharmacy_id, medicine_id, patient_name, patient_phone, quantity))

    conn.commit()
    conn.close()
    return code


def get_pharmacy_reservations(pharmacy_id):
    """Returns active and recent patient pickup reservations for a pharmacy."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, r.reservation_code, r.patient_name, r.patient_phone, r.quantity,
               r.status, r.created_at, m.name AS medicine_name, s.price
        FROM Reservations r
        JOIN Medicines m ON r.medicine_id = m.id
        LEFT JOIN Medicine_Stock s ON (s.pharmacy_id = r.pharmacy_id AND s.medicine_id = r.medicine_id)
        WHERE r.pharmacy_id = ?
        ORDER BY r.created_at DESC LIMIT 15
    """, (pharmacy_id,))
    reservations = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return reservations


def quick_adjust_stock(pharmacy_id, medicine_id, delta):
    """1-Click instant stock booster/decrement (+5, +10, -1) for fast admin operations."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Medicine_Stock 
        SET stock_quantity = MAX(0, stock_quantity + ?),
            last_updated = CURRENT_TIMESTAMP,
            is_demo_data = 0
        WHERE pharmacy_id = ? AND medicine_id = ?
    """, (delta, pharmacy_id, medicine_id))
    conn.commit()
    conn.close()
    return True



def get_homepage_stats():
    """Returns general platform statistics to display on the public homepage."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total_pharmacies FROM Pharmacies")
    p_count = cursor.fetchone()['total_pharmacies']

    cursor.execute("SELECT COUNT(*) AS total_medicines FROM Medicines")
    m_count = cursor.fetchone()['total_medicines']

    cursor.execute("SELECT COUNT(*) AS total_stock_units, SUM(stock_quantity) AS total_units FROM Medicine_Stock")
    s_row = cursor.fetchone()
    conn.close()

    return {
        'total_pharmacies': p_count,
        'total_medicines': m_count,
        'total_units': s_row['total_units'] or 0
    }


# Auto-initialize database and sample data if executed directly
if __name__ == '__main__':
    init_db()
    seed_sample_data()

