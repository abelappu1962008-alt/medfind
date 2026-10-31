"""
test_app.py - Automated Unit & Integration Tests for MEDFIND
Tests all backend routes, database queries, admin authentication,
stock management, and public search verification.
"""

import sys
import os
import unittest

# Add MedFind directory to path
medfind_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MedFind')
sys.path.insert(0, medfind_dir)

import app
import database


class MedFindTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.app.test_client()

        # Re-initialize test database
        database.init_db()
        database.seed_sample_data()

    def test_database_seeded_data(self):
        """Verifies database contains at least 5 pharmacies and 15 medicines."""
        conn = database.get_db_connection()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM Pharmacies")
        p_count = c.fetchone()[0]
        self.assertGreaterEqual(p_count, 5, "Should have at least 5 pharmacies")

        c.execute("SELECT COUNT(*) FROM Medicines")
        m_count = c.fetchone()[0]
        self.assertGreaterEqual(m_count, 15, "Should have at least 15 medicines")

        c.execute("SELECT COUNT(*) FROM Admin_Users")
        a_count = c.fetchone()[0]
        self.assertGreaterEqual(a_count, 5, "Should have at least 5 admin users")
        
        conn.close()
        print(f"[TEST PASS] Database verified: {p_count} pharmacies, {m_count} medicines, {a_count} admins.")

    def test_homepage(self):
        """Tests that the homepage loads with status code 200 and proper brand text."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MED", response.data)
        self.assertIn(b"FIND", response.data)
        self.assertIn(b"Find Medicines. Save Time. Stay Informed.", response.data)
        print("[TEST PASS] Homepage loaded successfully.")

    def test_medicine_search(self):
        """Tests public medicine search with price comparison and stock status."""
        response = self.client.get('/search?query=Paracetamol')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Paracetamol", response.data)
        self.assertIn(b"Best Price", response.data)
        self.assertIn(b"In Stock", response.data)
        print("[TEST PASS] Public medicine search works with Best Price ribbon.")

    def test_medicine_search_unavailable(self):
        """Tests searching for a medicine that does not exist."""
        response = self.client.get('/search?query=NonExistentMedicineXYZ')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sorry, this medicine is currently unavailable in the listed pharmacies.", response.data)
        print("[TEST PASS] Search unavailability message displayed properly.")

    def test_autocomplete_api(self):
        """Tests the innovative real-time autocomplete JSON API."""
        response = self.client.get('/api/autocomplete?q=para')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsInstance(json_data, list)
        self.assertGreaterEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['name'], "Paracetamol 650mg")
        print(f"[TEST PASS] Autocomplete API returned {len(json_data)} suggestions.")

    def test_pharmacy_profile_page(self):
        """Tests individual pharmacy details page."""
        response = self.client.get('/pharmacy/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Apex Health Pharmacy", response.data)
        self.assertIn(b"Downtown", response.data)
        print("[TEST PASS] Pharmacy details page loaded successfully.")

    def test_admin_authentication_and_dashboard(self):
        """Tests admin login, session protection, inventory update, and logout."""
        # 1. Unauthenticated access to dashboard should redirect to login
        dash_unauth = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b"Please log in to access the Pharmacy Administrator portal.", dash_unauth.data)

        # 2. Login with incorrect password
        bad_login = self.client.post('/admin/login', data={
            'username': 'apex_admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b"Invalid administrator username or password.", bad_login.data)

        # 3. Login with correct password
        good_login = self.client.post('/admin/login', data={
            'username': 'apex_admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(good_login.status_code, 200)
        self.assertIn(b"Apex Health Pharmacy", good_login.data)
        self.assertIn(b"Listed Medicines", good_login.data)

        # 4. Admin updates stock: change medicine #1 (Paracetamol) to 88 units at $2.75
        update_resp = self.client.post('/admin/stock/save', data={
            'medicine_id': 1,
            'stock_quantity': 88,
            'price': 2.75
        }, follow_redirects=True)
        self.assertIn(b"Inventory updated successfully!", update_resp.data)

        # 5. Verify the public search immediately reflects the new stock quantity 88 and price $2.75
        search_resp = self.client.get('/search?query=Paracetamol')
        self.assertIn(b"88", search_resp.data)
        self.assertIn(b"$2.75", search_resp.data)

        # 6. Logout
        logout_resp = self.client.get('/admin/logout', follow_redirects=True)
        self.assertIn(b"You have been securely logged out.", logout_resp.data)
        print("[TEST PASS] Full Admin workflow (auth, dashboard, stock update, public reflection, logout) tested successfully.")


if __name__ == '__main__':
    unittest.main()

