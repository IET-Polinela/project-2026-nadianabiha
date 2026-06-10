# Deployment Checklist - Tahap 2 Backend

## 1. Pre-Flight Check (Server Infrastructure)

Pada tahap ini, tugas utama adalah melakukan inspeksi server melalui SSH. Repository ini tidak menyimpan konfigurasi Nginx atau unit service systemd karena biasanya disediakan oleh administrator server.

Server yang digunakan:
- Server 6: `103.151.63.88`
- Login SSH: `mhsXX` / `mhsXX`

Database server:
- DB name: `db_mhsXX`
- DB user: `user_mhsXX`
- DB password: `mhsXX`

> Catatan: ganti `XX` dengan nomor mahasiswa kamu. Contoh jika kamu mhs05, gunakan:
> - SSH: `mhs05` / `mhs05`
> - DB name: `db_mhs05`
> - DB user: `user_mhs05`
> - DB password: `mhs05`

### Hal yang harus diperiksa di server

- Pastikan folder proyek berada di:
  - `/home/<username>/server_smartcity`
  - Atau jalur yang sama persis dengan struktur yang sudah kamu siapkan.

- Periksa konfigurasi Nginx di file sites-available:
  ```bash
  cat /etc/nginx/sites-available/mhsXX
  ```
  Pastikan terdapat baris:
  - `listen 8014;` atau port publik lain yang diberikan
  - `proxy_pass http://127.0.0.1:9014;` atau internal port Gunicorn yang sesuai

- Periksa service Gunicorn:
  ```bash
  cat /etc/systemd/system/gunicorn-mhsXX.service
  ```
  Pastikan:
  - `WorkingDirectory=/home/<username>/server_smartcity`
  - `ExecStart=` mengarah ke `gunicorn` dan module `smartcity_app.wsgi:application`
  - `User=` menjalankan service dengan akun mahasiswa yang benar

## 2. Verifikasi Struktur Lokal

Repository saat ini sudah disesuaikan dengan persyaratan laboratorium:

- `server_smartcity/` adalah root proyek Django
- `server_smartcity/smartcity_app/` adalah module konfigurasi Django
- `server_smartcity/manage.py` menggunakan `smartcity_app.settings`
- `server_smartcity/smartcity_app/settings.py` telah dikonfigurasi untuk:
  - `ALLOWED_HOSTS = ['*']`
  - `CORS_ALLOW_ALL_ORIGINS = True`
  - `STATIC_ROOT = BASE_DIR / 'staticfiles'`

## 2. Persiapan Repository dan Working Directory

a. Pada server `/home/mhsXX`, clone repository GitHub proyek ke dalam folder `project_app`.

Contoh:

```bash
ssh mhsXX@103.151.63.88
cd /home/mhsXX
git clone https://github.com/IET-Polinela/project-2026-nadianabiha.git project_app
```

b. Masuk ke folder project_app dan pastikan struktur folder berisi `server_smartcity` seperti yang digunakan oleh file service Gunicorn.

```bash
cd /home/mhsXX/project_app
ls
ls server_smartcity
ls server_smartcity/smartcity_app
```

c. Periksa kembali `manage.py` dan `smartcity_app/settings.py` untuk memastikan working directory dan module Django sesuai dengan `smartcity_app`.

```bash
cat server_smartcity/manage.py
cat server_smartcity/smartcity_app/settings.py | grep ROOT_URLCONF
cat server_smartcity/smartcity_app/settings.py | grep WSGI_APPLICATION
```

> Catatan: `project_app` harus berada di jalur yang sama dengan `WorkingDirectory` di unit service Gunicorn.

## 3. Langkah Verifikasi Lokal sebelum deployment

Jalankan perintah berikut pada komputer lokal untuk memastikan semuanya siap:

```bash
cd c:\Users\user\Documents\24782087_iet_2026\server_smartcity
. .venv\Scripts\Activate.ps1
python manage.py check
python manage.py migrate
python manage.py runserver
```

## 4. Jika konfigurasi server belum tersedia

Jika kamu belum bisa SSH ke server, gunakan checklist ini untuk menanyakan atau memeriksa:
- Nama file Nginx di `/etc/nginx/sites-available/mhsXX`
- Nama file systemd service `gunicorn-mhsXX.service`
- Port publik dan port internal Gunicorn
- Jalur `WorkingDirectory` dan `ExecStart`

## 5. Catatan penting

- Nama `server_smartcity` dan `smartcity_app` tidak wajib di Django, tetapi disyaratkan oleh konfigurasi deployment laboratorium.
- Repository ini sudah mengikuti struktur tersebut.
