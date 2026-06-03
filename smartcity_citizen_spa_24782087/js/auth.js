// ============================================================
// auth.js - Modul Autentikasi
// Menangani proses Login dan pengelolaan JWT Token
// ============================================================

/**
 * Fungsi untuk menyiapkan event handler pada form login.
 * Menangkap event submit, mengirim kredensial ke backend,
 * dan menyimpan JWT token ke localStorage.
 */
function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            // preventDefault() WAJIB digunakan agar halaman tidak reload
            // yang akan membocorkan password ke URL
            event.preventDefault();

            // Ambil nilai username dan password dari form
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            try {
                // Kirim payload username dan password ke endpoint /api/token/
                // menggunakan fungsi requestAPI dari api.js
                const response = await requestAPI('/api/token/', 'POST', {
                    username: username,
                    password: password,
                });

                // Jika respons berstatus 200 (OK)
                if (response.status === 200) {
                    const data = await response.json();

                    // Simpan access dan refresh token ke dalam localStorage
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);

                    // Berikan alert sukses
                    alert('Login berhasil! Selamat datang.');

                    // Ubah rute ke halaman dashboard
                    window.location.hash = '#dashboard';
                } else {
                    // Jika login gagal
                    const errorData = await response.json();
                    alert('Login gagal! Username atau password salah.');
                    console.error('Login Error:', errorData);
                }
            } catch (error) {
                // Tangani error jaringan
                alert('Terjadi kesalahan jaringan. Pastikan backend server berjalan.');
                console.error('Network Error:', error);
            }
        });
    }
}
