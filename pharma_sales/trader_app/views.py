from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_permission_codename, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormView, CreateView, ProcessFormView, UpdateView, DeleteView
from django.views import View
from datetime import date

from manager_app.models import Employee, User, Branch, Order, Cart, Batch, Variant, Product, Client
from manager_app.forms import LoginForm
from .models import Visit
from .forms import PlanDateForm, PlanAddVisitForm, MakeVisitForm


def save_coordinates(request):
    print(request.COOKIES['long'])
    print(request.COOKIES['lat'])
    # Localization.objects.create(
    #     latitude = float(request.COOKIES['lat']),
    #     longitude = float(request.COOKIES['lon']),
    #     Employee = request.user.Employee
    # )

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
    permission_required = 'trader_app.add_visit' ## to change
    
    def get(self, request):
        return render(request, 'trader_app/dashboard.html')
    
    
class TraderStartDayView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View starts day of work
    """
    permission_required = 'trader_app.add_visit' ## to change
    
    def get(self, request):
        visits = Visit.objects.filter(date=date.today(), trader=request.user.employee)
        resp = render (request, 'trader_app/start_day.html', {'visits': visits})
        
        return resp


class TraderPlaningDateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for choise date and city
    """
    permission_required = 'trader_app.add_visit' ## to change
    
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
    
    permission_required = 'trader_app.add_visit' ## to change
    
    def get(self, request, plan_date, city):
        visits = Visit.objects.filter(date=plan_date)
        form = PlanAddVisitForm()
        form.fields['branch'].queryset = Branch.objects.filter(account_manager=request.user.employee, city=city)
        if len(visits) < 12:
            message = f'Brakuje Ci {12 - len(visits)} wizyt do celu'
        else:
            message = f'Zaplanowałeś {len(visits)} spotkań.'
        
        print(Branch.objects.filter(account_manager=request.user.employee, city=city))
        
        
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
            visits = Visit.objects.filter(date=plan_date)
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
            visits = Visit.objects.filter(bity=city, date=plan_date)
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
    permission_required = 'trader_app.add_visit' ## to change
    
    def post(self, request, visit_id, visit_date, visit_city):
        Visit.objects.get(id=visit_id).delete()
        return redirect(f'/trader/planning/{visit_date}/{visit_city}/')


class TraderVisitView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    View for visits
    """
    permission_required = 'trader_app.add_visit' ## to change
    
    def get(self, request, visit_id):
        #Lokaliztion
        save_coordinates(request)
        visit = Visit.objects.get(id=visit_id)
        if visit.note or visit.proof_img:
            form = MakeVisitForm(initial={
                'proof_img':visit.proof_img,
                'note': visit.note
            })
        else:
            form = MakeVisitForm()
        return render(request, 'trader_app/visit.html', {'form': form})
    
    def post(self, request, visit_id):
        form = MakeVisitForm (request.POST)
        if form.is_valid():
            visit = Visit.objects.get(id=visit_id)
            visit.proof_img = form.cleaned_data['proof_img']
            visit.note = form.cleaned_data['note']
            visit.save()
            return render(request, 'trader_app/visit.html', {'form': form})
        else: return render(request, 'trader_app/visit.html', {'form': form})



