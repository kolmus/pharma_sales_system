from django.contrib.auth.models import User

import datetime
import pytest

from manager_app.models import (
    THURSDAY,
    Employee,
    Client,
    FRIDAY,
    REGISTER_ADRESS,
    Branch,
    Product,
    Variant,
    Batch,
    Order,
    Cart,
    CREATING_ST,
    TO_VERIFY_ST,
    WAIT_FOR_PAY_ST,
    ACCEPTED_ST,
    TO_DELIVER_ST,
    PROBLEM_ST,
    IN_DELIVERY_ST,
    NOT_PAYED_ST,
    ENDED_ST
    
    
)
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
    
    assert len(Branch.objects.filter(name_of_branch='name of branch')) == 0
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
    
@pytest.mark.django_db
def test_add_batch(client, logged_user_everymodel):
    
    variant = Variant.objects.all()[0]
    var_id = variant.id
    
    assert len(Batch.objects.all()) == 3
    assert len(Batch.objects.filter(number = 'new batch number')) == 0
    
    response = client.post(f'/batch/add/', {
        'number': 'new batch number',
        'ean': 1478523,
        'expiration_date': '2022-01-30',
        'netto': 400.31,
        'vat': 1,
        'quantity': 4000,
        'variant': variant.id,
        'is_active': True,
    })
    assert response.status_code == 302
    assert len(Batch.objects.all()) == 4
    batch = Batch.objects.get(number = 'new batch number')
    assert batch.ean == 1478523
    assert batch.expiration_date == datetime.date(2022, 1, 30)
    assert batch.netto == 400.31
    assert batch.vat == 1
    assert batch.quantity == 4000
    assert batch.variant == variant
    assert batch.is_active == True
    
@pytest.mark.django_db
def test_add_Order_and_cart(client, logged_user_everymodel):
    branch = Branch.objects.all()[0]
    bran_id = branch.id
    variant = Variant.objects.all()[0]
    var_id = variant.id
    
    orders = len(Order.objects.all())
    carts = len(Cart.objects.all())
    
    response = client.post(f'/branch/{bran_id}/orders/add/', {
        'variant': var_id,
        'quantity': 1
    })
    assert response.status_code == 302
    assert len(Order.objects.all()) == orders + 1
    assert len(Cart.objects.all()) == carts + 1

@pytest.mark.django_db
def test_add_position_to_cart(client, logged_user_everymodel):
    order = Order.objects.filter(order_status = CREATING_ST)[0]
    positions = len(order.cart_set.all())
    branch = order.branch
    bran_id = branch.id
    ord_id = order.id
    variant = Variant.objects.all()[0]
    var_id = variant.id
    
    response = client.post(f'/branch/{bran_id}/orders/{ord_id}/', {
        'variant': var_id,
        'quantity': 1
    })

    assert response.status_code == 200
    assert len(order.cart_set.all()) == positions + 1
    
@pytest.mark.django_db
def test_delete_position_from_cart(client, logged_user_everymodel):
    order = Order.objects.filter(order_status = CREATING_ST)[0]
    positions = len(order.cart_set.all())
    position = order.cart_set.all()[0]
    pos_id = position.id
    ord_id = order.id
    
    response = client.post(f'/orders/{ord_id}/delete/{pos_id}/')
    print(response.content)
    order = Order.objects.get(id=ord_id)
    assert response.status_code == 302
    assert len(order.cart_set.all()) == positions - 1
    assert len(Cart.objects.filter(id = pos_id)) == 0
    
@pytest.mark.django_db
def test_update_order_status(client, logged_user_everymodel):
    order = Order.objects.all()[0]
    ord_id = order.id
    
    response = client.post(f'/orders/{ord_id}/status/{CREATING_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == CREATING_ST
    response = client.post(f'/orders/{ord_id}/status/{TO_VERIFY_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == TO_VERIFY_ST
    response = client.post(f'/orders/{ord_id}/status/{WAIT_FOR_PAY_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == WAIT_FOR_PAY_ST
    response = client.post(f'/orders/{ord_id}/status/{ACCEPTED_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == ACCEPTED_ST
    response = client.post(f'/orders/{ord_id}/status/{TO_DELIVER_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == TO_DELIVER_ST
    response = client.post(f'/orders/{ord_id}/status/{PROBLEM_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == PROBLEM_ST
    response = client.post(f'/orders/{ord_id}/status/{IN_DELIVERY_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == IN_DELIVERY_ST
    response = client.post(f'/orders/{ord_id}/status/{NOT_PAYED_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == NOT_PAYED_ST
    response = client.post(f'/orders/{ord_id}/status/{ENDED_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == ENDED_ST
    
@pytest.mark.django_db
def test_order_delete(client, logged_user_everymodel):
    orders = Order.objects.all()
    ord_id = orders[0].id
    len_orders = len(orders)
    response = client.post(f'/orders/{ord_id}/delete/')
    orders = Order.objects.all()
    assert response.status_code == 302
    assert len(orders) == len_orders -1
    assert len(Order.objects.filter(id = ord_id)) == 0

@pytest.mark.django_db
def test_order_modify (client, logged_user_everymodel):
    order = Order.objects.all()[0]
    ord_id = order.id
    assert order.order_number != "Nowy numer do zamówienia"
    assert order.branch != 5
    bran_id = order.branch.id
    response = client.post(f'/orders/{ord_id}/cs/', {
        'order_number': 'Nowy numer do zamówienia',
        'discount': 5
    })
    
    assert response.status_code == 200
    
    response = client.post(f'/orders/{ord_id}/cs/', {
        'order_number': 'Nowy numer do zamówienia',
        'branch': bran_id,
        'discount': 5
    })
    
    order = Order.objects.get(id = ord_id)
    assert order.order_number == "Nowy numer do zamówienia"
    assert order.discount == 5
    assert order.branch == Branch.objects.get(id=bran_id)
    