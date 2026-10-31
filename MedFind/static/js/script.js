/**
 * script.js - Interactive Client-Side Logic for MEDFIND
 * Handles live medicine autocomplete, modals, quick-fill accounts,
 * map visualization toggle, 2-hour pickup reservations, and Rx scanner demo.
 */

document.addEventListener("DOMContentLoaded", () => {
  initAutocomplete();
  initModals();
  initDemoCredentials();
  initSortAutoSubmit();
  initQuickChips();
  initMapToggle();
  initReservationModal();
  initRxScannerDemo();
});

/* ===================================================================
   1. INNOVATIVE FEATURE: SMART MEDICINE AUTOCOMPLETE
   =================================================================== */
function initAutocomplete() {
  const searchInput = document.querySelector("#medicine-input");
  const autocompleteBox = document.querySelector("#autocomplete-results");

  if (!searchInput || !autocompleteBox) return;

  let debounceTimer;

  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (query.length < 1) {
      autocompleteBox.style.display = "none";
      autocompleteBox.innerHTML = "";
      return;
    }

    debounceTimer = setTimeout(() => {
      fetch(`/api/autocomplete?q=${encodeURIComponent(query)}`)
        .then((res) => res.json())
        .then((items) => {
          if (!items || items.length === 0) {
            autocompleteBox.style.display = "none";
            return;
          }

          autocompleteBox.innerHTML = items
            .map(
              (item) => `
              <div class="autocomplete-item" data-name="${item.name}">
                <div>
                  <div class="autocomplete-name">${item.name}</div>
                  <div class="autocomplete-meta">${item.generic_name} • ${item.category}</div>
                </div>
                <span class="badge badge-otc" style="font-size: 0.7rem;">Select</span>
              </div>
            `
            )
            .join("");

          autocompleteBox.style.display = "block";

          autocompleteBox.querySelectorAll(".autocomplete-item").forEach((el) => {
            el.addEventListener("click", () => {
              searchInput.value = el.getAttribute("data-name");
              autocompleteBox.style.display = "none";
              const form = searchInput.closest("form");
              if (form) form.submit();
            });
          });
        })
        .catch((err) => {
          console.error("Autocomplete fetch error:", err);
        });
    }, 200);
  });

  document.addEventListener("click", (e) => {
    if (!searchInput.contains(e.target) && !autocompleteBox.contains(e.target)) {
      autocompleteBox.style.display = "none";
    }
  });
}

/* ===================================================================
   2. HOMEPAGE QUICK MEDICINE CHIPS
   =================================================================== */
function initQuickChips() {
  const chips = document.querySelectorAll(".quick-chip");
  const searchInput = document.querySelector("#medicine-input");
  const form = document.querySelector(".search-form");

  chips.forEach((chip) => {
    chip.addEventListener("click", (e) => {
      e.preventDefault();
      const medName = chip.getAttribute("data-med");
      if (searchInput && medName) {
        searchInput.value = medName;
        if (form) form.submit();
      }
    });
  });
}

/* ===================================================================
   3. SORT DROPDOWN AUTO-SUBMIT
   =================================================================== */
function initSortAutoSubmit() {
  const sortSelect = document.querySelector("#sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", () => {
      const form = sortSelect.closest("form");
      if (form) form.submit();
    });
  }
}

/* ===================================================================
   4. MODAL CONTROLS (GENERIC & EDIT STOCK)
   =================================================================== */
function initModals() {
  const openButtons = document.querySelectorAll("[data-modal-target]");
  const closeButtons = document.querySelectorAll(".modal-close-btn, [data-modal-close]");

  openButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-modal-target");
      const targetModal = document.querySelector(targetId);
      if (targetModal) {
        targetModal.classList.add("active");
      }
    });
  });

  closeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const activeModal = btn.closest(".modal-overlay");
      if (activeModal) {
        activeModal.classList.remove("active");
      }
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("active");
      }
    });
  });

  // Admin Stock Edit Trigger
  const editButtons = document.querySelectorAll(".btn-edit-stock");
  const editModal = document.querySelector("#editStockModal");

  if (editModal && editButtons.length > 0) {
    const medIdInput = editModal.querySelector("#edit-med-id");
    const medNameDisplay = editModal.querySelector("#edit-med-name");
    const qtyInput = editModal.querySelector("#edit-quantity");
    const priceInput = editModal.querySelector("#edit-price");

    editButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const medId = btn.getAttribute("data-med-id");
        const medName = btn.getAttribute("data-med-name");
        const qty = btn.getAttribute("data-qty");
        const price = btn.getAttribute("data-price");

        if (medIdInput) medIdInput.value = medId;
        if (medNameDisplay) medNameDisplay.textContent = medName;
        if (qtyInput) qtyInput.value = qty;
        if (priceInput) priceInput.value = price;

        editModal.classList.add("active");
      });
    });
  }
}

