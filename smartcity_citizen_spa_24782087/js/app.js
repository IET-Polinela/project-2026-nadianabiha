// ============================================================
// app.js - Modul Utama Aplikasi
// Entry point untuk inisialisasi aplikasi SPA
// ============================================================

// Variable global untuk tracking halaman dan tab aktif
let currentTab = 'my_reports';
let currentPage = 1;
let allReports = [];
let totalCount = 0;
let totalPages = 0;

/**
 * Fungsi utama untuk menarik data laporan dari API.
 * Memanggil endpoint /api/report/ dengan parameter tab dan page.
 */
async function loadDashboardData(tab = currentTab, page = currentPage) {
    currentTab = tab;
    currentPage = page;

    try {
        // Menembak API Backend dengan parameter tab dan page
        const response = await requestAPI(`/api/report/?tab=${tab}&page=${page}`);

        if (response.status === 200) {
            const data = await response.json();
            console.log('Data laporan berhasil dimuat:', data);

            // Ekstraksi Data Paginasi
            allReports = Array.isArray(data.results) ? data.results : [];
            totalCount = Number.isFinite(data.count) ? data.count : 0;
            totalPages = Math.ceil(totalCount / 10);

            // Render cards ke container
            const container = document.getElementById('reportContainer');
            if (container) {
                renderList(allReports, container);
            }

            // Render pagination
            const paginationContainer = document.getElementById('paginationContainer');
            if (paginationContainer) {
                renderPagination(totalCount, page, paginationContainer);
            }

            // Update summary setiap kali data dashboard dimuat ulang
            loadSummaryStats();
        } else {
            console.error('Gagal memuat data, status:', response.status);
            const listContainer = document.getElementById('reportContainer');
            if (listContainer) {
                listContainer.innerHTML = `
                    <div class="card border-0 p-5 shadow-sm text-center text-muted">
                        <h5 class="mb-2">Gagal memuat data laporan.</h5>
                        <p class="small">Silakan coba lagi nanti.</p>
                    </div>`;
            }
            const paginationContainer = document.getElementById('paginationContainer');
            if (paginationContainer) paginationContainer.innerHTML = '';
        }
    } catch (error) {
        console.error('Error saat memuat data:', error);
        const listContainer = document.getElementById('reportContainer');
        if (listContainer) {
            listContainer.innerHTML = `
                <div class="card border-0 p-5 shadow-sm text-center text-muted">
                    <h5 class="mb-2">Gagal memuat data laporan.</h5>
                    <p class="small">Periksa koneksi jaringan atau autentikasi Anda.</p>
                </div>`;
        }
        const paginationContainer = document.getElementById('paginationContainer');
        if (paginationContainer) paginationContainer.innerHTML = '';
    }
}

/**
 * Render daftar kartu laporan ke container.
 */
function renderList(reports, container) {
    if (!reports || reports.length === 0) {
        container.innerHTML = `
            <div class="card border-0 p-5 shadow-sm text-center text-muted">
                <i class="bi bi-inbox fs-1"></i>
                <h5 class="mt-3">Belum ada laporan</h5>
                <p class="small">Data kosong untuk tab ini.</p>
            </div>`;
        return;
    }

    // Mapping status ke persentase Progress Bar
    const statusProgress = {
        'DRAFT': 0,
        'REPORTED': 25,
        'VERIFIED': 50,
        'IN_PROGRESS': 75,
        'RESOLVED': 100,
    };

    // Mapping status ke warna badge
    const statusBadge = {
        'DRAFT': 'secondary',
        'REPORTED': 'info',
        'VERIFIED': 'primary',
        'IN_PROGRESS': 'warning',
        'RESOLVED': 'success',
    };

    const statusProgressClass = {
        'DRAFT': 'progress-bar-draft',
        'REPORTED': 'progress-bar-reported',
        'VERIFIED': 'progress-bar-verified',
        'IN_PROGRESS': 'progress-bar-in-progress',
        'RESOLVED': 'progress-bar-resolved',
    };

    let html = '<div class="row row-cols-1 row-cols-xl-2 g-4">';
    reports.forEach(report => {
        const progress = statusProgress[report.status] || 0;
        const badge = statusBadge[report.status] || 'secondary';
        const progressClass = statusProgressClass[report.status] || '';
        const updatedAt = new Date(report.updated_at).toLocaleString('id-ID');

        let editButton = '';
        if (report.is_owner && report.status === 'DRAFT') {
            editButton = `
                <button class="btn btn-sm btn-outline-warning btn-draft-edit mt-3" onclick="editDraft(${report.id})">
                    <i class="bi bi-pencil-square me-1"></i>
                    Edit Draft
                </button>`;
        }

        html += `
            <div class="col">
                <div class="card card-report h-100 border-0 shadow-sm ${report.status === 'DRAFT' ? 'draft-card bg-white' : 'bg-white'}">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <h6 class="card-title fw-bold mb-1">${report.title}</h6>
                                <div class="text-muted small report-meta">
                                    <span><i class="bi bi-person me-1"></i>${report.reporter}</span>
                                    <span><i class="bi bi-geo-alt me-1"></i>${report.location}</span>
                                    <span><i class="bi bi-tag me-1"></i>${report.category}</span>
                                </div>
                            </div>
                            <span class="badge bg-${badge} status-badge text-uppercase">${report.status}</span>
                        </div>
                        <p class="card-text small text-muted mb-4">${report.description || ''}</p>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between align-items-center mb-2 progress-label">
                                <span>Progress</span>
                                <span>${progress}%</span>
                            </div>
                            <div class="progress custom-progress">
                                <div class="custom-progress-bar ${progressClass}" role="progressbar"
                                     style="width: ${progress}%" aria-valuenow="${progress}"
                                     aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">Diperbarui: ${updatedAt}</small>
                            ${editButton}
                        </div>
                    </div>
                </div>
            </div>`;
    });
    html += '</div>';

    container.innerHTML = html;
}

