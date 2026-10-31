git/**
 * MEDFIND – Smart Medicine Availability Finder
 * Complete Standalone Web Application Engine (app.js)
 * Implements full client-side relational storage, real-time multi-pharmacy search,
 * price comparison engine, 2-hour hold reservation token generator, and chemist admin console.
 */

// =====================================================================
// 1. DEFAULT DATASETS (PERSISTED IN LOCALSTORAGE)
// =====================================================================

const DEFAULT_PHARMACIES = [
  {
    id: 1,
    name: "Apex Health Pharmacy",
    address: "142 Central Avenue, Downtown",
    city: "Downtown",
    phone: "+1 (555) 234-5678",
    opening_hours: "Open 24/7",
    rating: 4.8,
    distance_miles: 0.8,
    is_open_247: true
  },
  {
    id: 2,
    name: "Metro Care Chemist",
    address: "78 Parkview Avenue, North Hills",
    city: "North Hills",
    phone: "+1 (555) 345-6789",
    opening_hours: "8:00 AM - 10:30 PM",
    rating: 4.6,
    distance_miles: 1.4,
    is_open_247: false
  },
  {
    id: 3,
    name: "Wellness Forever Pharmacy",
    address: "405 Oakwood Boulevard, Westside Plaza",
    city: "Westside",
    phone: "+1 (555) 456-7890",
    opening_hours: "Open 24/7",
    rating: 4.9,
    distance_miles: 2.1,
    is_open_247: true
  },
  {
    id: 4,
    name: "Green Cross Medical Store",
    address: "12 College Road, University District",
    city: "University District",
    phone: "+1 (555) 567-8901",
    opening_hours: "7:30 AM - 11:00 PM",
    rating: 4.5,
    distance_miles: 1.1,
    is_open_247: false
  },
  {
    id: 5,
    name: "Lifeline Pharma Hub",
    address: "99 Sunset Boulevard, East Park",
    city: "East Park",
    phone: "+1 (555) 678-9012",
    opening_hours: "8:00 AM - 9:30 PM",
    rating: 4.4,
    distance_miles: 2.7,
    is_open_247: false
  }
];

const DEFAULT_MEDICINES = [
  { id: 1, name: "Paracetamol 650mg", generic_name: "Acetaminophen", category: "Analgesic & Antipyretic", dosage_form: "Tablet", prescription_required: 0 },
  { id: 2, name: "Amoxicillin 500mg", generic_name: "Amoxicillin Trihydrate", category: "Antibiotic", dosage_form: "Capsule", prescription_required: 1 },
  { id: 3, name: "Metformin 500mg", generic_name: "Metformin Hydrochloride", category: "Antidiabetic", dosage_form: "Tablet", prescription_required: 1 },
  { id: 4, name: "Azithromycin 500mg", generic_name: "Azithromycin", category: "Antibiotic", dosage_form: "Tablet", prescription_required: 1 },
  { id: 5, name: "Cetirizine 10mg", generic_name: "Cetirizine Hydrochloride", category: "Antihistamine", dosage_form: "Tablet", prescription_required: 0 },
  { id: 6, name: "Pantoprazole 40mg", generic_name: "Pantoprazole Sodium", category: "Antacid / PPI", dosage_form: "Tablet", prescription_required: 1 },
  { id: 7, name: "Atorvastatin 20mg", generic_name: "Atorvastatin Calcium", category: "Cardiovascular", dosage_form: "Tablet", prescription_required: 1 },
  { id: 8, name: "Amlodipine 5mg", generic_name: "Amlodipine Besylate", category: "Antihypertensive", dosage_form: "Tablet", prescription_required: 1 },
  { id: 9, name: "Ibuprofen 400mg", generic_name: "Ibuprofen", category: "NSAID / Pain Relief", dosage_form: "Tablet", prescription_required: 0 },
  { id: 10, name: "Montelukast 10mg", generic_name: "Montelukast Sodium", category: "Respiratory", dosage_form: "Tablet", prescription_required: 1 },
  { id: 11, name: "Omeprazole 20mg", generic_name: "Omeprazole", category: "Gastrointestinal", dosage_form: "Capsule", prescription_required: 0 },
  { id: 12, name: "Vitamin D3 60,000 IU", generic_name: "Cholecalciferol", category: "Nutritional Supplement", dosage_form: "Capsule", prescription_required: 0 },
  { id: 13, name: "Cough Relief Syrup 100ml", generic_name: "Dextromethorphan + Guaifenesin", category: "Cough & Cold", dosage_form: "Syrup", prescription_required: 0 },
  { id: 14, name: "Insulin Glargine 100 IU/ml", generic_name: "Insulin Glargine (rDNA)", category: "Diabetes Management", dosage_form: "Injection Cartridge", prescription_required: 1 },
  { id: 15, name: "Losartan Potassium 50mg", generic_name: "Losartan Potassium", category: "Antihypertensive", dosage_form: "Tablet", prescription_required: 1 },
  { id: 16, name: "Ciprofloxacin 500mg", generic_name: "Ciprofloxacin", category: "Antibiotic", dosage_form: "Tablet", prescription_required: 1 },
  { id: 17, name: "Oral Rehydration Salts (ORS)", generic_name: "WHO Formulation", category: "Electrolyte Replenisher", dosage_form: "Sachet", prescription_required: 0 }
];

