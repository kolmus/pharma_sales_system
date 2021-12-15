

from django.contrib.auth.models import Permission, User

from manager_app.models import Employee


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