/* ===================================================================
   5. QUICK-FILL DEMO CREDENTIALS
   =================================================================== */
function initDemoCredentials() {
  const demoChips = document.querySelectorAll(".demo-account-chip");
  const usernameInput = document.querySelector("#admin-username");
  const passwordInput = document.querySelector("#admin-password");

  demoChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const user = chip.getAttribute("data-username");
      const pass = chip.getAttribute("data-password");

      if (usernameInput && user) usernameInput.value = user;
      if (passwordInput && pass) passwordInput.value = pass;
    });
  });
}

/* ===================================================================
   6. INTERACTIVE MAP PREVIEW TOGGLE
   =================================================================== */
function initMapToggle() {
  const mapBtn = document.querySelector("#toggle-map-btn");
  const mapBox = document.querySelector("#map-preview-box");

  if (!mapBtn || !mapBox) return;

  mapBtn.addEventListener("click", () => {
    const isShowing = mapBox.classList.toggle("active");
    mapBtn.textContent = isShowing ? "✕ Hide Map View" : "🗺️ Toggle Pharmacy Map";
  });

  // Map pin clicking scrolls to matching pharmacy card
  document.querySelectorAll(".map-pin").forEach((pin, index) => {
    pin.addEventListener("click", () => {
      const cards = document.querySelectorAll(".pharmacy-card");
      if (cards[index]) {
        cards[index].scrollIntoView({ behavior: "smooth", block: "center" });
        cards[index].style.borderColor = "var(--primary-color)";
        cards[index].style.boxShadow = "0 0 0 4px rgba(5, 150, 105, 0.2)";
        setTimeout(() => {
          cards[index].style.borderColor = "";
          cards[index].style.boxShadow = "";
        }, 1800);
      }
    });
  });
}

/* ===================================================================
   7. 2-HOUR PICKUP HOLD RESERVATION (INNOVATIVE FEATURE)
   =================================================================== */
function initReservationModal() {
  const reserveButtons = document.querySelectorAll(".btn-open-reserve");
  const modal = document.querySelector("#reserveModal");
  if (!modal || reserveButtons.length === 0) return;

  const pharmIdInput = modal.querySelector("#reserve-pharmacy-id");
  const medIdInput = modal.querySelector("#reserve-medicine-id");
  const medTitle = modal.querySelector("#reserve-med-title");
  const pharmTitle = modal.querySelector("#reserve-pharm-title");
  const priceTitle = modal.querySelector("#reserve-price-title");
  const form = modal.querySelector("#reserveForm");
  const confirmationBox = modal.querySelector("#reserve-confirmation-box");
  const tokenDisplay = modal.querySelector("#token-display");
  const submitBtn = modal.querySelector("#btn-submit-reserve");

  reserveButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      pharmIdInput.value = btn.getAttribute("data-pharmacy-id");
      medIdInput.value = btn.getAttribute("data-medicine-id");
      medTitle.textContent = btn.getAttribute("data-medicine-name");
      pharmTitle.textContent = btn.getAttribute("data-pharmacy-name");
      priceTitle.textContent = btn.getAttribute("data-price");

      // Reset form states
      form.reset();
      confirmationBox.style.display = "none";
      submitBtn.style.display = "inline-flex";
      submitBtn.disabled = false;
      modal.classList.add("active");
    });
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = "Reserving...";

    const formData = new FormData(form);

    fetch("/api/reserve", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          tokenDisplay.textContent = data.code;
          confirmationBox.style.display = "block";
          submitBtn.style.display = "none";
        } else {
          alert(data.error || "Unable to reserve medicine. Please try again.");
          submitBtn.disabled = false;
          submitBtn.textContent = "Confirm 2-Hour Reservation";
        }
      })
      .catch((err) => {
        console.error("Reservation error:", err);
        alert("Network error processing reservation.");
        submitBtn.disabled = false;
        submitBtn.textContent = "Confirm 2-Hour Reservation";
      });
  });
}

/* ===================================================================
   8. SIMULATED RX SCANNER DEMO
   =================================================================== */
function initRxScannerDemo() {
  const dropzone = document.querySelector("#rx-scanner-dropzone");
  const rxButtons = document.querySelectorAll(".demo-rx-btn");

  if (!dropzone) return;

  rxButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const query = btn.getAttribute("data-query");
      btn.textContent = "🔍 Parsing prescription...";
      setTimeout(() => {
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
      }, 600);
    });
  });

  dropzone.addEventListener("click", () => {
    // Pick first demo query
    const sample = rxButtons[0];
    if (sample) sample.click();
  });
}

/* ===================================================================
   9. DELETE CONFIRMATION HELPER
   =================================================================== */
function confirmDelete(medicineName) {
  return confirm(
    `Are you sure you want to remove '${medicineName}' from your pharmacy inventory? This action is immediate.`
  );
}