// Initial stock matrix (pharmacy_id, medicine_id, stock_quantity, price)
const DEFAULT_STOCKS = [
  // Apex Health (Downtown)
  { pharmacy_id: 1, medicine_id: 1, stock_quantity: 45, price: 3.50, updated_mins_ago: 5 },
  { pharmacy_id: 1, medicine_id: 2, stock_quantity: 28, price: 9.80, updated_mins_ago: 12 },
  { pharmacy_id: 1, medicine_id: 3, stock_quantity: 50, price: 6.20, updated_mins_ago: 20 },
  { pharmacy_id: 1, medicine_id: 4, stock_quantity: 15, price: 14.50, updated_mins_ago: 35 },
  { pharmacy_id: 1, medicine_id: 5, stock_quantity: 80, price: 4.00, updated_mins_ago: 8 },
  { pharmacy_id: 1, medicine_id: 6, stock_quantity: 35, price: 7.50, updated_mins_ago: 14 },
  { pharmacy_id: 1, medicine_id: 7, stock_quantity: 22, price: 12.00, updated_mins_ago: 40 },
  { pharmacy_id: 1, medicine_id: 8, stock_quantity: 40, price: 5.50, updated_mins_ago: 15 },
  { pharmacy_id: 1, medicine_id: 9, stock_quantity: 65, price: 4.25, updated_mins_ago: 10 },
  { pharmacy_id: 1, medicine_id: 10, stock_quantity: 4, price: 11.20, updated_mins_ago: 25 }, // Low stock
  { pharmacy_id: 1, medicine_id: 14, stock_quantity: 8, price: 42.00, updated_mins_ago: 18 }, // Low stock

  // Metro Care (North Hills)
  { pharmacy_id: 2, medicine_id: 1, stock_quantity: 8, price: 3.20, updated_mins_ago: 15 },  // Low stock
  { pharmacy_id: 2, medicine_id: 2, stock_quantity: 12, price: 10.50, updated_mins_ago: 28 },
  { pharmacy_id: 2, medicine_id: 3, stock_quantity: 35, price: 5.90, updated_mins_ago: 33 },
  { pharmacy_id: 2, medicine_id: 4, stock_quantity: 0, price: 15.00, updated_mins_ago: 50 },  // Out of stock
  { pharmacy_id: 2, medicine_id: 5, stock_quantity: 50, price: 3.75, updated_mins_ago: 12 },
  { pharmacy_id: 2, medicine_id: 6, stock_quantity: 6, price: 7.80, updated_mins_ago: 16 },   // Low stock
  { pharmacy_id: 2, medicine_id: 7, stock_quantity: 18, price: 11.50, updated_mins_ago: 22 },
  { pharmacy_id: 2, medicine_id: 8, stock_quantity: 25, price: 5.25, updated_mins_ago: 30 },
  { pharmacy_id: 2, medicine_id: 9, stock_quantity: 40, price: 4.10, updated_mins_ago: 18 },

  // Wellness Forever (Westside)
  { pharmacy_id: 3, medicine_id: 1, stock_quantity: 120, price: 3.95, updated_mins_ago: 2 },
  { pharmacy_id: 3, medicine_id: 2, stock_quantity: 45, price: 9.40, updated_mins_ago: 10 },
  { pharmacy_id: 3, medicine_id: 3, stock_quantity: 80, price: 6.00, updated_mins_ago: 15 },
  { pharmacy_id: 3, medicine_id: 4, stock_quantity: 30, price: 13.90, updated_mins_ago: 7 }, // Best Price
  { pharmacy_id: 3, medicine_id: 5, stock_quantity: 110, price: 3.50, updated_mins_ago: 4 }, // Best Price
  { pharmacy_id: 3, medicine_id: 6, stock_quantity: 60, price: 7.20, updated_mins_ago: 8 },  // Best Price
  { pharmacy_id: 3, medicine_id: 7, stock_quantity: 45, price: 11.00, updated_mins_ago: 11 }, // Best Price
  { pharmacy_id: 3, medicine_id: 8, stock_quantity: 55, price: 5.00, updated_mins_ago: 9 },  // Best Price
  { pharmacy_id: 3, medicine_id: 9, stock_quantity: 90, price: 3.90, updated_mins_ago: 6 },  // Best Price
  { pharmacy_id: 3, medicine_id: 14, stock_quantity: 15, price: 39.50, updated_mins_ago: 5 }, // Best Price

  // Green Cross (University District)
  { pharmacy_id: 4, medicine_id: 1, stock_quantity: 35, price: 3.10, updated_mins_ago: 3 },  // Best Price ($3.10)
  { pharmacy_id: 4, medicine_id: 2, stock_quantity: 20, price: 9.60, updated_mins_ago: 14 },
  { pharmacy_id: 4, medicine_id: 3, stock_quantity: 25, price: 5.80, updated_mins_ago: 19 }, // Best Price
  { pharmacy_id: 4, medicine_id: 4, stock_quantity: 10, price: 14.80, updated_mins_ago: 22 },
  { pharmacy_id: 4, medicine_id: 5, stock_quantity: 45, price: 3.80, updated_mins_ago: 12 },
  { pharmacy_id: 4, medicine_id: 7, stock_quantity: 0, price: 12.50, updated_mins_ago: 45 },  // Out of stock
  { pharmacy_id: 4, medicine_id: 8, stock_quantity: 30, price: 5.40, updated_mins_ago: 20 },
  { pharmacy_id: 4, medicine_id: 9, stock_quantity: 50, price: 4.00, updated_mins_ago: 16 },
  { pharmacy_id: 4, medicine_id: 17, stock_quantity: 60, price: 1.25, updated_mins_ago: 15 }, // Best Price

  // Lifeline Pharma (East Park)
  { pharmacy_id: 5, medicine_id: 1, stock_quantity: 0, price: 3.75, updated_mins_ago: 60 },  // Out of stock
  { pharmacy_id: 5, medicine_id: 2, stock_quantity: 15, price: 10.00, updated_mins_ago: 30 },
  { pharmacy_id: 5, medicine_id: 3, stock_quantity: 40, price: 6.10, updated_mins_ago: 25 },
  { pharmacy_id: 5, medicine_id: 4, stock_quantity: 12, price: 14.20, updated_mins_ago: 35 },
  { pharmacy_id: 5, medicine_id: 5, stock_quantity: 30, price: 4.20, updated_mins_ago: 20 },
  { pharmacy_id: 5, medicine_id: 10, stock_quantity: 5, price: 11.50, updated_mins_ago: 22 }, // Low stock
  { pharmacy_id: 5, medicine_id: 14, stock_quantity: 6, price: 44.00, updated_mins_ago: 19 }  // Low stock
];

