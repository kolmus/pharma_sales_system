import pytest
from django.contrib.auth.models import User
from datetime import date, datetime


from trader_app.models import Visit
from manager_app.models import Employee, Client, Branch, Variant, Order, Cart, CREATING_ST, TO_VERIFY_ST

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
    
@pytest.mark.django_db
def test_trader_planning_view(client, trader_logged_user_everymodel):
    response = client.post('/trader/planning/', {'plan_date': '2012-12-16', 'city': 'city2'})   # to update after change form
    assert response.status_code == 302
    response = client.post('/trader/planning/', {'plan_date': '2012-12-16', 'city': ''})
    assert response.status_code == 200

@pytest.mark.django_db
def test_trader_add_visit(client, trader_logged_user_everymodel):
    branches = Branch.objects.filter(city = 'city2')                 # to update after chaange planning view form
    visits = len(Visit.objects.all())
    response = client.post('/trader/planning/2012-12-16/city2/', {'branch': branches[0].id})
    assert response.status_code == 200
    assert len(Visit.objects.all()) == visits + 1

@pytest.mark.django_db
def test_trader_delete_visit(client, trader_logged_user_everymodel):
    visits = len(Visit.objects.all())
    visit = Visit.objects.all()[0]
    visit_id = visit.id
    response = client.post(f'/trader/planning/2012-12-16/city2/{visit_id}/delete/')
    assert response.status_code == 302
    assert len(Visit.objects.all()) == visits - 1
    assert len(Visit.objects.filter(id = visits)) == 0
    
    
@pytest.mark.django_db
def test_trader_add_Order_and_cart(client, trader_logged_user_everymodel):
    branch = Branch.objects.all()[0]
    bran_id = branch.id
    variant = Variant.objects.all()[0]
    var_id = variant.id
    visit_id = Visit.objects.all()[0].id
    orders = len(Order.objects.all())
    carts = len(Cart.objects.all())
    
    response = client.post(f'/trader/visit/{visit_id}/{bran_id}/order/add/', {
        'variant': var_id,
        'quantity': 1
    })
    assert response.status_code == 302
    assert len(Order.objects.all()) == orders + 1
    assert len(Cart.objects.all()) == carts + 1
    
@pytest.mark.django_db
def test_trader_add_position_to_cart(client, trader_logged_user_everymodel):
    order = Order.objects.filter(order_status = CREATING_ST)[0]
    positions = len(order.cart_set.all())
    branch = order.branch
    bran_id = branch.id
    ord_id = order.id
    variant = Variant.objects.all()[0]
    var_id = variant.id
    visit_id = Visit.objects.all()[0].id
    
    response = client.post(f'/trader/visit/{visit_id}/{bran_id}/orders/{ord_id}/', {
        'variant': var_id,
        'quantity': 1
    })

    assert response.status_code == 200
    assert len(order.cart_set.all()) == positions + 1

@pytest.mark.django_db
def test_trader_delete_position_from_cart(client, trader_logged_user_everymodel):
    order = Order.objects.filter(order_status = CREATING_ST)[0]
    positions = len(order.cart_set.all())
    position = order.cart_set.all()[0]
    pos_id = position.id
    ord_id = order.id
    visit = Visit.objects.all()[0]
    visit_id = visit.id
    bran_id = visit.client_branch.id
    
    response = client.post(f'/trader/visit/{visit_id}/{bran_id}/delete/{pos_id}/')
    order = Order.objects.get(id=ord_id)
    assert response.status_code == 302
    assert len(order.cart_set.all()) == positions - 1
    assert len(Cart.objects.filter(id = pos_id)) == 0
    
@pytest.mark.django_db
def test_trader_update_order_status(client, trader_logged_user_everymodel):
    order = Order.objects.all()[0]
    ord_id = order.id
    visit = Visit.objects.all()[0]
    visit_id = visit.id
    bran_id = visit.client_branch.id
    
    response = client.post(f'/trader/visit/{visit_id}/{bran_id}/orders/{ord_id}/status/{CREATING_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == CREATING_ST
    response = client.post(f'/orders/{ord_id}/status/{TO_VERIFY_ST}/')
    assert response.status_code == 302
    order = Order.objects.get(id=ord_id)
    assert order.order_status == TO_VERIFY_ST
    
@pytest.mark.django_db
def test_trader_end_visit(client, trader_logged_user_everymodel):          
    visit = Visit.objects.all()[0]
    visit_id = visit.id
    assert visit.visited != True
    response = client.post(f'/trader/visit/{visit_id}/visited/')
    visit = Visit.objects.get(id = visit_id)
    assert visit.visited == True
    assert response.status_code == 302
    

    