/**
 * Render tombol pagination berdasarkan total data.
 */
function renderPagination(totalCount, activePage, container) {
    const totalPages = Math.ceil(totalCount / 10);
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }

    const maxButtons = 5;
    let startPage = Math.max(activePage - Math.floor(maxButtons / 2), 1);
    let endPage = startPage + maxButtons - 1;

    if (endPage > totalPages) {
        endPage = totalPages;
        startPage = Math.max(totalPages - maxButtons + 1, 1);
    }

    let html = '<nav><ul class="pagination pagination-sm justify-content-center">';

    if (activePage > 1) {
        html += `
            <li class="page-item">
                <a class="page-link" href="#" data-page="1" aria-label="First">&laquo;</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="#" data-page="${activePage - 1}" aria-label="Previous">&lsaquo;</a>
            </li>`;
    }

    for (let page = startPage; page <= endPage; page++) {
        html += `
            <li class="page-item ${page === activePage ? 'active' : ''}">
                <a class="page-link" href="#" data-page="${page}">${page}</a>
            </li>`;
    }

    if (activePage < totalPages) {
        html += `
            <li class="page-item">
                <a class="page-link" href="#" data-page="${activePage + 1}" aria-label="Next">&rsaquo;</a>
            </li>
            <li class="page-item">
                <a class="page-link" href="#" data-page="${totalPages}" aria-label="Last">&raquo;</a>
            </li>`;
    }

    html += '</ul></nav>';
    container.innerHTML = html;

    container.querySelectorAll('a.page-link').forEach(link => {
        const targetPage = Number(link.dataset.page);
        if (!Number.isNaN(targetPage)) {
            link.addEventListener('click', event => {
                event.preventDefault();
                loadDashboardData(currentTab, targetPage);
            });
        }
    });
}

/**
 * Kalkulasi Rekap Status di Sidebar.
 * Bypass pagination dengan page_size besar untuk menghitung total per status.
 */
async function loadSummaryStats() {
    try {
        const response = await requestAPI('/api/report/?tab=my_reports&page_size=1000');
        if (response.status === 200) {
            const data = await response.json();
            const reports = data.results;

            // Hitung total per status menggunakan .filter().length
            const countDraft = reports.filter(r => r.status === 'DRAFT').length;
            const countDiproses = reports.filter(r =>
                ['REPORTED', 'VERIFIED', 'IN_PROGRESS'].includes(r.status)
            ).length;
            const countSelesai = reports.filter(r => r.status === 'RESOLVED').length;

            // Update elemen sidebar
            const elDraft = document.getElementById('countDraft');
            const elDiproses = document.getElementById('countDiproses');
            const elSelesai = document.getElementById('countSelesai');

            if (elDraft) elDraft.textContent = countDraft;
            if (elDiproses) elDiproses.textContent = countDiproses;
            if (elSelesai) elSelesai.textContent = countSelesai;
        }
    } catch (error) {
        console.error('Error saat memuat summary stats:', error);
    }
}