const DEFAULT_RESERVATIONS = [
  { id: 1, code: "MED-4912", pharmacy_id: 1, medicine_id: 1, patient_name: "Sarah Jenkins", patient_phone: "+1 (555) 019-2834", quantity: 1, status: "Active", time_ago: "12m ago" },
  { id: 2, code: "MED-8321", pharmacy_id: 1, medicine_id: 2, patient_name: "David Chen", patient_phone: "+1 (555) 234-8971", quantity: 1, status: "Active", time_ago: "35m ago" },
  { id: 3, code: "MED-2104", pharmacy_id: 4, medicine_id: 1, patient_name: "Maria Rossi", patient_phone: "+1 (555) 678-1122", quantity: 1, status: "Active", time_ago: "45m ago" }
];

// =====================================================================
// 2. STORAGE CONTROLLER
// =====================================================================

function getStoredData(key, fallback) {
  const item = localStorage.getItem(`medfind_${key}`);
  if (!item) {
    localStorage.setItem(`medfind_${key}`, JSON.stringify(fallback));
    return fallback;
  }
  try {
    return JSON.parse(item);
  } catch (e) {
    return fallback;
  }
}

function setStoredData(key, data) {
  localStorage.setItem(`medfind_${key}`, JSON.stringify(data));
}

let pharmacies = getStoredData("pharmacies", DEFAULT_PHARMACIES);
let medicines = getStoredData("medicines", DEFAULT_MEDICINES);
let stocks = getStoredData("stocks", DEFAULT_STOCKS);
let reservations = getStoredData("reservations", DEFAULT_RESERVATIONS);

// =====================================================================
// 3. CORE SEARCH & PRICE COMPARISON ENGINE
// =====================================================================

function executeSearch(query, locationFilter, sortBy) {
  const cleanQuery = (query || "").trim().toLowerCase();
  const cleanLoc = (locationFilter || "All").trim();

  // Find matching medicines
  const matchedMeds = medicines.filter(m => 
    !cleanQuery ||
    m.name.toLowerCase().includes(cleanQuery) || 
    m.generic_name.toLowerCase().includes(cleanQuery) ||
    m.category.toLowerCase().includes(cleanQuery)
  );

  const matchedMedIds = new Set(matchedMeds.map(m => m.id));

  // Find stock records matching medicines
  let results = [];
  stocks.forEach(stk => {
    if (matchedMedIds.has(stk.medicine_id)) {
      const pharm = pharmacies.find(p => p.id === stk.pharmacy_id);
      const med = medicines.find(m => m.id === stk.medicine_id);
      if (pharm && med) {
        // Location filter
        if (cleanLoc === "All" || pharm.city.toLowerCase() === cleanLoc.toLowerCase()) {
          results.push({
            pharmacy_id: pharm.id,
            pharmacy_name: pharm.name,
            pharmacy_address: pharm.address,
            pharmacy_city: pharm.city,
            pharmacy_phone: pharm.phone,
            opening_hours: pharm.opening_hours,
            is_open_247: pharm.is_open_247,
            distance_miles: pharm.distance_miles,
            medicine_id: med.id,
            medicine_name: med.name,
            generic_name: med.generic_name,
            category: med.category,
            dosage_form: med.dosage_form,
            prescription_required: med.prescription_required,
            stock_quantity: stk.stock_quantity,
            price: stk.price,
            updated_mins_ago: stk.updated_mins_ago || 5,
            stock_percent: Math.min(100, Math.round((stk.stock_quantity / 50) * 100))
          });
        }
      }
    }
  });

  // Calculate lowest price among items currently in stock
  const inStockPrices = results.filter(r => r.stock_quantity > 0).map(r => r.price);
  const minPrice = inStockPrices.length > 0 ? Math.min(...inStockPrices) : null;

  results.forEach(item => {
    item.is_best_price = (minPrice !== null && item.price === minPrice && item.stock_quantity > 0);
  });

  // Sorting
  if (sortBy === "price_asc") {
    results.sort((a, b) => (b.stock_quantity > 0) - (a.stock_quantity > 0) || a.price - b.price);
  } else if (sortBy === "price_desc") {
    results.sort((a, b) => (b.stock_quantity > 0) - (a.stock_quantity > 0) || b.price - a.price);
  } else if (sortBy === "stock_desc") {
    results.sort((a, b) => b.stock_quantity - a.stock_quantity);
  } else { // 'availability' (default)
    results.sort((a, b) => (b.stock_quantity > 0) - (a.stock_quantity > 0) || b.stock_quantity - a.stock_quantity || a.price - b.price);
  }

  return results;
}

