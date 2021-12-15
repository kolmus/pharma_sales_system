import pytest
from django.contrib.auth.models import User
import datetime

from manager_app.models import Employee, Client, Branch

@pytest.mark.django_db
def test_trader_login_page(client, three_exemple_users):
    response = client.post('/trader/login/', {'login': 'sdfghj', 'password': 'zsexdrcftvgybnujim'})
    assert response.status_code == 200
    response = client.post('/trader/login/', {'login': 'supervisor_login', 'password': 'supervisor_password'})
    assert response.status_code == 302
    response = client.get('/trader/')
    assert response.status_code == 403
    response = client.post('/trader/login/', {'login': 'trader_login', 'password': 'trader_password'})
    assert response.status_code == 302
    response = client.get('/trader/')
    assert response.status_code == 200
    response = client.post('/trader/login/', {'login': 'noperm_login', 'password': 'noperm_password'})
    assert response.status_code == 302
    response = client.get('/trader/')
    assert response.status_code == 403
    
    