// Global state untuk tracking ID report yang sedang diedit
let editingReportId = null;

/**
 * Fungsi untuk mengambil data draft lama dan memunculkannya di form modal
 */
async function editDraft(id) {
    try {
        const response = await requestAPI(`/api/report/${id}/`);
        if (response.status === 200) {
            const report = await response.json();

            // Isi form dengan data lama
            document.getElementById('inputTitle').value = report.title;
            document.getElementById('inputCategory').value = report.category;
            document.getElementById('inputLocation').value = report.location;
            document.getElementById('inputDescription').value = report.description;

            // Set global ID
            editingReportId = id;

            // Ubah judul modal
            const modalLabel = document.getElementById('reportModalLabel');
            if (modalLabel) modalLabel.innerHTML = '<i class="bi bi-pencil-square me-2"></i>Edit Draft Laporan';

            // Tampilkan modal
            showReportModal();
        }
    } catch (error) {
        console.error('Error saat mengambil detail report:', error);
    }
}

/**
 * Setup event listener untuk form laporan saat aplikasi dimuat
 */
function setupReportForm() {
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    const submitHandler = async (status) => {
        const title = document.getElementById('inputTitle').value;
        const category = document.getElementById('inputCategory').value;
        const location = document.getElementById('inputLocation').value;
        const description = document.getElementById('inputDescription').value;

        if (!title || !category || !location || !description) {
            alert('Semua field harus diisi!');
            return;
        }

        const payload = {
            title, category, location, description, status
        };

        try {
            let response;
            if (editingReportId === null) {
                // POST: Buat laporan baru
                response = await requestAPI('/api/report/', 'POST', payload);
            } else {
                // PUT: Update laporan lama
                response = await requestAPI(`/api/report/${editingReportId}/`, 'PUT', payload);
            }

            if (response.status === 201 || response.status === 200) {
                alert(status === 'DRAFT' ? 'Draft berhasil disimpan!' : 'Laporan berhasil diajukan!');

                // Tutup modal
                hideReportModal();

                // Reset form dan ID
                document.getElementById('reportForm').reset();
                editingReportId = null;

                // Kembalikan judul modal ke default
                const modalLabel = document.getElementById('reportModalLabel');
                if (modalLabel) modalLabel.innerHTML = '<i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru';

                // Refresh data dashboard tanpa reload halaman
                loadDashboardData('my_reports', 1);
                loadSummaryStats();
            } else {
                const err = await response.json();
                alert('Gagal menyimpan laporan. Periksa inputan.');
                console.error(err);
            }
        } catch (error) {
            console.error('Error submit form:', error);
            alert('Terjadi kesalahan jaringan.');
        }
    };

    if (btnDraft) {
        btnDraft.addEventListener('click', () => submitHandler('DRAFT'));
    }
    if (btnSubmit) {
        btnSubmit.addEventListener('click', () => submitHandler('REPORTED'));
    }

    // Event listener untuk reset state saat modal ditutup
    const modalElement = document.getElementById('reportModal');
    if (modalElement) {
        modalElement.addEventListener('hidden.bs.modal', () => {
            document.getElementById('reportForm').reset();
            editingReportId = null;
            const modalLabel = document.getElementById('reportModalLabel');
            if (modalLabel) modalLabel.innerHTML = '<i class="bi bi-pencil-square me-2"></i>Buat Laporan Baru';
        });
    }
}

function showReportModal() {
    const modalElement = document.getElementById('reportModal');
    if (!modalElement) return;

    if (window.bootstrap && bootstrap.Modal) {
        bootstrap.Modal.getOrCreateInstance(modalElement).show();
        return;
    }

    modalElement.classList.add('show');
    modalElement.removeAttribute('aria-hidden');
    modalElement.setAttribute('aria-modal', 'true');
    modalElement.style.display = 'block';
}

function hideReportModal() {
    const modalElement = document.getElementById('reportModal');
    if (!modalElement) return;

    if (window.bootstrap && bootstrap.Modal) {
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (modalInstance) {
            modalInstance.hide();
            return;
        }
    }

    modalElement.classList.remove('show');
    modalElement.setAttribute('aria-hidden', 'true');
    modalElement.removeAttribute('aria-modal');
    modalElement.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('Smart City Portal - Citizen SPA berhasil dimuat.');
    console.log('NPM: 24782087');
    setupReportForm();
});
