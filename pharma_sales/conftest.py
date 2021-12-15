from django.contrib.auth.models import Permission, User
import pytest

from manager_app.models import (
    Employee
)
from manager_app.tests.utils import create_branch, create_product, create_supervisor, create_employee, create_2clients

@pytest.fixture
def three_exemple_users():
    
    user = User.objects.create_user(
        username='supervisor_login',
        password='supervisor_password',
        first_name='name1',
        last_name='surname1',
        email = 'exemple@anything.com'
    )
    user.user_permissions.add(Permission.objects.get(codename='add_batch'))
    user.user_permissions.add(Permission.objects.get(codename='change_batch'))
    user.user_permissions.add(Permission.objects.get(codename='delete_batch'))
    user.user_permissions.add(Permission.objects.get(codename='view_batch'))
    user.user_permissions.add(Permission.objects.get(codename='add_branch'))
    user.user_permissions.add(Permission.objects.get(codename='change_branch'))
    user.user_permissions.add(Permission.objects.get(codename='delete_branch'))
    user.user_permissions.add(Permission.objects.get(codename='view_branch'))
    user.user_permissions.add(Permission.objects.get(codename='add_cart'))
    user.user_permissions.add(Permission.objects.get(codename='change_cart'))
    user.user_permissions.add(Permission.objects.get(codename='delete_cart'))
    user.user_permissions.add(Permission.objects.get(codename='view_cart'))
    user.user_permissions.add(Permission.objects.get(codename='add_client'))
    user.user_permissions.add(Permission.objects.get(codename='change_client'))
    user.user_permissions.add(Permission.objects.get(codename='delete_client'))
    user.user_permissions.add(Permission.objects.get(codename='view_client'))
    user.user_permissions.add(Permission.objects.get(codename='add_employee'))
    user.user_permissions.add(Permission.objects.get(codename='change_employee'))
    user.user_permissions.add(Permission.objects.get(codename='delete_employee'))
    user.user_permissions.add(Permission.objects.get(codename='view_employee'))
    user.user_permissions.add(Permission.objects.get(codename='add_invoice'))
    user.user_permissions.add(Permission.objects.get(codename='change_invoice'))
    user.user_permissions.add(Permission.objects.get(codename='delete_invoice'))
    user.user_permissions.add(Permission.objects.get(codename='view_invoice'))
    user.user_permissions.add(Permission.objects.get(codename='add_order'))
    user.user_permissions.add(Permission.objects.get(codename='change_order'))
    user.user_permissions.add(Permission.objects.get(codename='delete_order'))
    user.user_permissions.add(Permission.objects.get(codename='view_order'))
    user.user_permissions.add(Permission.objects.get(codename='add_product'))
    user.user_permissions.add(Permission.objects.get(codename='change_product'))
    user.user_permissions.add(Permission.objects.get(codename='delete_product'))
    user.user_permissions.add(Permission.objects.get(codename='view_product'))
    user.user_permissions.add(Permission.objects.get(codename='add_variant'))
    user.user_permissions.add(Permission.objects.get(codename='change_variant'))
    user.user_permissions.add(Permission.objects.get(codename='delete_variant'))
    user.user_permissions.add(Permission.objects.get(codename='view_variant'))
    user.user_permissions.add(Permission.objects.get(codename='add_visit'))
    user.user_permissions.add(Permission.objects.get(codename='change_visit'))
    user.user_permissions.add(Permission.objects.get(codename='delete_visit'))
    user.user_permissions.add(Permission.objects.get(codename='view_visit'))
    user.user_permissions.add(Permission.objects.get(codename='add_user'))
    user.user_permissions.add(Permission.objects.get(codename='add_permission'))

    employee = Employee.objects.create(
        phone=123456789,
        role='Supervisor',
        supervisor=None,
        user=user,
        is_active=True,
        is_supervisor=True
    )
    
    user2 = user = User.objects.create_user(
        username='trader_login', 
        password='trader_password', 
        first_name='name2',
        last_name='surname2',
        email = 'exemple2@anything.com'
    )
    user2.user_permissions.add(Permission.objects.get(codename='change_batch'))
    user2.user_permissions.add(Permission.objects.get(codename='view_batch'))
    user2.user_permissions.add(Permission.objects.get(codename='add_branch'))
    user2.user_permissions.add(Permission.objects.get(codename='change_branch'))
    user2.user_permissions.add(Permission.objects.get(codename='view_branch'))
    user2.user_permissions.add(Permission.objects.get(codename='add_cart'))
    user2.user_permissions.add(Permission.objects.get(codename='change_cart'))
    user2.user_permissions.add(Permission.objects.get(codename='delete_cart'))
    user2.user_permissions.add(Permission.objects.get(codename='view_cart'))
    user2.user_permissions.add(Permission.objects.get(codename='add_client'))
    user2.user_permissions.add(Permission.objects.get(codename='change_client'))
    user2.user_permissions.add(Permission.objects.get(codename='view_client'))
    user2.user_permissions.add(Permission.objects.get(codename='add_order'))
    user2.user_permissions.add(Permission.objects.get(codename='change_order'))
    user2.user_permissions.add(Permission.objects.get(codename='delete_order'))
    user2.user_permissions.add(Permission.objects.get(codename='view_order'))
    user2.user_permissions.add(Permission.objects.get(codename='view_product'))
    user2.user_permissions.add(Permission.objects.get(codename='view_variant'))
    user2.user_permissions.add(Permission.objects.get(codename='add_visit'))
    user2.user_permissions.add(Permission.objects.get(codename='change_visit'))
    user2.user_permissions.add(Permission.objects.get(codename='delete_visit'))
    user2.user_permissions.add(Permission.objects.get(codename='view_visit'))
    employee2 = Employee.objects.create(
      phone=123456789,
        role='Trader',
        supervisor=employee,
        user=user,
        is_active=True,
        is_supervisor=False
    )
    
    user3 = user = User.objects.create_user(
        username='noperm_login', 
        password='noperm_password', 
        first_name='name3',
        last_name='surname3',
        email = 'exemple3@anything.com'
    )

    users = [user, user2, user3]
    return users


@pytest.fixture
def logged_user_everymodel(client):
    user = create_supervisor(username='supervisor', password="SecretPassword")
    user2 = create_employee(username='trader', password="SecretPassword", supervisor=user.employee)
    new_client = create_2clients(nip=5222851, nip2=45876321)
    new_branch = create_branch(new_client, user2.employee)
    new_product = create_product(6)
    client.login(
        username='supervisor',
        password='SecretPassword',
    )
    
    print("####################" + str(user.employee.id))
    print('username ', user.username)
    print('password   ', user.password)
    print('new client id  ', new_client.id)
    print('new branch id    ', new_branch.id)
    print('New product id', new_product.id)
    print("####################" + str(user2.employee.id))
    
    return client, user

