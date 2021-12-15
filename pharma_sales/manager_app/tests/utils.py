

from django.contrib.auth.models import Permission, User

from manager_app.models import BIG_PHARM, FAMILY_PHARM, Branch, Client, Employee, REGISTER_ADRESS, FRIDAY, Product


def create_supervisor(username, password):
    print(password)
    user = User.objects.create_user(
        username=username,
        password=password,
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
    return user

def create_employee(username, password, supervisor):
    user2 = user = User.objects.create_user(
        username=username, 
        password=password, 
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
        supervisor=supervisor,
        user=user,
        is_active=True,
        is_supervisor=False
    )
    return user2

def create_2clients(nip, nip2):
    client = Client.objects.create(
        nip = nip,
        company_name = "company_name",
        short_company_name = "cmp",
        regon = 1478523,
        krs = 14478955,
        type = FAMILY_PHARM
    )
    
    client2 = Client()
    client2.nip = nip2
    client2.company_name = "company_name2"
    client2.regon = 1478723
    client2.krs = 75379
    client2.logo = None
    client2.type = BIG_PHARM
    client2.save()

    
    print(client)
    print(client2)
    return client2


def create_branch(client, employee):
    branch = Branch()
    branch.client = client
    branch.type = REGISTER_ADRESS
    branch.name_of_branch = 'name of branch2'
    branch.zip_code = '01-236'
    branch.province = 'province2'
    branch.city = 'city2'
    branch.street = 'street2'
    branch.building_number = '2020C'
    branch.apartment_number = '122l'
    branch.details = 'short notehjk'
    branch.account_manager = employee
    branch.visit_days = FRIDAY
    branch.visit_hour_from = '08:00:00'
    branch.visit_hour_to = '16:00:00'
    branch.save()
    
    branch2 = Branch()
    branch2.client = client
    branch2.type = REGISTER_ADRESS
    branch2.name_of_branch = 'name of branch2'
    branch2.zip_code = '01-336'
    branch2.province = 'province3'
    branch2.city = 'city5'
    branch2.street = 'street7'
    branch2.building_number = '20205C'
    branch2.apartment_number = '12sa2l'
    branch2.details = 'short notasehjk'
    branch2.account_manager = employee
    branch2.visit_days = FRIDAY
    branch2.visit_hour_from = '08:00:00'
    branch2.visit_hour_to = '16:00:00'
    branch2.save()
    
    return branch

def create_product(number):
    
    new_product1 = Product()
    new_product1.name = f'product'
    new_product1.description = f'description'
    new_product1.active_substance = f'substance'
    new_product1.save()
    for i in range (number-1):
        
        new_product = Product()
        new_product.name = f'product{i}'
        new_product.description = f'description{i}'
        new_product.active_substance = f'substance{i}'
        new_product.save()
        
    return new_product1