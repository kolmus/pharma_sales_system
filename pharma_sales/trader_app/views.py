from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.views import View
from datetime import date

from manager_app.models import (
    FAMILY_PHARM,
    REGISTER_ADRESS,
    Branch,
    Order,
    Cart,
    Product,
    Client
)
from manager_app.forms import LoginForm, CartForm
from .models import Visit, Localization
from .forms import ClientByNipForm, PlanDateForm, PlanAddVisitForm, MakeVisitForm


def save_coordinates(request, note):
    """Function saves gps coordinates in Localization model

    Args:
        request (object): from View 
        note (str): note about reason of save location
    """    
    try:
        Localization.objects.create(
            latitude = float(request.COOKIES['lat']),
            longitude = float(request.COOKIES['long']),
            employee = request.user.employee,
            note = note
        )
    except KeyError: 
        Localization.objects.create(
            employee = request.user.employee,
            note = note
        )

class TraderLoginView(View):
    """View created for login page

    Args:
        LoginForm (class): Form with login and password
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'trader_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['login'], 
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('/trader/')
            else:
                return render(request, 'trader_app/login.html', {'form': form, 'answer': 'Błędny login lub hasło'})
        else: 
            return render(request, 'trader_app/login.html', {'form': form})


class TraderLogoutView(LoginRequiredMixin, View):
    """
    View created to logout
    """
    def get(self, request):
        logout(request)
        return redirect("/trader/login/")


class TraderDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for dashboard page
    """
    permission_required = 'trader_app.add_visit' 
    def get(self, request):
        return render(request, 'trader_app/dashboard.html')


class TraderStartDayView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View starts day of work
    """
    permission_required = 'trader_app.view_visit' 
    
    def get(self, request):
        save_coordinates(request, 'Otwarty plan dnia')
        if Visit.objects.filter(date=date.today(), trader=request.user.employee, visited=False,).exists:
            visits = Visit.objects.filter(date=date.today(), trader=request.user.employee, visited=False,)
            resp = render (request, 'trader_app/start_day.html', {'visits': visits})
        else: 
            resp = render (request, 'trader_app/start_day.html', {'message': 'Nie masz zaplanowanych wizyt na dziś'})
        return resp


class TraderPlaningDateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for choise date and city
    """
    permission_required = 'trader_app.add_visit' 
    
    def get(self, request):
        form= PlanDateForm(initial={'plan_date': date.today()})
        return render(request, 'trader_app/planning.html', {'form': form})
    
    def post(self, request):
        form = PlanDateForm(request.POST)
        if form.is_valid():
            return redirect(f"/trader/planning/{form.cleaned_data['plan_date']}/{form.cleaned_data['city']}/")
        else:
            return render(request, 'trader_app/planning.html', {'form': form})


class TraderPlaningVisitsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View creates new visits.
    """
    
    permission_required = ('trader_app.add_visit', 'trader_app.delete_visit') 
    
    def get(self, request, plan_date, city):
        visits = Visit.objects.filter(date=plan_date, visited=False)
        form = PlanAddVisitForm()
        form.fields['branch'].queryset = Branch.objects.filter(account_manager=request.user.employee, city=city)
        if len(visits) < 12:
            message = f'Brakuje Ci {12 - len(visits)} wizyt do celu'
        else:
            message = f'Zaplanowałeś {len(visits)} spotkań.'
        
        
        return render(request, 'trader_app/planning_visit_form.html', {
            'visits': visits,
            'form': form,
            'message': message,
        })
    
    def post(self, request, plan_date, city):
        form_queryset = Branch.objects.filter(account_manager=request.user.employee, city=city)
        form = PlanAddVisitForm(request.POST)
        form.fields['branch'].queryset = form_queryset
        if form.is_valid():
            new_visit = Visit.objects.create(
                date=plan_date,
                trader=request.user.employee,
                client_branch=form.cleaned_data['branch']
            )
            visits = Visit.objects.filter(date=plan_date, visited=False)
            new_form= PlanAddVisitForm()
            new_form.fields['branch'].queryset = form_queryset
            
            if len(visits) < 12:
                message = f'Brakuje Ci {12 - len(visits)} wizyt do celu'
            else:
                message = f'Zaplanowałeś {len(visits)} spotkań.'
            return render(request, 'trader_app/planning_visit_form.html', {
                'visits': visits,
                'form': new_form,
                'message': message,
            })
        else:
            visits = Visit.objects.filter(date=plan_date, visited=False)
            if len(visits) < 12:
                message = f'Brakuje Ci {12 - len(visits)} wizyt do celu'
            else:
                message = f'Zaplanowałeś {len(visits)} spotkań.'
            return render(request, 'trader_app/planning_visit_form.html', {
                'visits': visits,
                'form': form,
                'message': message,
            })


class TraderVisitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'trader_app.delete_visit' 
    """
    View delentes positionfrom cart
    """
    def post(self, request, visit_id, visit_date, visit_city):
        Visit.objects.get(id=visit_id).delete()
        return redirect(f'/trader/planning/{visit_date}/{visit_city}/')


class TraderVisitView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for visits
    """
    permission_required = 'trader_app.view_visit' 
    
    def get(self, request, visit_id):
        #Lokaliztion
        visit = Visit.objects.get(id=visit_id)
        save_coordinates(request, f'Wejście w wizytę {visit.client_branch}')
        
        visit = Visit.objects.get(id=visit_id)
        if visit.note or visit.proof_img:
            form = MakeVisitForm(initial={
                'proof_img':visit.proof_img,
                'note': visit.note
            })
        else:
            form = MakeVisitForm()
        return render(request, 'trader_app/visit.html', {'form': form, 'visit': visit})
    
    def post(self, request, visit_id):
        visit = Visit.objects.get(id=visit_id)
        save_coordinates(request, f'Zdjęcie z wizyty {visit.client_branch}')
        form = MakeVisitForm (request.POST, request.FILES, instance=Visit.objects.get(id=visit_id))
        # visit = Visit.objects.get(id=visit_id)
        if form.is_valid():

            
            visit =form.save()
            return render(request, 'trader_app/visit.html', {'form': form, 'visit': visit})
        else: 
            return render(request, 'trader_app/visit.html', {'form': form, 'visit': visit})


class TraderProductsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to show Products list
    """
    permission_required = 'manager_app.view_product' 
    
    def get(self, request, visit_id):
        products = Product.objects.filter(is_active=True)
        
        return render(request, 'trader_app/products.html', {'products': products, 'visit_id': visit_id})


class TraderProductDetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to show details 
    """
    permission_required = 'manager_app.view_product' 
    
    def get(self, request, visit_id, product_id):
        visit = Visit.objects.get(id=visit_id)
        save_coordinates(request, f'Wejście w szczeguły produktu {visit.branch}')
        
        product = Product.objects.get(id=product_id)
        print(product.variant_set.all())
        return render(request, 'trader_app/product_details.html', {'product': product, 'visit_id': visit_id})


class TraderOrderCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for making orders
    """
    permission_required = ('manager_app.add_cart', 'manager_app.add_order') 

    def get(self, request, branch_id, visit_id):
        branch = Branch.objects.get(id=branch_id)
        form = CartForm()
        return render(request, 'trader_app/cart_form.html', {'title': f'Nowe zamówienie dla {branch}', 'form': form, 'visit_id': visit_id})
    
    def post(self, request, branch_id, visit_id):
        form = CartForm(request.POST)
        branch = Branch.objects.get(id = branch_id)
            
        if form.is_valid():
            # create order
            today = date.today()
            order_number = '{}/{}/{}/{}'.format(
                branch.id,
                today.year,
                today.month,
                len(Order.objects.filter(branch=branch, date__year__gte=int(today.year), date__month__gte=int(today.month)))+1  # to change for something more uniq
            )
            order = Order.objects.create(
                order_number=order_number,
                branch=branch,
            )
            
            # Create cart
            cart = Cart()
            cart.order = order
            cart.quantity = int(form.cleaned_data['quantity'])
            
            variant = form.cleaned_data.get('variant')
            batch = variant.batch_set.filter(is_active=True)[0]
            for element in variant.batch_set.filter(is_active=True):
                if element.quantity < batch.quantity and element.quantity > int(form.cleaned_data['quantity']):
                    batch  = element
            cart.batch = batch
            cart.save()
            
            return redirect(f'/trader/visit/{visit_id}/{branch.id}/orders/{order.id}/')
        else:
            return render(request, 'trader_app/cart_form.html', {'title': f'Nowe zamówienie dla {branch}', 'form': form})


class TraderCartModifyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for adding posiotions to Cart
    """
    permission_required = ('manager_app.add_cart', 'manager_app.delete_cart') 
    
    def get(self, request, visit_id, branch_id, order_id):
        branch = Branch.objects.get(id=branch_id)
        order = Order.objects.get(id=order_id)
        
        positions = Cart.objects.filter(order=order).order_by('id')
        form = CartForm()
        return render(request, 'trader_app/cart_form.html', {
            'title': f'Zamówienie dla {branch}', 
            'form': form,
            'positions': positions,
            'order': order,
            'visit_id': visit_id
        })
        
    def post(self, request,visit_id, branch_id, order_id):
        form = CartForm(request.POST)
        order = Order.objects.get(id=order_id)
        if form.is_valid():
            new_cart = Cart()
            new_cart.order = order
            new_cart.quantity = int(form.cleaned_data['quantity'])
            variant = form.cleaned_data.get('variant')
            batch = variant.batch_set.filter(is_active=True)[0]
            for element in variant.batch_set.filter(is_active=True):
                if element.quantity < batch.quantity and element.quantity > int(form.cleaned_data['quantity']):
                    batch  = element
            new_cart.batch = batch
            new_cart.save()
        
        branch = Branch.objects.get(id=branch_id)
        positions = Cart.objects.filter(order=order).order_by('id')
        return render(request, 'trader_app/cart_form.html', {
            'title': f'Zamówienie dla {branch}', 
            'form': form,
            'positions': positions,
            'order': order,
            'visit_id': visit_id
        })


