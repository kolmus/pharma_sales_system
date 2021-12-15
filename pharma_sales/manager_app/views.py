
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from datetime import date, timedelta

from .forms import ClientForm, LoginForm, EmployeeAddForm, EmployeeEditForm, VariantForm, CartForm, CalendarForm
from .models import CREATING_ST, ORDER_STATUS, Batch, CalendarSupervisor, Client, Employee, Branch, Product, Variant, Order, Cart, CLIENT_TYPE, WEEKDAY
from django.contrib.auth.models import User


class LoginView(View):
    """View created for login page

    Args:
        LoginForm (class): Form with login and password
    """
    def get(self, request):
        # print(request.GET['next'])
        form = LoginForm()
        return render(request, 'manager_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['login'], 
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'manager_app/login.html', {'form': form, 'answer': 'Błędny login lub hasło'})
        else: 
            return render(request, 'manager_app/login.html', {'form': form})


class LogoutView(View):
    """
    View created fo logout
    """
    def get(self, request):
        logout(request)
        return redirect("/login/")


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Dashbord View - supervisors clendar.
    Login required.
    """
    permission_required = 'auth.add_user'
    
    def get(self, request):
        
        today = date.today()
        days_in_calendar = 5
        
        year, month, day = (int(x) for x in str(today).split('-'))
        weekday = today.weekday()
        
        last_monday = today - timedelta(days = weekday )
        team = Employee.objects.filter(supervisor = request.user.employee, is_active = True)
        
        
        last_week_monday = last_monday - timedelta(days = 7)
        
        last_week = {}
        for i in range(days_in_calendar):
            correct_date = last_week_monday + timedelta(days = i)
            year, month, day = (int(x) for x in str(correct_date).split('-'))
            final_date = f'{year}-{month}-{day} {WEEKDAY[correct_date.weekday()][1]}'
            
            if CalendarSupervisor.objects.filter(owner=request.user.employee, meeting_date=correct_date).exists():
                meeting = CalendarSupervisor.objects.get(owner=request.user.employee, meeting_date=correct_date)
                form = CalendarForm(initial={
                    'note': meeting.note,
                    'employee': meeting.employee 
                })
            else:
                form = CalendarForm()
            form.fields['employee'].queryset = team
            last_week[final_date] = form
        
        
        this_week = {}
        for i in range(days_in_calendar):
            correct_date = last_monday + timedelta(days = i)
            year, month, day = (int(x) for x in str(correct_date).split('-'))
            final_date = f'{year}-{month}-{day} {WEEKDAY[correct_date.weekday()][1]}'
            
            if CalendarSupervisor.objects.filter(owner=request.user.employee, meeting_date=correct_date).exists():
                meeting = CalendarSupervisor.objects.get(owner=request.user.employee, meeting_date=correct_date)
                form = CalendarForm(initial={
                    'note': meeting.note,
                    'employee': meeting.employee 
                })
            else:
                form = CalendarForm()
            form.fields['employee'].queryset = team
            this_week[final_date] = form
        
        
        next_monday = last_monday + timedelta( days=7)
        next_week = {}
        for i in range(days_in_calendar):
            correct_date = next_monday + timedelta(days = i)
            year, month, day = (int(x) for x in str(correct_date).split('-'))
            final_date = f'{year}-{month}-{day} {WEEKDAY[correct_date.weekday()][1]}'
            
            if CalendarSupervisor.objects.filter(owner=request.user.employee, meeting_date=correct_date).exists():
                meeting = CalendarSupervisor.objects.get(owner=request.user.employee, meeting_date=correct_date)
                form = CalendarForm(initial={
                    'note': meeting.note,
                    'employee': meeting.employee 
                })
                form.fields['employee'].queryset = team
            else:
                form = CalendarForm()
            form.fields['employee'].queryset = team
            next_week[final_date] = form
        return render(request, 'manager_app/dashboard.html', {
            'last_week': last_week,
            'this_week': this_week,
            'next_week': next_week
        })
        
    def post(self, request):
        team = Employee.objects.filter(supervisor = request.user.employee, is_active = True)
        form = CalendarForm(request.POST)
        form.fields['employee'].queryset = team
        date_post = request.POST['date_cal']
        date_correct = date_post.split(' ')[0]
        if form.is_valid():
            if CalendarSupervisor.objects.filter(meeting_date = date_correct, owner = request.user.employee).exists():
                meeting = CalendarSupervisor.objects.filter(meeting_date = date_correct, owner = request.user.employee)[0]
                meeting.employee = form.cleaned_data['employee']
                meeting.note = form.cleaned_data['note']
                meeting.save()
            else: 
                meeting = CalendarSupervisor()
                meeting.owner = request.user.employee
                meeting.meeting_date = date_correct
                meeting.employee = form.cleaned_data['employee']
                meeting.note = form.cleaned_data['note']
                meeting.save()
        return redirect('/')
        

class EmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class for Emlpoyers list View
    """
    permission_required = 'manager_app.view_employee',
    
    def get(self, request):
        team = Employee.objects.filter(supervisor=request.user.employee)
        
        today = date.today()
        year, month, day = (int(x) for x in str(today).split('-'))
        
        info = []
        for employee in team:
            traders_info = {}
            traders_info['employee'] = employee
            
            branches = Branch.objects.filter(account_manager = employee)
            
            last_month_total = 0
            for order in Order.objects.filter(
                branch__in=branches, 
                date__gte=f'{year}-{month-1}-01', 
                date__lt=f'{year}-{month}-01'
            ):
                for position in order.cart_set.all():
                    last_month_total += (int(position.quantity) * float(position.batch.netto))
            
            traders_info['last_month'] = round(last_month_total, 2)
            
            this_month_total = 0
            for order in Order.objects.filter(branch__in=branches, date__gte=f'{year}-{month}-01'):
                for position in order.cart_set.all():
                    this_month_total += (int(position.quantity) * float(position.batch.netto))
            traders_info['this_month'] = round(this_month_total, 2)
            
            traders_info['visit_done'] = len(employee.visit_set.filter(date=today, visited=True))
            traders_info['visit_todo'] = len(employee.visit_set.filter(date=today, visited=False))
            traders_info['orders_today'] = len(Order.objects.filter(branch__in=branches, date=today))
            
            today_total = 0
            for order in Order.objects.filter(branch__in=branches, date=today):
                for position in order.cart_set.all():
                    today_total += (int(position.quantity) * float(position.batch.netto))
            traders_info['today_total'] = round(today_total, 2)
            
            info.append(traders_info)
        
        return render(request, 'manager_app/employees.html', {'info': info})


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """View fo creating new users.
    Creates new user and new Emploee
        
    """
    permission_required = 'auth.add_user'
    
    def get(self, request):
        form = EmployeeAddForm()
        return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})
    
    def post(self, request):
        form = EmployeeAddForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=False,
                is_active=True,
            )
            new_employee = Employee.objects.create(
                phone=form.cleaned_data['phone'],
                role=form.cleaned_data['role'],
                supervisor=form.cleaned_data['supervisor'],
                user=new_user
            )
            
            
            return redirect(f'/employees/{new_employee.id}/')
        else:
            return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})


class EmployeeDetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """ 
    Details View for Employee model  objects

    Args:
        
        id_ (int): id of object in Emploee model
    Returns:
        employee [object]: Emloyee object
    """
    permission_required = 'manager_app.view_employee',
    
    def get(self, request, id_):
        today = date.today()
        year, month, day = (int(x) for x in str(today).split('-'))
        
        employee = Employee.objects.get(id=id_)
        
        branches = Branch.objects.filter(account_manager=employee)
        last_month_total = 0
        for order in Order.objects.filter(
            branch__in=branches, 
            date__gte=f'{year}-{month-1}-01', 
            date__lt=f'{year}-{month}-01'
        ):
            for position in order.cart_set.all():
                last_month_total += (int(position.quantity) * float(position.batch.netto))
            
        this_month_total = 0
        for order in Order.objects.filter(branch__in=branches, date__gte=f'{year}-{month}-01'):
            for position in order.cart_set.all():
                this_month_total += (int(position.quantity) * float(position.batch.netto))
        
        orders_last_month = 0
        for branch in branches:
            for order in branch.order_set.filter(date__gte=f'{year}-{month-1}-01'):
                orders_last_month += 1
        
        this_month_orders = 0
        for branch in branches:
            for order in branch.order_set.filter(date__gte=f'{year}-{month}-01'):
                this_month_orders += 1
        
        orders_today = 0
        orders_today_total = 0
        for branch in branches:
            for order in branch.order_set.filter(date=today):
                orders_today += 1
                for position in order.cart_set.all():
                    orders_today_total += (int(position.quantity) * float(position.batch.netto))
        
        return render(request, 'manager_app/employee_details.html', {
            'employee': employee,
            'last_month_total': round(last_month_total, 2),
            'this_month_total': round(this_month_total, 2),
            'last_month_orders': orders_last_month,
            'this_month_orders': this_month_orders,
            'visit_today_done': len(employee.visit_set.filter(date=today, visited=True)),
            'visit_today': len(employee.visit_set.filter(date=today)),
            'orders_today': orders_today,
            'orders_today_total': orders_today_total
        })