// =====================================================================
// 4. CLIENT INITIALIZATION & DOM BINDINGS
// =====================================================================

document.addEventListener("DOMContentLoaded", () => {
  initSearchForm();
  initAutocomplete();
  initQuickFilters();
  initMapToggle();
  initReservationModal();
  initAdminConsole();

  // Run initial default search for Paracetamol to showcase rich UI immediately
  performSearchAndRender("Paracetamol 650mg", "All", "availability");
});

function initSearchForm() {
  const form = document.getElementById("search-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = document.getElementById("medicine-input").value;
      const loc = document.getElementById("location-select").value;
      const sort = document.getElementById("sort-select") ? document.getElementById("sort-select").value : "availability";
      performSearchAndRender(q, loc, sort);
    });
  }

  const sortSelect = document.getElementById("sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      const q = document.getElementById("medicine-input").value;
      const loc = document.getElementById("location-select").value;
      performSearchAndRender(q, loc, sortSelect.value);
    });
  }
}

function performSearchAndRender(query, location, sortBy) {
  const results = executeSearch(query, location, sortBy);
  renderResults(results, query, location);
}

function renderResults(results, query, location) {
  const resultsArea = document.getElementById("search-results-section");
  const countDisplay = document.getElementById("results-count-text");
  const queryDisplay = document.getElementById("results-query-highlight");
  const container = document.getElementById("results-cards-container");
  const unavailableBox = document.getElementById("unavailable-notice-box");
  const alternativesBox = document.getElementById("alternatives-box");

  if (!resultsArea || !container) return;

  resultsArea.style.display = "block";
  queryDisplay.textContent = `"${query || 'All Medicines'}"`;
  countDisplay.textContent = `Found ${results.length} pharmacy listing${results.length === 1 ? '' : 's'} • In-stock stores prioritized`;

  container.innerHTML = "";

  if (results.length === 0) {
    unavailableBox.style.display = "block";
    alternativesBox.style.display = "none";
    return;
  }

  unavailableBox.style.display = "none";

  // Build Results Cards
  results.forEach(item => {
    const isOutOfStock = item.stock_quantity === 0;
    const isLowStock = item.stock_quantity > 0 && item.stock_quantity <= 10;

    let stockBadgeHtml = "";
    if (isOutOfStock) {
      stockBadgeHtml = `<span class="badge badge-out-of-stock">❌ Out of Stock</span>`;
    } else if (isLowStock) {
      stockBadgeHtml = `<span class="badge badge-low-stock">⚠️ Low Stock (Only ${item.stock_quantity} left)</span>`;
    } else {
      stockBadgeHtml = `<span class="badge badge-in-stock"><span class="pulse-dot" style="width: 6px; height: 6px;"></span> In Stock</span>`;
    }

    const card = document.createElement("div");
    card.className = `pharmacy-card ${isOutOfStock ? 'out-of-stock-card' : ''}`;
    card.id = `card-pharm-${item.pharmacy_id}`;

    card.innerHTML = `
      ${item.is_best_price ? `
        <div class="card-best-price-ribbon">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
          Best Price
        </div>
      ` : ''}

      <!-- Col 1: Pharmacy Details -->
      <div class="col-pharmacy-info">
        <h3>
          <a href="#" class="pharmacy-name-link" onclick="openPharmacyModal(${item.pharmacy_id}); return false;">
            ${item.pharmacy_name}
          </a>
        </h3>

        <div class="pharmacy-location-line">
          <span class="badge badge-dist">📍 ${item.distance_miles} mi away</span>
          <span>${item.pharmacy_address} (${item.pharmacy_city})</span>
          ${item.is_open_247 ? `<span class="badge badge-in-stock" style="font-size: 0.7rem;">🕒 24/7 Open</span>` : `<span>• ${item.opening_hours}</span>`}
        </div>

        <div class="medicine-badge-group">
          <strong style="color: var(--text-primary);">${item.medicine_name}</strong>
          <span class="medicine-subtext">(${item.generic_name})</span>
          <span class="badge badge-demo">${item.dosage_form}</span>
          ${item.prescription_required ? `<span class="badge badge-rx">Rx Required</span>` : `<span class="badge badge-otc">OTC Available</span>`}
        </div>
      </div>

      <!-- Col 2: Live Stock & Meter -->
      <div class="col-stock-info">
        <div>${stockBadgeHtml}</div>

        <div class="stock-qty-display">
          ${item.stock_quantity > 0 ? `${item.stock_quantity} <span style="font-size: 0.88rem; font-weight: 500; color: var(--text-muted);">units available</span>` : `<span style="color: var(--danger); font-size: 1.1rem;">0 units</span>`}
        </div>

        <div class="stock-gauge-wrapper">
          <div class="stock-gauge-bar">
            <div class="stock-gauge-fill ${!isOutOfStock && !isLowStock ? 'gauge-green' : isLowStock ? 'gauge-amber' : 'gauge-red'}" style="width: ${item.stock_percent}%;"></div>
          </div>
        </div>

        <div class="stock-timestamp">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span>Updated ${item.updated_mins_ago}m ago • Verified</span>
        </div>
      </div>

      <!-- Col 3: Price -->
      <div class="col-price-info">
        <div class="price-main">$${item.price.toFixed(2)}</div>
        <div class="price-unit-label">Per pack / strip</div>
        ${item.is_best_price ? `<span class="badge badge-best-price" style="margin-top: 5px;">Lowest Price</span>` : ''}
      </div>

      <!-- Col 4: Action Buttons -->
      <div class="col-actions">
        ${item.stock_quantity > 0 ? `
          <button type="button" class="btn btn-reserve btn-sm" onclick="triggerHoldModal(${item.pharmacy_id}, ${item.medicine_id}, '${escapeQuotes(item.pharmacy_name)}', '${escapeQuotes(item.medicine_name)}', '$${item.price.toFixed(2)}')">
            ⏱️ Hold for 2h
          </button>
          <a href="tel:${item.pharmacy_phone}" class="btn btn-call-pharmacy btn-sm">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
            Call Store
          </a>
        ` : `
          <button class="btn btn-outline btn-sm" disabled style="opacity: 0.6; cursor: not-allowed;">
            Out of Stock
          </button>
        `}
        <button type="button" class="btn btn-outline btn-sm" onclick="openPharmacyModal(${item.pharmacy_id})">
          View Profile
        </button>
      </div>
    `;

    container.appendChild(card);
  });

  // Out-of-Stock suggestions check
  const hasInStock = results.some(r => r.stock_quantity > 0);
  if (!hasInStock) {
    showAlternativeStores(query);
  } else {
    alternativesBox.style.display = "none";
  }
}

