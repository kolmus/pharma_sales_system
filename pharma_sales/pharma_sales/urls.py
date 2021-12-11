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
from django.conf import settings
from django.conf.urls.static import static

from manager_app.views import (
    BatchCreateView,
    BranchUpdateView,
    LoginView,
    LogoutView,
    DashboardView,
    EmployeeView,
    EmployeeCreateView,
    EmployeeDetailsView,
    EmployeeEditView,
    ClientCreateView,
    ClientListView,
    ClientDetailsView,
    ClientUpdateView,
    BranchCreateView,
    ProductCreateView,
    ProductUpdateView,
    ProductListView,
    VariantCreateView,
    VariantUpdateView,
    OrderCartCreateView,
    CartModifyView,
    CartDeleteView,
    OrderStatusUpdateView,
    OrderListView,
    OrderCSModifyView,
    OrderDeleteView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', DashboardView.as_view()),
    path('employees/', EmployeeView.as_view()),
    path('employees/add/', EmployeeCreateView.as_view()),
    path('employees/<int:id_>/', EmployeeDetailsView.as_view()),
    path('employees/edit/<int:id_>/', EmployeeEditView.as_view()),
    path('clients/', ClientListView.as_view()),
    path('clients/add/', ClientCreateView.as_view()),
    path('clients/<int:id_>/', ClientDetailsView.as_view()),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view()),
    path('branch/add/', BranchCreateView.as_view()),
    path('branch/edit/<int:pk>/', BranchUpdateView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/add/', ProductCreateView.as_view()),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view()),
    path('variant/add/', VariantCreateView.as_view()),
    path('variant/edit/<int:id_>/', VariantUpdateView.as_view()),
    path('batch/add/', BatchCreateView.as_view()),
    path('branch/<int:branch_id>/orders/add/', OrderCartCreateView.as_view()),
    path('branch/<int:branch_id>/orders/<int:order_id>/', CartModifyView.as_view()),
    path('orders/<int:order_id>/delete/<int:position_id>/', CartDeleteView.as_view()),
    path('branch/<int:branch_id>/orders/<int:order_id>/status/<int:status_value>/', OrderStatusUpdateView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('orders/<int:pk>/cs/', OrderCSModifyView.as_view()),
    path('orders/<int:order_id>/delete/', OrderDeleteView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
