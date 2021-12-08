"""pharma_sales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from manager_app.views import (
    LoginView,
    LogoutView,
    DashbaordView,
    EmployeeView,
    EmployeAddView,
    EmployeeDetailsView,
    EmployeeEditView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', DashbaordView.as_view()),
    path('employees/', EmployeeView.as_view()),
    path('employees/add/', EmployeAddView.as_view()),
    path('employees/<int:id_>/', EmployeeDetailsView.as_view()),
    path('employees/edit/<int:id_>/', EmployeeEditView.as_view()),
]
