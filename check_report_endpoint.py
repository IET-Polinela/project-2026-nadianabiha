import os
import sys
import django

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server_smartcity'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcity_app.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()
res = client.get('/api/report/')
print('unauth', res.status_code)
print(res.content.decode())

user = User.objects.filter(username='citizen1').first()
print('citizen1 exists', bool(user), user)
if user:
    client.force_login(user)
    res2 = client.get('/api/report/')
    print('auth', res2.status_code)
    print(res2.content.decode()[:1000])
