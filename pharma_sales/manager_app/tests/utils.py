
from django.contrib.auth.models import Permission, User
from trader_app.models import Visit
from manager_app.models import (
    BIG_PHARM,
    FAMILY_PHARM,
    Branch,
    Client,
    Employee,
    REGISTER_ADRESS,
    FRIDAY,
    Product,
    Variant,
    Batch,
    Order,
    Cart,
    
)


def create_supervisor(username, password):
    """for tests - create supervisor employe

    Args:
        username (str): [new username]
        password (str): [secret password]

    Returns:
        user [object]: [object of User model]
    """    
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
    """For Tests
    creates user vitr trader permitions.
    
    Args:
        username ([str]): [new username]
        password ([str]): [secret password ]
        supervisor ([object]): [model Employee]

    Returns:
        [object]: [Auth User Model]
    """    
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
    """For Tests
    creates 2 objects of Client model

    Args:
        nip ([int]): [int or bigint]
        nip2 ([int]): [int or bigint]

    Returns:
        [object]: Model Client object with nip2
    """    
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
    """For Tests
    
    Creates new Branch model

    Args:
        client ([obj]): [Model Client]
        employee ([obj]): [Model Employ, permissions as trader]

    Returns:
        [object]: [New object of model Branch]
    """    
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
    branch2.city = 'city2'
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
    """For Tests
     
     Creates new object of Product Model
    Args:
        number ([int]): number of new objects

    Returns:
        [object]: [New object of Product Model]
    """    
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

def create_variant(product, number):
    """For Tests

    Creates new object of Variant Model

    Args:
        product (obj): Model Product
        number (int): number of new objects

    Returns:
        object: New object of Variant Model
    """    
    variant = Variant()
    variant.dose = 1
    variant.unit = 1
    variant.in_package = 20
    variant.product = product
    variant.is_active = True
    variant.save()
    
    for i in range(number - 1):
        variant1 = Variant()
        variant1.dose = (1 + i)
        variant1.unit = (1 + i)
        variant1.in_package = (20 + i)
        variant1.product = product
        variant1.is_active = True
        variant1.save()
    return variant
        
def create_batch(variant, number):
    """For Tests

    Creates new object of Batch Model

    Args:
        variant (obj): Model Variant
        number (int): number of new objects

    Returns:
        object: New object of Batch Model
    """    
    batch = Batch()
    batch.number = 'batch number'
    batch.ean = 147852
    batch.expiration_date = '2022-01-30'
    batch.netto = 400.31
    batch.vat = 1
    batch.quantity = 4000
    batch.variant = variant
    batch.is_active = True
    batch.save()
    
    for i in range(number - 1):
        batch = Batch()
        batch.number = f'batch number{i}'
        batch.ean = 147852
        batch.expiration_date = '2022-01-30'
        batch.netto = 400.31 + i * 10
        batch.vat = 1
        batch.quantity = 4000 + i * 100
        batch.variant = variant
        batch.is_active = True
        batch.save()
    return batch
        
def create_order(branch, number):
    """For Tests

    Creates new object of Order Model

    Args:
        branch (obj): Model Branch
        number (int): number of new objects

    Returns:
        object: New object of Order Model
    """    
    order = Order()
    order.order_number = 'Order number'
    order.branch = branch
    order.save()
    
    for i in range(number - 1):
        order1 = Order()
        order1.order_number = f'Order number {i}'
        order1.branch = branch
        order1.save()
    return order
    
def create_cart_position(order, batch):
    """For Tests

    Creates new object of Cart Model

    Args:
        order (obj): Model Order

    Returns:
        object: New object of Cart Model
    """    
    position = Cart()
    position.order = order
    position.batch = batch
    position.quantity = 3
    position.save()
    return position

def create_visit(branch, user):
    """For Test
    Creates 1 object of Visit modlue

    Args:
        branch (obj): Object of Branch model
        user (obj): Object of User model

    Returns:
        Object: 1 new object of Visit Model
    """    
    visit = Visit()
    visit.date = '2021-12-16'
    visit.trader = user.employee
    visit.client_branch = branch
    visit.save()
    return visit
