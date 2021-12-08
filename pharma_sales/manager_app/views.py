from typing import ValuesView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View

from .forms import LoginForm, EmployeeAddForm, EmployeeEditForm
from .models import Employee, Branch
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


class EmployeAddView(LoginRequiredMixin, View):
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
    def get(self, request, id_):
        employee = Employee.objects.get(id=id_)
        return render(request, 'manager_app/employee_details.html', {'employee': employee})

class EmployeeEditView(LoginRequiredMixin, View):
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