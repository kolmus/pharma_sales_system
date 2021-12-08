from typing import ValuesView
from django.db.models import fields
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy

from .forms import ClientForm, LoginForm, EmployeeAddForm, EmployeeEditForm
from .models import Client, Employee, Branch
from django.contrib.auth.models import User

class LoginView(View):
    """View created for login page

    Args:
        LoginForm (class): Form with login and password
    """
    def get(self, request):
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


class DashbaordView(LoginRequiredMixin, View):
    """
    Dashbord View - general informations and statistics.
    Login required.
    """
    def get(self, request):
        return render(request, 'manager_app/dashboard.html')


class EmployeeView(LoginRequiredMixin, View):
    """class fer Emlpoyers list Viev

    Args:
        none

    Returns:
        team [QuerySet]: Objects of Employee model with 'supervisor' set on current user
    """
    
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_employee = user.employee
        team = Employee.objects.filter(supervisor=user_employee)
        return render(request, 'manager_app/employees.html', {'team': team})


class EmployeeCreateView(LoginRequiredMixin, View):
    """View fo creating new users.
    Creates new user and new Emploee
        
    Returns: 
        
    """
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
            return redirect(f'/employee/{new_employee.id}/')
        else:
            return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})


class EmployeeDetailsView(LoginRequiredMixin, View):
    """ 
    Details Viev for Employee model  objects

    Args:
        
        id_ (int): id of object in Emploee model
    Returns:
        employee [object]: Emloyee object
    """
    def get(self, request, id_):
        employee = Employee.objects.get(id=id_)
        return render(request, 'manager_app/employee_details.html', {'employee': employee})

class EmployeeEditView(LoginRequiredMixin, View):
    """
    View for modify Empployee models

    Args:
        id_ (int): id of emloyee object
    
    Returns:
        form : with curent values
        legend (str): legend for form
    """
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
        form = EmployeeAddForm(request.POST)
        if form.is_valid():
            edited_user = Employee.objects.get(id=id_).user
            User.objects.update(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            edited_employee = Employee.objects.create(
                phone=form.cleaned_data['phone'],
                role=form.cleaned_data['role'],
                supervisor=form.cleaned_data['supervisor'],
                user=edited_user
            )
            return redirect(f'/employee/{edited_employee.id}/')
        else:
            return render(request, 'manager_app/employee_form.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})
        

class ClientCreateView(LoginRequiredMixin, View):
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
            return redirect(f'/clients/{new_client.id}/add-branch/')
        else:
            return render(
            request, 
            'manager_app/client_form.html', 
            {
                'form': form, 
                'legend': 'Tworzenie nowego klienta', 
                'answer': 'Wystąpił błąc. Spróbuj ponownie'
            }
        )


class ClientDetailsView(LoginRequiredMixin, View):
    def get(self, request, id_):
        client = Client.objects.get(id=id_)
        return render(request, 'manager_app/client_details.html', {'client': client})


class ClientListView(LoginRequiredMixin, View):
    def get(self, request):
        traders = Employee.objects.filter(supervisor=request.user.employee)
        clients = {}
        for trader in traders:
            branches = Branch.objects.filter(account_manager=trader)
            clients[trader.name] = branches
        print(clients)
        return render(request, 'manager_app/clients.html', {'clients': clients})
    
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'
    success_url = f'/clients/'
    
    
class BranchCreateView(LoginRequiredMixin, CreateView):
    model = Branch
    fields = '__all__'
    success_url = '/branch/'


