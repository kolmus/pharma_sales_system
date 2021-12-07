from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View

from .forms import LoginForm, EmployeeAddForm
from .models import Employee
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


class EmployeeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """class fer Emlpoyers list Viev

    Args:
        none

    Returns:
        team [QuerySet]: Objects of Employee model with 'supervisor' set on current user
    """
    permission_required = 'manager_app.employee_list'
    
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        team = Employee.objects.filter(supervisor=user)
        return render(request, 'manager_app/emloyees.html', {'team': team})


class EmployeAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'manager_app.employee_add'
    
    def get(self, request):
        form = EmployeeAddForm()
        return render(request, 'manager_app/employee_add.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})
    
    def post(self, request):
        form = EmployeeAddForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=True,
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
            return render(request, 'manager_app/employee_add.html', {'form': form, 'legend': 'Dodaj nowego pracownika'})



