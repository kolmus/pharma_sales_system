from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views import View

from manager_app.models import Employee, User, Branch, Order, Cart, Batch, Variant, Product, Client
from manager_app.forms import LoginForm



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
    
    
class TraderDashboardView(LoginRequiredMixin, View):
    """
    View for dashboard page
    """
    def get(self, request):
        return render(request, 'trader_app/dashboard.html')
    