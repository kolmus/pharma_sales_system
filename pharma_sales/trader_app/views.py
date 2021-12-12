from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View
from datetime import date

from manager_app.models import Employee, User, Branch, Order, Cart, Batch, Variant, Product, Client
from manager_app.forms import LoginForm
from .models import Visit



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
    permission_required = 'auth.add_user' ## to change
    
    def get(self, request):
        return render(request, 'trader_app/dashboard.html')
    
class TraderStartDayView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View starts day of work
    """
    permission_required = 'auth.add_user' ## to change
    
    def get(self, request):
        visits = Visit.objects.filter(date=date.today())
        print(visits)
        resp = render (request, 'trader_app/today.html')
        return resp

class TraderPlaningView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View helps to plan all day = needs 12 position to access save
    """
    permission_required = 'auth.add_user' ## to change
    
    def get(self, request):
        clients = Branch.objects.filter(account_manager=request.user.employee)
        return render(request, 'trader_app/planning.html', {'clients': clients})
    
    def post(self, request):
        clients = Branch.objects.filter(account_manager=request.user.employee)
        return render(request, 'trader_app/planning.html', {'clients': clients})