function showAlternativeStores(query) {
  const box = document.getElementById("alternatives-box");
  const list = document.getElementById("alternatives-grid-container");
  if (!box || !list) return;

  // Search without location constraint
  const allResults = executeSearch(query, "All", "availability").filter(r => r.stock_quantity > 0);
  if (allResults.length === 0) {
    box.style.display = "none";
    return;
  }

  box.style.display = "block";
  list.innerHTML = "";

  allResults.slice(0, 4).forEach(alt => {
    const item = document.createElement("div");
    item.className = "alternative-card";
    item.innerHTML = `
      <div>
        <strong style="color: var(--text-primary); display: block;">${alt.pharmacy_name}</strong>
        <span class="text-muted" style="font-size: 0.8rem;">📍 ${alt.pharmacy_city} • ${alt.stock_quantity} in stock</span>
        <div style="font-weight: 750; color: var(--primary-color); font-size: 0.95rem; margin-top: 2px;">
          $${alt.price.toFixed(2)}
        </div>
      </div>
      <div>
        <a href="tel:${alt.pharmacy_phone}" class="btn btn-call-pharmacy btn-sm">Call Store</a>
      </div>
    `;
    list.appendChild(item);
  });
}

function escapeQuotes(str) {
  return (str || "").replace(/'/g, "\\'");
}

// =====================================================================
// 5. AUTOCOMPLETE, CHIPS & RX SCANNER
// =====================================================================

function initAutocomplete() {
  const input = document.getElementById("medicine-input");
  const box = document.getElementById("autocomplete-results");
  if (!input || !box) return;

  input.addEventListener("input", () => {
    const val = input.value.trim().toLowerCase();
    if (!val) {
      box.style.display = "none";
      return;
    }

    const matches = medicines.filter(m => 
      m.name.toLowerCase().includes(val) || 
      m.generic_name.toLowerCase().includes(val) || 
      m.category.toLowerCase().includes(val)
    ).slice(0, 7);

    if (matches.length === 0) {
      box.style.display = "none";
      return;
    }

    box.innerHTML = matches.map(m => `
      <div class="autocomplete-item" onclick="selectAutocomplete('${m.name}')">
        <div>
          <div class="autocomplete-name">${m.name}</div>
          <div class="autocomplete-meta">${m.generic_name} • ${m.category}</div>
        </div>
        <span class="badge badge-otc" style="font-size: 0.7rem;">Select</span>
      </div>
    `).join("");

    box.style.display = "block";
  });

  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !box.contains(e.target)) {
      box.style.display = "none";
    }
  });
}

function selectAutocomplete(name) {
  const input = document.getElementById("medicine-input");
  const box = document.getElementById("autocomplete-results");
  if (input) input.value = name;
  if (box) box.style.display = "none";
  performSearchAndRender(name, document.getElementById("location-select").value, "availability");
}

