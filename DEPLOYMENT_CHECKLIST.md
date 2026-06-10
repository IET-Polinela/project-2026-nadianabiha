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

## 2. Persiapan Repository dan Working Directory

a. Pada server `/home/mhsXX`, clone repository GitHub proyek ke dalam folder `project_app`:

```bash
ssh mhsXX@103.151.63.88
cd /home/mhsXX
git clone https://github.com/IET-Polinela/project-2026-nadianabiha.git project_app
```

b. Verifikasi struktur folder `project_app`:

```bash
cd /home/mhsXX/project_app
ls -la
ls -la server_smartcity
ls -la server_smartcity/smartcity_app
```

c. Pastikan `project_app` berada di jalur yang sesuai dengan `WorkingDirectory` di unit service Gunicorn.

## 3. Konfigurasi Lingkungan Terisolasi (Venv) & Database

a. Masuk ke folder `server_smartcity`:

```bash
cd /home/mhsXX/project_app/server_smartcity
```

b. Hapus virtual environment lama (jika ada) dan buat ulang:

```bash
rm -rf venv
python3 -m venv venv
```

c. Aktifkan virtual environment dan install dependency:

```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
```

d. Konfigurasi database di `settings.py` dengan kredensial yang benar:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_mhsXX',
        'USER': 'user_mhsXX',
        'PASSWORD': 'mhsXX',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

e. Jalankan migration:

```bash
python manage.py migrate
```

## 4. Mengaktifkan Gunicorn

a. Kumpulkan file statis DRF:

```bash
python manage.py collectstatic --noinput
```

b. Verifikasi status Gunicorn:

```bash
systemctl status gunicorn-mhsXX
```

Harusnya status menunjukkan `active (running)` dan berwarna hijau.

c. Jika perlu restart, informasikan ke administrator server untuk menjalankan:

```bash
sudo systemctl restart gunicorn-mhsXX
sudo systemctl reload nginx
```
