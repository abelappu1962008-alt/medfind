"""
app.py - MEDFIND Flask Application
Smart Medicine Availability Finder
Web backend providing patient search, pharmacy locator, real-time stock verification,
price comparison, and pharmacy inventory management dashboard.
"""

import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, abort
)
import database

# Initialize the Flask application
app = Flask(__name__)

# Secret key for secure session handling and flash messages
app.secret_key = os.environ.get('MEDFIND_SECRET_KEY', 'medfind_hackathon_secure_token_2026')


# =====================================================================
# TEMPLATE HELPERS & CUSTOM FILTERS
# =====================================================================

@app.template_filter('currency')
def currency_filter(value):
    """Formats numeric prices as currency (e.g. $4.50)."""
    try:
        return f"${float(value):.2f}"
    except (ValueError, TypeError):
        return "$0.00"


@app.template_filter('time_ago')
def time_ago_filter(value):
    """
    Innovative Feature: Human-friendly last stock update indicator.
    Calculates elapsed time between inventory update and current time.
    """
    if not value:
        return "Recently updated"
    try:
        if isinstance(value, str):
            # Parse SQLite default timestamp format 'YYYY-MM-DD HH:MM:SS'
            updated_dt = datetime.strptime(value.split('.')[0], "%Y-%m-%d %H:%M:%S")
        else:
            updated_dt = value
        
        diff = datetime.now() - updated_dt
        seconds = diff.total_seconds()

        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} min{'s' if minutes > 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif seconds < 172800:
            return "Yesterday"
        else:
            days = int(seconds // 86400)
            return f"{days} days ago"
    except Exception:
        return str(value)


# =====================================================================
# AUTHENTICATION DECORATOR FOR ADMIN PAGES
# =====================================================================

def login_required(f):
    """
    Decorator that protects pharmacy administrator routes.
    Redirects unauthenticated users to the admin login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Please log in to access the Pharmacy Administrator portal.", "warning")
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# =====================================================================
# PATIENT FACING ROUTES (NO LOGIN REQUIRED)
# =====================================================================

@app.route('/')
def index():
    """
    MEDFIND Homepage:
    - Large medicine search bar
    - Location selection dropdown
    - Real-time platform statistics
    - 'How It Works' workflow
    - About MedFind & Contact info
    """
    stats = database.get_homepage_stats()
    locations = database.get_all_locations()
    
    # Frequently searched medicines for quick-search chips
    popular_medicines = [
        "Paracetamol 650mg",
        "Amoxicillin 500mg",
        "Metformin 500mg",
        "Cetirizine 10mg",
        "Pantoprazole 40mg",
        "Insulin Glargine"
    ]
    
    return render_template(
        'index.html',
        stats=stats,
        locations=locations,
        popular_medicines=popular_medicines
    )


@app.route('/search')
def search():
    """
    Medicine Search Results Page:
    - Queries medicines across multiple pharmacies
    - Displays available stock quantity and price
    - Flags Best Price badge for cheapest available option
    - Shows stock status (In Stock, Low Stock, Out of Stock)
    - Provides out-of-stock alternative pharmacy suggestions
    - Allows sorting by availability, price, and stock quantity
    """
    query = request.args.get('query', '').strip()
    location = request.args.get('location', '').strip()
    sort_by = request.args.get('sort_by', 'availability').strip()

    # If no search query provided, redirect back to homepage
    if not query:
        flash("Please enter a medicine name to search.", "info")
        return redirect(url_for('index'))

    # Perform database query
    results = database.search_medicines(query=query, location=location, sort_by=sort_by)
    locations = database.get_all_locations()

    # Out-of-stock alternative recommendations:
    # If the user searched a specific location and got 0 results or only out-of-stock results,
    # find other pharmacies outside that location that currently have the medicine.
    alternatives = []
    has_available_stock = any(item['stock_quantity'] > 0 for item in results)

    if not has_available_stock or len(results) == 0:
        alternatives = database.get_alternative_pharmacies(medicine_name=query)

    return render_template(
        'search_results.html',
        query=query,
        location=location,
        sort_by=sort_by,
        results=results,
        locations=locations,
        alternatives=alternatives
    )


@app.route('/pharmacy/<int:pharmacy_id>')
def pharmacy_details(pharmacy_id):
    """
    Detailed Pharmacy Profile:
    - Pharmacy address, telephone number, opening hours
    - Full list of medicines currently in stock at this specific pharmacy
    - Internal search filter to check specific medicine at this pharmacy
    """
    pharmacy = database.get_pharmacy_by_id(pharmacy_id)
    if not pharmacy:
        abort(404, description="Pharmacy not found")

    search_term = request.args.get('q', '').strip()
    inventory = database.get_pharmacy_inventory(pharmacy_id, search_term=search_term)

    return render_template(
        'pharmacy_details.html',
        pharmacy=pharmacy,
        inventory=inventory,
        search_term=search_term
    )


# =====================================================================
# INNOVATIVE REAL-TIME REST APIS
# =====================================================================

@app.route('/api/autocomplete')
def api_autocomplete():
    """
    Innovative Feature: Smart Search Autocomplete
    Returns matching medicine names and categories in JSON format as patient types.
    """
    term = request.args.get('q', '').strip()
    suggestions = database.get_medicine_autocomplete(term)
    return jsonify(suggestions)


@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    """
    Innovative Feature: Instant 2-Hour Stock Hold
    Takes patient name, phone, pharmacy_id, medicine_id and reserves 1 unit.
    Returns reservation confirmation code.
    """
    try:
        pharmacy_id = int(request.form.get('pharmacy_id'))
        medicine_id = int(request.form.get('medicine_id'))
        patient_name = request.form.get('patient_name', '').strip()
        patient_phone = request.form.get('patient_phone', '').strip()

        if not patient_name or not patient_phone:
            return jsonify({'success': False, 'error': 'Name and phone number are required.'}), 400

        code = database.create_reservation(pharmacy_id, medicine_id, patient_name, patient_phone, quantity=1)
        return jsonify({
            'success': True,
            'code': code,
            'message': f"Reserved successfully! Your 2-Hour Pickup Code is {code}. Show this at the counter."
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/locations')
def api_locations():
    """Returns available pharmacy locations in JSON format."""
    locations = database.get_all_locations()
    return jsonify(locations)


# =====================================================================
# PHARMACY ADMINISTRATOR ROUTES (SECURE & PROTECTED)
# =====================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Pharmacy Administrator Login:
    - Secure password check against hashed credentials
    - Pre-populates demo credentials for easy hackathon evaluation
    """
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template('admin_login.html')

        user = database.authenticate_admin(username, password)

        if user:
            # Login successful: store user session details
            session['admin_id'] = user['id']
            session['username'] = user['username']
            session['pharmacy_id'] = user['pharmacy_id']
            session['pharmacy_name'] = user['pharmacy_name']
            session['pharmacy_city'] = user['pharmacy_city']

            flash(f"Welcome back, {user['username']}! Logged in as manager of {user['pharmacy_name']}.", "success")
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin_dashboard'))
        else:
            flash("Invalid administrator username or password. Please try again.", "danger")

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Logs out the pharmacy administrator and clears session."""
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """
    Pharmacy Administrator Inventory Dashboard:
    - Displays key metrics: Total items, In-stock, Low-stock alerts, Out-of-stock
    - Lists only the logged-in pharmacy's medicine inventory
    - Filter by Low Stock (< 10 units) for proactive replenishment
    - Form to add new medicines from catalog
    - Modal/form to update stock quantity and price
    - Pharmacy contact info management
    """
    pharmacy_id = session['pharmacy_id']
    filter_low = (request.args.get('filter') == 'low')
    search_term = request.args.get('q', '').strip()

    # Load metrics, inventory, pharmacy profile, catalog and recent reservations
    metrics = database.get_dashboard_metrics(pharmacy_id)
    inventory = database.get_pharmacy_inventory(pharmacy_id, filter_low_stock=filter_low, search_term=search_term)
    pharmacy = database.get_pharmacy_by_id(pharmacy_id)
    catalog = database.get_all_medicines_catalog()
    reservations = database.get_pharmacy_reservations(pharmacy_id)

    # Identify which medicines are not yet in this pharmacy's inventory
    existing_med_ids = {item['medicine_id'] for item in inventory}
    available_catalog = [med for med in catalog if med['id'] not in existing_med_ids]

    return render_template(
        'admin_dashboard.html',
        metrics=metrics,
        inventory=inventory,
        pharmacy=pharmacy,
        catalog=available_catalog,
        reservations=reservations,
        filter_low=filter_low,
        search_term=search_term
    )


@app.route('/admin/stock/quick-adjust', methods=['POST'])
@login_required
def admin_quick_adjust():
    """1-Click stock adjustments (+5, +10, -1) from dashboard table."""
    pharmacy_id = session['pharmacy_id']
    try:
        medicine_id = int(request.form.get('medicine_id'))
        delta = int(request.form.get('delta', 0))
        database.quick_adjust_stock(pharmacy_id, medicine_id, delta)
        flash(f"Stock count updated by {delta:+d} units successfully!", "success")
    except Exception as e:
        flash(f"Error adjusting stock: {e}", "danger")
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/stock/save', methods=['POST'])
@login_required
def admin_save_stock():
    """
    Adds a medicine to the pharmacy's inventory or updates existing stock quantity and price.
    Changes immediately reflect in patient search results!
    """
    pharmacy_id = session['pharmacy_id']
    try:
        medicine_id = int(request.form.get('medicine_id'))
        quantity = int(request.form.get('stock_quantity', 0))
        price = float(request.form.get('price', 0.0))

        if quantity < 0 or price < 0:
            flash("Stock quantity and price cannot be negative.", "danger")
            return redirect(url_for('admin_dashboard'))

        database.add_or_update_stock(pharmacy_id, medicine_id, quantity, price)
        flash("Inventory updated successfully! Changes are immediately live for patient searches.", "success")
    except (ValueError, TypeError) as err:
        flash(f"Invalid input: {str(err)}", "danger")

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/stock/delete/<int:stock_id>', methods=['POST'])
@login_required
def admin_delete_stock(stock_id):
    """
    Removes a medicine listing from the pharmacy's inventory.
    Only allows deleting records owned by the logged-in pharmacy.
    """
    pharmacy_id = session['pharmacy_id']
    success = database.delete_stock_item(stock_id, pharmacy_id)

    if success:
        flash("Medicine listing removed from your pharmacy inventory.", "info")
    else:
        flash("Unable to remove listing. Record not found or unauthorized.", "danger")

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/pharmacy/update', methods=['POST'])
@login_required
def admin_update_pharmacy():
    """Updates the logged-in pharmacy's name, phone, address, and hours."""
    pharmacy_id = session['pharmacy_id']
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    city = request.form.get('city', '').strip()
    opening_hours = request.form.get('opening_hours', '').strip()

    if not name or not phone or not address or not city:
        flash("Pharmacy name, contact number, address, and city are required.", "danger")
        return redirect(url_for('admin_dashboard'))

    database.update_pharmacy_profile(pharmacy_id, name, phone, address, city, opening_hours)
    session['pharmacy_name'] = name
    session['pharmacy_city'] = city
    flash("Pharmacy contact and location information updated successfully.", "success")

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/medicine/create', methods=['POST'])
@login_required
def admin_create_medicine():
    """
    Allows pharmacy administrators to register a brand new medicine in the master catalog
    and immediately add it to their inventory with initial stock and price.
    """
    pharmacy_id = session['pharmacy_id']
    name = request.form.get('name', '').strip()
    generic_name = request.form.get('generic_name', '').strip()
    category = request.form.get('category', '').strip()
    dosage_form = request.form.get('dosage_form', 'Tablet').strip()
    manufacturer = request.form.get('manufacturer', '').strip()
    description = request.form.get('description', '').strip()
    prescription_req = 1 if request.form.get('prescription_required') == '1' else 0

    try:
        initial_stock = int(request.form.get('stock_quantity', 0))
        price = float(request.form.get('price', 0.0))
    except ValueError:
        flash("Please enter valid numeric values for stock quantity and price.", "danger")
        return redirect(url_for('admin_dashboard'))

    if not name or not generic_name or not category:
        flash("Medicine name, generic formula, and category are required fields.", "danger")
        return redirect(url_for('admin_dashboard'))

    # Insert into master catalog
    new_med_id = database.create_new_medicine(
        name, generic_name, category, dosage_form,
        manufacturer, description, prescription_req
    )

    # Immediately add to this pharmacy's inventory
    database.add_or_update_stock(pharmacy_id, new_med_id, initial_stock, price)
    flash(f"New medicine '{name}' registered in catalog and added to your inventory!", "success")

    return redirect(url_for('admin_dashboard'))


# =====================================================================
# ERROR HANDLERS
# =====================================================================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error_message="The requested page could not be found."), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error_message="An internal server error occurred."), 500


# Application entry point
if __name__ == '__main__':
    # Ensure database tables and sample data exist upon startup
    database.init_db()
    database.seed_sample_data()

    print("\n" + "="*60)
    print("MEDFIND - Smart Medicine Availability Finder is running!")
    print("Web URL: http://127.0.0.1:5000")
    print("Admin Login: http://127.0.0.1:5000/admin/login")
    print("Sample Admin: username='apex_admin' | password='admin123'")
    print("="*60 + "\n")

    # Run local Flask development server
    app.run(host='127.0.0.1', port=5000, debug=True)

