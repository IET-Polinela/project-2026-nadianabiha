# Smart City Issue Tracker

NPM: 24782087  
Nama: Nadia Nabiha Dziqra

## Struktur Project

- `server_smartcity/` - Backend Django, Django REST Framework API, portal admin, dan unit test backend.
- `smartcity_citizen_spa_24782087/` - Frontend Citizen Portal berbasis SPA.
- `tests/e2e/` - Automated End-to-End Testing menggunakan Playwright.
- `scripts/run-playwright-lab15.ps1` - Script untuk menjalankan backend, frontend, lalu Playwright test.

## Perintah Lab 15

Backend unit test:

```bash
cd server_smartcity
python manage.py test main_app
```

Coverage:

```bash
cd server_smartcity
python -m coverage run manage.py test main_app
python -m coverage report
```

Playwright E2E:

```bash
npm test
```
