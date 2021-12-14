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
    
@pytest.mark.django_db
def test_dashbord_page(client, logged_in_supervior_with_employee):
    response = client.post('/', {'employee': '2', 'note': '6543gfd', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '', 'note': 'dfghjk', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '2', 'note': '', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '', 'note': '', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302

@pytest.mark.django_db
def test_create_employee_page(client, logged_in_supervior_with_employee):  
    response = client.post('/employees/add/', {
        'first_name': 'marek',
        'last_name': 'jakistam',
        'username': 'username5',
        'email': 'example4@something.pl',
        'phone': '852369741',
        'password1': 'VerySecretPassword',
        'password2': 'VerySecretPassword',
        'role': 'Trader',
        'supervisor': ''        # to analise
    })
    assert response.status_code == 302
    
    response = client.post('/employees/add/', {
        'first_name': 'marek',
        'last_name': 'jakistam',
        'email': 'example4@something.pl',
        'phone': 852369741,
        'role': 'Trader',
        'supervisor': ""
    })
    assert response.status_code == 200
    
    
    
    