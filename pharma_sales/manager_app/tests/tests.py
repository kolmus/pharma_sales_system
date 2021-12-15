from django.contrib.auth.models import User

import datetime
from django.http import response
import pytest

from manager_app.models import THURSDAY, Employee, Client, FRIDAY, REGISTER_ADRESS, Branch, Product, Variant

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
def test_dashbord_page(client, logged_user_everymodel):
    response = client.post('/', {'employee': '2', 'note': '6543gfd', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '', 'note': 'dfghjk', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '2', 'note': '', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302
    
    response = client.post('/', {'employee': '', 'note': '', 'date_cal': '2021-12-15 Środa'})
    assert response.status_code == 302

@pytest.mark.django_db
def test_create_employee_page(client, logged_user_everymodel):  
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
def test_edit_employee_page(client, logged_user_everymodel):   # form to repair
    
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
def test_branch_create(client, logged_user_everymodel):
    
    employee = Employee.objects.filter(is_supervisor=False)[0]
    client_in_base = Client.objects.all()[0]
    client_id = client_in_base.id
    
    assert len(Branch.objects.filter(name_of_branch='name of branch')) == False
    print(employee.id)
    response = client.post(f'/branch/add/', {
        'client': client_id,
        'type': REGISTER_ADRESS,
        'name_of_branch': 'name of branch',
        'zip_code': '01-234',
        'province': 'province',
        'city': 'city',
        'street': 'street',
        'building_number': '200C',
        'apartment_number': '12l',
        'details': 'short note',
        'account_manager': employee.id,
        'visit_days': FRIDAY,
        'visit_hour_from': '08:00:00',
        'visit_hour_to': '16:00:00'
    })
    

    assert response.status_code == 302
    branch = Branch.objects.get(client=client_in_base)
    assert branch.type == REGISTER_ADRESS
    assert branch.name_of_branch == 'name of branch'
    assert branch.zip_code == '01-234'
    assert branch.province == 'province'
    assert branch.city == 'city'
    assert branch.street == 'street'
    assert branch.building_number == '200C'
    assert branch.apartment_number == '12l'
    assert branch.details == 'short note'
    assert branch.visit_days == FRIDAY
    assert branch.visit_hour_from == datetime.time(8, 0)
    assert branch.visit_hour_to == datetime.time(16, 0)

@pytest.mark.django_db
def test_edit_branch(client, logged_user_everymodel):
    
    
    employee = Employee.objects.filter(is_supervisor=False)[0]
    client_in_base = Client.objects.all()[0]
    branch = Branch.objects.all()[0]
    br_id = branch.id
    

    assert branch.name_of_branch != 'name of branch => loremipsum'
    assert branch.zip_code != '02-495'
    assert branch.province != 'provinceggg'
    assert branch.city != 'cityggg'
    assert branch.street != 'streetggg'
    assert branch.building_number != '2008C'
    assert branch.apartment_number != '12sl'
    assert branch.details != 'short note edited branch'
    assert branch.visit_hour_from != datetime.time(7, 0)
    assert branch.visit_hour_to != datetime.time(17, 0)
    
    
    response = client.post(f'/branch/edit/{branch.id}/', {
        'client': branch.client.id,
        'type': REGISTER_ADRESS,
        'name_of_branch': 'name of branch => loremipsum',
        'zip_code': '02-495',
        'province': 'provinceggg',
        'city': 'cityggg',
        'street': 'streetggg',
        'building_number': '2008C',
        'apartment_number': '12sl',
        'details': 'short note edited branch',
        'account_manager': employee.id,
        'visit_days': THURSDAY,
        'visit_hour_from': '07:00:00',
        'visit_hour_to': '17:00:00'
    })
    

    assert response.status_code == 302
    branch = Branch.objects.get(id=br_id)
    assert branch.type == REGISTER_ADRESS
    assert branch.name_of_branch == 'name of branch => loremipsum'
    assert branch.zip_code == '02-495'
    assert branch.province == 'provinceggg'
    assert branch.city == 'cityggg'
    assert branch.street == 'streetggg'
    assert branch.building_number == '2008C'
    assert branch.apartment_number == '12sl'
    assert branch.details == 'short note edited branch'
    assert branch.visit_days == THURSDAY
    assert branch.visit_hour_from == datetime.time(7, 0)
    assert branch.visit_hour_to == datetime.time(17, 0)
    

@pytest.mark.django_db
def test_add_product(client, logged_user_everymodel):
    
    assert len(Product.objects.all()) == 6

    response = client.post(f'/products/add/', {
        'name': 'name of product',
        'description': 'some description',
        'active_substance': 'anything'
    })
    
    assert response.status_code == 302
    assert len(Product.objects.all()) == 7
    product = Product.objects.get(name = 'name of product')
    assert product.description == 'some description'
    assert product.active_substance == 'anything'
    
@pytest.mark.django_db
def test_edit_product(client, logged_user_everymodel):
    
    product = Product.objects.all()[0]
    pr_id = product.id
    
    assert product.name != 'name of product test2'
    assert product.description != 'some description test2'
    assert product.active_substance != 'anything test2'
    response = client.post(f'/products/edit/{pr_id}/', {
        'name': 'name of product test2',
        'description': 'some description test2',
        'active_substance': 'anything test2'
    })
    product = Product.objects.get(id = pr_id)
    assert response.status_code == 302
    assert product.name == 'name of product test2'
    assert product.description == 'some description test2'
    assert product.active_substance == 'anything test2'
    
