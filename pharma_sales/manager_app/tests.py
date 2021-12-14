import pytest
from django.contrib.auth import authenticate, login, logout

@pytest.mark.django_db
def test_login_page(client, three_exemple_users):
    
    response = client.post('/login/', {'login': 'sdfghj', 'password': 'zsexdrcftvgybnujim'})
    assert response.status_code == 200
    response = client.post('/login/', {'login': 'supervisor_login', 'password': 'supervisor_password'})
    assert response.status_code == 302
    response = client.get('/')
    assert response.status_code == 200
    response = client.post('/login/', {'login': 'trader_login', 'password': 'trader_password'})
    assert response.status_code == 302
    response = client.get('/')
    assert response.status_code == 403
    response = client.post('/login/', {'login': 'noperm_login', 'password': 'noperm_password'})
    assert response.status_code == 302
    response = client.get('/')
    assert response.status_code == 403
    

