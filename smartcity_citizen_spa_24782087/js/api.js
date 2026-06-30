// ============================================================
// api.js - Modul Komunikasi API
// Berisi fungsi helper untuk berkomunikasi dengan Backend Django
// ============================================================

const API_BASE_URL = 'http://103.151.63.88:8005'; // Base URL backend Django (Server Public IP)

/**
 * Fungsi utama untuk melakukan request ke API Backend.
 * Secara otomatis menyisipkan JWT Access Token dari localStorage
 * ke header Authorization untuk setiap request.
 *
 * @param {string} endpoint - Path endpoint API (contoh: '/api/token/')
 * @param {string} method - Metode HTTP (GET, POST, PUT, DELETE)
 * @param {object|null} bodyData - Data yang akan dikirim sebagai body (untuk POST/PUT)
 * @returns {Promise<Response>} - Promise yang berisi response dari server
 */
async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const url = `${API_BASE_URL}${endpoint}`;

    // Siapkan headers default
    const headers = {
        'Content-Type': 'application/json',
    };

    // Ambil access_token dari localStorage dan sisipkan ke header Authorization
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // Siapkan opsi fetch
    const options = {
        method: method,
        headers: headers,
    };

    // Tambahkan body jika ada data yang dikirim (POST/PUT)
    if (bodyData) {
        options.body = JSON.stringify(bodyData);
    }

    // Lakukan fetch request
    const response = await fetch(url, options);
    if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        alert('Sesi Anda telah habis atau Anda belum login.');
        window.location.hash = '#login';
    }
    return response;
}
