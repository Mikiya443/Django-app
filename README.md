# Earnhubs — Pure Django

Single-stack Django platform: Python backend + Django templates/CSS frontend. No Node.js or React.

Features: accounts, referrals, wallet, transactions, withdrawals, task rewards, marketplace, responsive frontend, and full Django admin control center.

## Render
Create a **Python Web Service** from this repository.
Build: `./build.sh`
Start: `gunicorn config.wsgi:application`

For real production data, attach PostgreSQL and set `DATABASE_URL`. Create an admin with `python manage.py createsuperuser`.
