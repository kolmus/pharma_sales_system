from django.contrib.auth.models import User

import pytest

from manager_app.models import Employee

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
    user = User.objects.get(username='supervisor')


    response = client.post('/employees/add/', {
        'first_name': 'Marek',
        'last_name': 'Bąkowski',
        'username': 'username5',
        'email': 'example4@something.com',
        'phone': '852369741',
        'password1': 'VerySecretPassword',
        'password2': 'VerySecretPassword',
        'role': 'Trader',
        'supervisor': user.employee.id
    })
    
    assert response.status_code == 302
    assert User.objects.get(username="username5")
    response = client.post('/employees/add/', {
        'first_name': 'rrr',
        'last_name': 'ttt',
        'username': 'qwerty',
        'email': 'example7@something.pl',
        'phone': '852355541',
        'password1': 'VerySecretPassword',
        'password2': 'VerySecretPassword',
        'role': 'Trader',
        'supervisor': user.employee.id
    })

    assert response.status_code == 302
    
    
    response = client.post('/employees/add/', {
        'first_name': '',
        'last_name': '',
        'email': '',
        'phone': '',
        'role': '',
        'supervisor': ""
    })
    assert response.status_code == 200
    
    
@pytest.mark.django_db
def test_edit_employee_page(client, logged_in_supervior_with_employee):   # form to repair
    user = User.objects.get(username='supervisor')
    employee = Employee.objects.filter(is_supervisor=False)[0]
    emp_id = employee.id
    
    response = client.post(f'/employees/edit/{employee.id}/', {
        'first_name': 'Ted',
        'last_name': employee.user.last_name,
        'email': employee.user.email,
        'phone': employee.phone,
        'role': 'masterTrader',
        'supervisor': employee.supervisor.id     
    })
   
    assert response.status_code == 302
    employee = Employee.objects.get(id=emp_id)
    
    assert employee.user.first_name == "Ted"
    assert employee.role == 'masterTrader'


    response = client.post(f'/employees/edit/{employee.id}/', {
        'first_name': 'marek',
        'last_name': 'jakistam',
        'email': 'example4@something.pl',
        'phone': 852369741,
        'role': 'Trader',
        'supervisor': ""
    })
    employee = Employee.objects.get(id=emp_id)
    assert response.status_code == 302
    assert employee.user.first_name == 'marek'
    assert employee.user.last_name == 'jakistam'
    assert employee.user.email == 'example4@something.pl'
    assert employee.phone == 852369741
    assert employee.role == 'Trader'
    assert employee.supervisor == None
    
    
    response = client.post(f'/employees/edit/{employee.id}/', {
        'first_name': 'marek',
        'last_name': '',
        'email': 'example4@something.pl',
        'phone': 852369741,
        'role': 'Trader',
        'supervisor': ""
    })

    assert response.status_code == 200

@pytest.mark.django_db