class TraderCartDeleteView(LoginRequiredMixin, View):
    """
    View remove positiom from Cart
    """
    def post(self, request, order_id, position_id, visit_id):
        position = Cart.objects.get(id=position_id)
        branch_id = position.order.branch.id
        position.delete()
        
        return redirect(f'/trader/visit/{visit_id}/{branch_id}/orders/{order_id}/')


class TraderOrderStatusUpdateView(LoginRequiredMixin, View):
    """
    View change status to 'Zamówienie przyjęte, oczekuje na weryfikację.'
    """
    
    def post(self, request, branch_id, order_id, status_value, visit_id):
        order = Order.objects.get(id=order_id)
        order.order_status = status_value
        order.save()
        if status_value == 0:
            return redirect(f'/trader/visit/{visit_id}/{branch_id}/orders/{order_id}/')
        else:
            return redirect(f'/trader/visit/{visit_id}/')


class TraderEndVisitView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to mark viit as dome
    """
    permission_required = 'trader_app.change_visit' 
    
    def post(self, request, visit_id):
        visit = Visit.objects.get(id=visit_id)
        save_coordinates(request, f'Zakończenie wizyty {visit_id}')
        
        visit = Visit.objects.get(id=visit_id)
        visit.visited = True
        visit.save()
        return redirect('/trader/start_day/')


class TraderClientAdd(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to crate new client ang main adress
    """
    permission_required = ('manager_app.add_client', 'manager_app.add_branch')
    
    def get(self, request):
        form = ClientByNipForm(initial={
            'type': 0,
            'visit_hour_from': '8:00',
            'visit_hour_to': '16:00',
            'type': FAMILY_PHARM
        })
        return render(request, 'trader_app/client_form.html', {'form': form})
    
    def post(self, request):
        form = ClientByNipForm(request.POST)
        if form.is_valid():
            client = Client()
            client.nip = form.cleaned_data['nip']
            client.company_name = form.cleaned_data['company_name']
            client.short_company_name = form.cleaned_data['short_company_name']
            client.logo = form.cleaned_data['logo']
            client.regon = form.cleaned_data['regon']
            client.krs = form.cleaned_data['krs']
            client.type = form.cleaned_data['type']
            client.save()
            branch = Branch()
            branch.client = client
            branch.type = REGISTER_ADRESS
            branch.name_of_branch = form.cleaned_data['name_of_branch']
            branch.zip_code = form.cleaned_data['zip_code']
            branch.province = form.cleaned_data['province']
            branch.city = form.cleaned_data['city']
            branch.street = form.cleaned_data['street']
            branch.building_number = form.cleaned_data['building_number']
            branch.apartment_number = form.cleaned_data['apartment_number']
            branch.details = form.cleaned_data['details']
            branch.account_manager = request.user.employee
            branch.visit_days = form.cleaned_data['visit_days']
            branch.visit_hour_from = form.cleaned_data['visit_hour_from']
            branch.visit_hour_to = form.cleaned_data['visit_hour_to']
            branch.save()
            return redirect('/trader/')
        else:
            return render(request, 'trader_app/client_form.html', {'form': form})


class TraderClientList(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View lists all Traders clients
    """    
    permission_required = ('manager_app.add_client', 'manager_app.add_branch')
    
    def get(self, request):
        branches = Branch.objects.filter(account_manager = request.user.employee).order_by('name_of_branch')
        paginator = Paginator(branches, 10)
        page = request.GET.get('page')
        branches = paginator.get_page(page)
        return render(request, 'trader_app/clients.html', {'branches': branches})