function initQuickFilters() {
  document.querySelectorAll(".quick-chip, .cat-pill").forEach(el => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const q = el.getAttribute("data-med") || el.getAttribute("data-query");
      if (q) {
        document.getElementById("medicine-input").value = q;
        performSearchAndRender(q, document.getElementById("location-select").value, "availability");
        document.getElementById("search-results-section").scrollIntoView({ behavior: "smooth" });
      }
    });
  });

  // Simulated Rx Scanner Dropzone
  const rxDropzone = document.getElementById("rx-scanner-dropzone");
  if (rxDropzone) {
    rxDropzone.addEventListener("click", () => {
      document.getElementById("medicine-input").value = "Amoxicillin 500mg";
      performSearchAndRender("Amoxicillin 500mg", "All", "availability");
      document.getElementById("search-results-section").scrollIntoView({ behavior: "smooth" });
    });
  }

  document.querySelectorAll(".demo-rx-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const q = btn.getAttribute("data-query");
      document.getElementById("medicine-input").value = q;
      performSearchAndRender(q, "All", "availability");
      document.getElementById("search-results-section").scrollIntoView({ behavior: "smooth" });
    });
  });
}

// =====================================================================
// 6. MAP PREVIEW TOGGLE & PIN HIGHLIGHT
// =====================================================================

function initMapToggle() {
  const btn = document.getElementById("toggle-map-btn");
  const box = document.getElementById("map-preview-box");
  if (!btn || !box) return;

  btn.addEventListener("click", () => {
    const isShowing = box.classList.toggle("active");
    btn.textContent = isShowing ? "✕ Hide Map View" : "🗺️ Toggle Pharmacy Map";
  });

  document.querySelectorAll(".map-pin").forEach(pin => {
    pin.addEventListener("click", () => {
      const pharmId = pin.getAttribute("data-pharm-id");
      const targetCard = document.getElementById(`card-pharm-${pharmId}`);
      if (targetCard) {
        targetCard.scrollIntoView({ behavior: "smooth", block: "center" });
        targetCard.style.borderColor = "var(--primary-color)";
        targetCard.style.boxShadow = "0 0 0 4px rgba(5, 150, 105, 0.25)";
        setTimeout(() => {
          targetCard.style.borderColor = "";
          targetCard.style.boxShadow = "";
        }, 1800);
      }
    });
  });
}

// =====================================================================
// 7. 2-HOUR HOLD RESERVATION MODAL
// =====================================================================

let activeHoldData = null;

function triggerHoldModal(pharmacyId, medicineId, pharmName, medName, price) {
  activeHoldData = { pharmacyId, medicineId, pharmName, medName, price };

  document.getElementById("modal-pharm-name").textContent = pharmName;
  document.getElementById("modal-med-name").textContent = medName;
  document.getElementById("modal-price").textContent = price;

  document.getElementById("modal-form-view").style.display = "block";
  document.getElementById("modal-success-view").style.display = "none";
  document.getElementById("reserveModal").classList.add("active");
}

function initReservationModal() {
  const modal = document.getElementById("reserveModal");
  const form = document.getElementById("reserveForm");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const patientName = document.getElementById("reserve-patient-name").value.trim() || "Alex Rivera";
      const patientPhone = document.getElementById("reserve-patient-phone").value.trim() || "+1 (555) 789-0123";

      const tokenCode = `MED-${Math.floor(1000 + Math.random() * 9000)}`;

      // Decrement stock in storage
      const stockRecord = stocks.find(s => s.pharmacy_id === activeHoldData.pharmacyId && s.medicine_id === activeHoldData.medicineId);
      if (stockRecord && stockRecord.stock_quantity > 0) {
        stockRecord.stock_quantity -= 1;
        setStoredData("stocks", stocks);
      }

      // Add to reservations in storage
      reservations.unshift({
        id: Date.now(),
        code: tokenCode,
        pharmacy_id: activeHoldData.pharmacyId,
        medicine_id: activeHoldData.medicineId,
        patient_name: patientName,
        patient_phone: patientPhone,
        quantity: 1,
        status: "Active",
        time_ago: "Just now"
      });
      setStoredData("reservations", reservations);

      // Display Token Code
      document.getElementById("modal-token-code").textContent = tokenCode;
      document.getElementById("modal-form-view").style.display = "none";
      document.getElementById("modal-success-view").style.display = "block";

      // Re-render search results live so new stock reflects immediately!
      const q = document.getElementById("medicine-input").value;
      const loc = document.getElementById("location-select").value;
      performSearchAndRender(q, loc, "availability");
      renderAdminDashboard();
    });
  }

  // Close buttons
  document.querySelectorAll("[data-modal-close]").forEach(btn => {
    btn.addEventListener("click", () => {
      modal.classList.remove("active");
      document.getElementById("editStockModal").classList.remove("active");
      document.getElementById("pharmacyModal").classList.remove("active");
      document.getElementById("adminModal").classList.remove("active");
    });
  });
}

// =====================================================================
// 8. CHEMIST ADMIN DASHBOARD CONTROLLER
// =====================================================================

let currentAdminPharmacyId = 1;