class EmployeeEditView(LoginRequiredMixin, View):
    """
    View for modify Empployee models

    Args:
        id_ (int): id of emloyee object
    
    Returns:
        form : with curent values
        legend (str): legend for form
    """
    permission_required = 'manager_app.change_employee',
    
    def get(self, request, id_):
        employee = Employee.objects.get(id=id_)
        form = EmployeeEditForm(initial={
            'first_name': employee.user.first_name,
            'last_name': employee.user.last_name,
            'email': employee.user.email,
            'phone': employee.phone,
            'role': employee.role,
            'supervisor': employee.supervisor
        })
        
        return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Edycja Pracownika'})
    
    def post(self, request, id_):
        form = EmployeeEditForm(request.POST)
        if form.is_valid():
            edited_user = Employee.objects.get(id=id_).user
            edited_user.email = form.cleaned_data['email']
            edited_user.first_name = form.cleaned_data['first_name']
            edited_user.last_name = form.cleaned_data['last_name']

            edited_user.save()
            
            edited_employee = edited_user.employee

            edited_employee.phone = form.cleaned_data['phone']

            edited_employee.role = form.cleaned_data['role']


            edited_employee.supervisor = form.cleaned_data['supervisor']
            edited_employee.save()
            
            

            
            return redirect(f'/employees/{edited_employee.id}/')
        else:
            return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})
        

class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for create Client
    redirect to Create Branch
    """
    permission_required = 'manager_app.add_client',
    
    def get(self, request):
        form = ClientForm()
        return render(
            request, 
            'manager_app/client_form.html', 
            {'form': form, 'legend': 'Tworzenie nowego klienta'}
        )
        
    def post(self, request):
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            new_client = Client()
            new_client.company_name = form.cleaned_data['company_name']
            new_client.nip = form.cleaned_data['nip']
            new_client.logo = form.cleaned_data['logo']
            new_client.regon = form.cleaned_data['regon']
            new_client.krs = form.cleaned_data['krs']
            new_client.type = form.cleaned_data['type']
            new_client.save()
            return redirect(f'/branch/add/')
        else:
            return render(
            request, 
            'manager_app/client_form.html', 
            {
                'form': form, 
                'legend': 'Tworzenie nowego klienta', 
                'answer': 'Wystąpił błąd. Spróbuj ponownie'
            }
        )


class ClientDetailsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for details of client and branch
    """
    permission_required = 'manager_app.view_client',
    
    def get(self, request, id_):
        client = Client.objects.get(id=id_)
        return render(request, 'manager_app/client_details.html', {'client': client})


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """View to show clients group by employers"""
    permission_required = ('manager_app.view_employee', 'manager_app.view_client')
    
    def get(self, request):
        traders = Employee.objects.filter(supervisor=request.user.employee)
        return render(request, 'manager_app/clients.html', {'traders': traders})
    
    
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for update Client
    """
    permission_required = 'manager_app.change_client',
    model = Client
    fields = '__all__'
    success_url = f'/clients/'
    
    
class BranchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View for create Branch
    """
    permission_required = 'manager_app.add_branch',
    model = Branch
    fields = '__all__'
    success_url = '/clients/'


class BranchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View  for update Branch
    """
    permission_required = 'manager_app.change_branch',
    model = Branch
    fields = '__all__'
    success_url = '/clients/'
    
    
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View for create Product
    """
    permission_required = 'manager_app.add_product'
    model = Product
    fields = '__all__'
    success_url = '/variant/add/'


class ProductUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    """
    View  for update Branch
    """
    permission_required = 'manager_app.change_product'
    model = Product
    fields = '__all__'
    succes_url = '/products/'

class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for list of Products and Variants
    """
    permission_required = 'manager_app.view_product'
    
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        list = {}
        for product in products:
            list[product.name] = Variant.objects.filter(product_id=product, is_active=True)
        return render(request, 'manager_app/products.html', {'products': list})


class VariantCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for add new variants to product
    """
    permission_required = 'manager_app.add_variant'
    
    def get(self, request):
        form = VariantForm()
        return render(request, 'manager_app/variant_form.html', {'form': form, 'legend': 'Dodaj nowy wariant produktu'})
    
    def post(self, request):
        form = VariantForm(request.POST, request.FILES)
        if form.is_valid():
            variant = Variant()
            variant.dose = form.cleaned_data['dose']
            variant.unit = form.cleaned_data['unit']
            variant.in_package = form.cleaned_data['in_package']
            variant.photo_main = form.cleaned_data['photo_main']
            variant.photo_2 = form.cleaned_data['photo2']
            variant.photo_3 = form.cleaned_data['photo3']
            variant.photo_4 = form.cleaned_data['photo4']
            variant.photo_5 = form.cleaned_data['photo5']
            variant.photo_6 = form.cleaned_data['photo6']
            variant.photo_7 = form.cleaned_data['photo7']
            variant.photo_8 = form.cleaned_data['photo8']
            variant.photo_9 = form.cleaned_data['photo9']
            variant.photo_10 = form.cleaned_data['photo10']
            variant.product = form.cleaned_data['product']
            variant.next_delivery = form.cleaned_data['next_delivery']
            variant.save()
            return redirect('/products/')
        else:
            return render(request, 'manager_app/variant_form.html', {'form': form, 'legend': 'Dodaj nowy wariant produktu'})


class VariantUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for update variants
    """
    permission_required = 'manager_app.change_variant'
    
    def get(self, request, id_):
        variant = Variant.objects.get(id=id_)
        form = VariantForm(initial={
            'product': variant.product_id,
            'dose': variant.dose,
            'unit': variant.unit,
            'in_package': variant.in_package,
            'next_delivery': variant.next_delivery,
            'photo_main': variant.photo_main,
            'photo2': variant.photo_2,
            'photo3': variant.photo_3,
            'photo4': variant.photo_4,
            'photo5': variant.photo_5,
            'photo6': variant.photo_6,
            'photo7': variant.photo_7,
            'photo8': variant.photo_8,
            'photo9': variant.photo_9,
            'photo10': variant.photo_10
        })
        return render(request, 'manager_app/variant_form.html', {'form': form, 'legend': 'Edytuj wariant produktu'})
    
    def post(self, request, id_):
        form = VariantForm(request.POST, request.FILES)
        if form.is_valid():
            variant = Variant.objects.get(id=id_)
            variant.dose = form.cleaned_data['dose']
            variant.unit = form.cleaned_data['unit']
            variant.in_package = form.cleaned_data['in_package']
            variant.photo_main = form.cleaned_data['photo_main']
            variant.photo_2 = form.cleaned_data['photo2']
            variant.photo_3 = form.cleaned_data['photo3']
            variant.photo_4 = form.cleaned_data['photo4']
            variant.photo_5 = form.cleaned_data['photo5']
            variant.photo_6 = form.cleaned_data['photo6']
            variant.photo_7 = form.cleaned_data['photo7']
            variant.photo_8 = form.cleaned_data['photo8']
            variant.photo_9 = form.cleaned_data['photo9']
            variant.photo_10 = form.cleaned_data['photo10']
            variant.product_id = form.cleaned_data['product']
            variant.next_delivery = form.cleaned_data['next_delivery']
            variant.save()
            print(variant.photo_main)
            return redirect('/products/')
        else:
            return render(request, 'manager_app/variant_form.html', {'form': form, 'legend': 'Dodaj nowy wariant produktu'})
        

class BatchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View for create Batch
    """
    permission_required = 'manager_app.add_batch'
    
    model = Batch
    fields = '__all__'
    success_url = '/products/'


class OrderCartCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for new Order and Cart
    """
    permission_required = 'manager_app.add_order'
    
    def get(self, request, branch_id):
        branch = Branch.objects.get(id=branch_id)
        form = CartForm()
        return render(request, 'manager_app/cart_form.html', {'title': f'Nowe zamówienie dla {branch}', 'form': form})

    def post(self, request, branch_id):
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
            
            return redirect(f'/branch/{branch.id}/orders/{order.id}/')
        else:
            return render(request, 'manager_app/cart_form.html', {'title': f'Nowe zamówienie dla {branch}', 'form': form})


class CartModifyView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for adding posiotions to Cart
    """
    permission_required = 'manager_app.add_cart'
    
    def get(self, request, branch_id, order_id):
        branch = Branch.objects.get(id=branch_id)
        order = Order.objects.get(id=order_id)
        
        positions = Cart.objects.filter(order=order).order_by('id')
        form = CartForm()
        return render(request, 'manager_app/cart_form.html', {
            'title': f'Zamówienie dla {branch}', 
            'form': form,
            'positions': positions,
            'order': order
        })
        
    def post(self, request, branch_id, order_id):
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
        return render(request, 'manager_app/cart_form.html', {
            'title': f'Zamówienie dla {branch}', 
            'form': form,
            'positions': positions,
            'order': order
        })
        
        
class CartDeleteView(LoginRequiredMixin, View):
    """
    View remove positiom from Cart
    """
    permission_required = 'manager_app.add_cart'
    
    def post(self, request, order_id, position_id):
        position = Cart.objects.get(id=position_id)
        branch_id = position.order.branch.id
        position.delete()
        
        return redirect(f'/branch/{branch_id}/orders/{order_id}/')


class OrderStatusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View to update order status
    """
    permission_required = 'manager_app.change_order'
    
    def post(self, request, order_id, status_value):
        order = Order.objects.get(id=order_id)
        order.order_status = status_value
        order.save()
        return redirect('/orders/')


class OrderDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for delete Order
    """
    permission_required = 'manager_app.change_order'
    
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.delete()
        
        return redirect(f'/orders/')


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin,View):
    """
    Lists of all Orders without ended
    """
    permission_required = 'manager_app.view_order'
    
    def get(self, request):
        orders = Order.objects.filter(order_status__in=[0, 1, 2, 3, 4, 5, 6]).order_by('order_status', '-date')
        
        result = {}
        for status in ORDER_STATUS:
            st_orders = orders.filter(order_status = status[0])
            result[status[1]] = st_orders
        return render(request, 'manager_app/orders.html', {'orders': result})
    
    
class OrderCSModifyView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):   # need changes
    """
    View for Customer Service to manage order manualy
    """
    permission_required = 'manager_app.change_order'
    
    model = Order
    fields = ['order_number', 'branch', 'invoice', 'discount']
    success_url = '/orders/'


