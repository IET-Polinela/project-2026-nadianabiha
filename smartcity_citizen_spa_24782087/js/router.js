// ============================================================
// router.js - Modul Hash-Based Routing
// Mengatur perpindahan halaman secara instan tanpa reload
// ============================================================

/**
 * Objek routes berisi mapping antara hash URL dengan konten HTML.
 * Setiap key adalah hash (tanpa #), value adalah HTML string.
 */
const routes = {
    'login': `
        <div>
            <div class="row justify-content-center mt-5">
                <div class="col-md-4 card shadow-sm border-0 p-4">
                    <h4 class="text-center fw-bold mb-4">Login Warga</h4>
                    <form id="loginForm">
                        <input type="text" id="loginUsername" class="form-control mb-3" placeholder="Username" required>
                        <input type="password" id="loginPassword" class="form-control mb-3" placeholder="Password" required>
                        <button type="submit" class="btn btn-primary w-100 fw-bold">Masuk</button>
                    </form>
                </div>
            </div>
        </div>
    `,
    'dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card dashboard-card p-3 shadow-sm sticky-top">
                    <button class="btn btn-primary btn-lg w-100 fw-bold mb-4" onclick="new bootstrap.Modal(document.getElementById('reportModal')).show()">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    <h6 class="fw-bold mb-3"><i class="bi bi-bar-chart-fill text-primary me-2"></i>Rekap Status</h6>
                    <ul class="list-group list-group-flush small">
                        <li class="list-group-item d-flex justify-content-between align-items-center px-0">
                            Draft <span class="badge bg-secondary rounded-pill px-3" id="countDraft">0</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center px-0">
                            Diproses <span class="badge bg-warning rounded-pill px-3" id="countDiproses">0</span>
                        </li>
                        <li class="list-group-item d-flex justify-content-between align-items-center px-0">
                            Selesai <span class="badge bg-success rounded-pill px-3" id="countSelesai">0</span>
                        </li>
                    </ul>
                </div>
            </aside>
            <section class="col-12 col-lg-8">
                <div class="card dashboard-card border-0 shadow-sm p-3">
                    <ul class="nav nav-pills mb-3" id="dashboardTabs">
                        <li class="nav-item">
                            <a class="nav-link active" href="#" id="tabMyReports"
                               onclick="switchTab('my_reports'); return false;">
                               <i class="bi bi-journal-text me-1"></i>Laporan Saya
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" id="tabFeed"
                               onclick="switchTab('feed'); return false;">
                               <i class="bi bi-globe me-1"></i>Feed Kota
                            </a>
                        </li>
                    </ul>
                    <div id="reportContainer">
                        <div class="text-center py-5 text-muted">
                            <div class="spinner-border" role="status"></div>
                            <p class="mt-2">Memuat data...</p>
                        </div>
                    </div>
                    <div id="paginationContainer" class="mt-3"></div>
                </div>
            </section>
            <aside class="col-12 col-lg-1 d-none d-xl-block"></aside>
        </div>
    `,
};

/**
 * Fungsi untuk berpindah tab (Laporan Saya / Feed Kota)
 */
function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;

    // Update UI tab active state
    document.getElementById('tabMyReports').classList.toggle('active', tab === 'my_reports');
    document.getElementById('tabFeed').classList.toggle('active', tab === 'feed');

    // Muat data sesuai tab
    loadDashboardData(tab, 1);
}

/**
 * Fungsi utama untuk menangani perubahan rute (hash).
 * Membaca hash dari URL, menampilkan konten yang sesuai,
 * dan menjalankan setup form jika halaman login.
 */
function handleRouting() {
    const hash = window.location.hash || '#login'; // Default ke login
    const page = hash.replace('#', '');

    // Ambil HTML dari objek routes, default ke halaman login
    const html = routes[page] || routes['login'];

    // Masukkan HTML ke dalam elemen app-content
    document.getElementById('app-content').innerHTML = html;

    // Jika halaman login, jalankan setupLoginForm dari auth.js
    if (page === 'login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }

    // Jika halaman dashboard, muat data laporan dari API
    if (page === 'dashboard' && typeof loadDashboardData === 'function') {
        loadDashboardData('my_reports', 1);
        loadSummaryStats();
    }
}

// Event listener untuk mendeteksi perubahan hash (navigasi)
window.addEventListener('hashchange', handleRouting);

// Event listener untuk menjalankan routing saat halaman pertama kali dimuat
window.addEventListener('DOMContentLoaded', handleRouting);