function initAdminConsole() {
  const pharmSelector = document.getElementById("admin-pharmacy-selector");
  if (pharmSelector) {
    pharmSelector.addEventListener("change", (e) => {
      currentAdminPharmacyId = parseInt(e.target.value, 10);
      renderAdminDashboard();
    });
  }
}

function openAdminDashboard() {
  renderAdminDashboard();
  document.getElementById("adminModal").classList.add("active");
}

function renderAdminDashboard() {
  const currentPharm = pharmacies.find(p => p.id === currentAdminPharmacyId);
  if (!currentPharm) return;

  document.getElementById("admin-pharm-title").textContent = currentPharm.name;
  document.getElementById("admin-pharm-city").textContent = `${currentPharm.city} Branch`;
  document.getElementById("admin-pharm-address").textContent = `${currentPharm.address} • ${currentPharm.phone} • ${currentPharm.opening_hours}`;

  // Get current pharmacy stock
  const pharmStocks = stocks.filter(s => s.pharmacy_id === currentAdminPharmacyId);
  const pharmReservations = reservations.filter(r => r.pharmacy_id === currentAdminPharmacyId);

  const totalMedicines = pharmStocks.length;
  const inStockCount = pharmStocks.filter(s => s.stock_quantity > 10).length;
  const lowStockCount = pharmStocks.filter(s => s.stock_quantity > 0 && s.stock_quantity <= 10).length;
  const outOfStockCount = pharmStocks.filter(s => s.stock_quantity === 0).length;

  document.getElementById("metric-total-meds").textContent = totalMedicines;
  document.getElementById("metric-in-stock").textContent = inStockCount;
  document.getElementById("metric-low-stock").textContent = lowStockCount;
  document.getElementById("metric-reservations").textContent = pharmReservations.length;

  // Render Reservations Stream
  const resContainer = document.getElementById("admin-reservations-stream");
  if (resContainer) {
    if (pharmReservations.length === 0) {
      resContainer.innerHTML = `<div class="text-muted text-xs p-2">No active customer pickup hold orders for this dispensary.</div>`;
    } else {
      resContainer.innerHTML = pharmReservations.slice(0, 10).map(r => {
        const med = medicines.find(m => m.id === r.medicine_id);
        return `
          <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] flex items-center justify-between">
            <div>
              <span class="badge badge-best-price">${r.code}</span>
              <strong class="ml-2">${med ? med.name : 'Prescription Medicine'}</strong>
              <span class="text-muted ml-1">(${r.quantity} pack)</span>
            </div>
            <div class="text-muted text-xs">👤 ${r.patient_name} • 📞 ${r.patient_phone}</div>
            <span class="badge badge-in-stock">${r.time_ago || 'Active'}</span>
          </div>
        `;
      }).join("");
    }
  }

  // Render Inventory Table
  const tbody = document.getElementById("admin-inventory-tbody");
  if (tbody) {
    tbody.innerHTML = pharmStocks.map(item => {
      const med = medicines.find(m => m.id === item.medicine_id);
      if (!med) return '';

      const isOutOfStock = item.stock_quantity === 0;
      const isLow = item.stock_quantity > 0 && item.stock_quantity <= 10;

      return `
        <tr style="${isOutOfStock ? 'background-color: #fff5f5;' : isLow ? 'background-color: #fffdf5;' : ''}">
          <td>
            <strong>${med.name}</strong>
            ${med.prescription_required ? `<span class="badge badge-rx">Rx</span>` : `<span class="badge badge-otc">OTC</span>`}
            <div class="text-muted" style="font-size: 0.78rem;">${med.dosage_form}</div>
          </td>
          <td class="text-muted">${med.generic_name}</td>
          <td>${med.category}</td>
          <td>
            ${!isOutOfStock && !isLow ? `<span class="badge badge-in-stock">In Stock</span>` : isLow ? `<span class="badge badge-low-stock">⚠️ Low Stock</span>` : `<span class="badge badge-out-of-stock">❌ Out of Stock</span>`}
          </td>
          <td>
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="font-size: 1.15rem; ${isOutOfStock ? 'color: var(--danger);' : isLow ? 'color: var(--warning-text);' : ''}">${item.stock_quantity}</strong>
              <span class="text-muted" style="font-size: 0.75rem;">units</span>
            </div>
            <div class="stock-gauge-bar" style="height: 5px; margin-top: 4px;">
              <div class="stock-gauge-fill ${!isOutOfStock && !isLow ? 'gauge-green' : isLow ? 'gauge-amber' : 'gauge-red'}" style="width: ${Math.min(100, item.stock_quantity * 2)}%;"></div>
            </div>
          </td>
          <td>
            <strong style="color: var(--primary-dark); font-size: 1.1rem;">$${item.price.toFixed(2)}</strong>
          </td>
          <td>
            <div style="display: flex; gap: 0.35rem;">
              <button class="quick-boost-btn" onclick="adjustStockDirect(${item.medicine_id}, 5)" title="Add 5 units immediately">+5</button>
              <button class="quick-boost-btn" onclick="adjustStockDirect(${item.medicine_id}, 10)" title="Add 10 units immediately">+10</button>
              <button class="quick-boost-btn" onclick="adjustStockDirect(${item.medicine_id}, -1)" title="Deduct 1 unit sold">-1</button>
            </div>
          </td>
          <td style="text-align: right;">
            <div style="display: flex; gap: 0.4rem; justify-content: flex-end;">
              <button class="btn btn-outline-primary btn-sm" onclick="openEditStockModal(${item.medicine_id}, '${escapeQuotes(med.name)}', ${item.stock_quantity}, ${item.price})">
                ✏️ Edit
              </button>
              <button class="btn btn-outline btn-sm" style="color: var(--danger);" onclick="deleteStockDirect(${item.medicine_id}, '${escapeQuotes(med.name)}')">
                🗑️
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join("");
  }
}

function adjustStockDirect(medicineId, delta) {
  const stockItem = stocks.find(s => s.pharmacy_id === currentAdminPharmacyId && s.medicine_id === medicineId);
  if (stockItem) {
    stockItem.stock_quantity = Math.max(0, stockItem.stock_quantity + delta);
    stockItem.updated_mins_ago = 1;
    setStoredData("stocks", stocks);

    // Refresh UI
    renderAdminDashboard();
    const q = document.getElementById("medicine-input").value;
    const loc = document.getElementById("location-select").value;
    performSearchAndRender(q, loc, "availability");
  }
}

function deleteStockDirect(medicineId, medName) {
  if (confirm(`Remove '${medName}' from this pharmacy's inventory?`)) {
    stocks = stocks.filter(s => !(s.pharmacy_id === currentAdminPharmacyId && s.medicine_id === medicineId));
    setStoredData("stocks", stocks);
    renderAdminDashboard();
    const q = document.getElementById("medicine-input").value;
    const loc = document.getElementById("location-select").value;
    performSearchAndRender(q, loc, "availability");
  }
}

let activeEditMedId = null;
function openEditStockModal(medicineId, medName, currentQty, currentPrice) {
  activeEditMedId = medicineId;
  document.getElementById("edit-med-name-title").textContent = medName;
  document.getElementById("edit-stock-qty-input").value = currentQty;
  document.getElementById("edit-stock-price-input").value = currentPrice.toFixed(2);
  document.getElementById("editStockModal").classList.add("active");
}

function saveStockEdit() {
  const newQty = parseInt(document.getElementById("edit-stock-qty-input").value, 10);
  const newPrice = parseFloat(document.getElementById("edit-stock-price-input").value);

  if (isNaN(newQty) || isNaN(newPrice) || newQty < 0 || newPrice < 0) {
    alert("Please enter valid numeric values.");
    return;
  }

  const stockItem = stocks.find(s => s.pharmacy_id === currentAdminPharmacyId && s.medicine_id === activeEditMedId);
  if (stockItem) {
    stockItem.stock_quantity = newQty;
    stockItem.price = newPrice;
    stockItem.updated_mins_ago = 1;
    setStoredData("stocks", stocks);

    document.getElementById("editStockModal").classList.remove("active");
    renderAdminDashboard();
    const q = document.getElementById("medicine-input").value;
    const loc = document.getElementById("location-select").value;
    performSearchAndRender(q, loc, "availability");
  }
}

// =====================================================================
// 9. PHARMACY PROFILE MODAL
// =====================================================================

function openPharmacyModal(pharmacyId) {
  const pharm = pharmacies.find(p => p.id === pharmacyId);
  if (!pharm) return;

  document.getElementById("modal-pharmacy-name").textContent = pharm.name;
  document.getElementById("modal-pharmacy-rating").textContent = `⭐ ${pharm.rating} Verified Retailer`;
  document.getElementById("modal-pharmacy-address").textContent = `📍 ${pharm.address}, ${pharm.city}`;
  document.getElementById("modal-pharmacy-hours").textContent = `🕒 ${pharm.opening_hours}`;
  document.getElementById("modal-pharmacy-call").href = `tel:${pharm.phone}`;
  document.getElementById("modal-pharmacy-call").textContent = `Call ${pharm.phone}`;

  // Get medicines in this pharmacy
  const pharmStocks = stocks.filter(s => s.pharmacy_id === pharmacyId);
  const listContainer = document.getElementById("modal-pharmacy-meds-list");

  listContainer.innerHTML = pharmStocks.map(stk => {
    const med = medicines.find(m => m.id === stk.medicine_id);
    if (!med) return '';
    const isOut = stk.stock_quantity === 0;
    const isLow = stk.stock_quantity > 0 && stk.stock_quantity <= 10;
    return `
      <div style="background: var(--surface-alt); padding: 0.85rem 1rem; border-radius: var(--radius-md); display: flex; justify-content: space-between; align-items: center; border: 1px solid var(--border-color);">
        <div>
          <strong>${med.name}</strong>
          <span class="text-muted" style="font-size: 0.8rem; display: block;">${med.generic_name} • ${med.dosage_form}</span>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 750; color: var(--primary-dark); font-size: 1.05rem;">$${stk.price.toFixed(2)}</div>
          <span class="badge ${!isOut && !isLow ? 'badge-in-stock' : isLow ? 'badge-low-stock' : 'badge-out-of-stock'}" style="font-size: 0.7rem;">
            ${!isOut ? `${stk.stock_quantity} in stock` : 'Out of Stock'}
          </span>
        </div>
      </div>
    `;
  }).join("");

  document.getElementById("pharmacyModal").classList.add("active");
}

