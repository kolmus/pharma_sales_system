from django.contrib import admin
from .models import Employee, Client, Branch, Product, Variant, Batch, Invoice, Order, CalendarSupervisor, Cart
from trader_app.models import Visit, Localization

def not_active(model_admin, request, query_set):
    query_set.update(is_active=False)
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role', 'supervisor')
    actions = [not_active]
    
    
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'logo', 'nip', 'regon', 'krs', 'type')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        'city',
        'street',
        'building_number',
        'apartment_number',
        'zip_code',
        'type',
        'client',
        'details',
        'name_of_branch',
        'account_manager',
        'visit_days',
        'visit_hour_from',
        'visit_hour_to'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active_substance')


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = (
        'dose',
        'in_package',
        'photo_main',
        'photo_2',
        'photo_3',
        'photo_4',
        'photo_5',
        'photo_6',
        'photo_7',
        'photo_8',
        'photo_9',
        'photo_10',
        'product_id',
        'next_delivery'
    )


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('number', 'ean', 'expiration_date', 'netto', 'vat', 'quantity', 'variant')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'status', 'payment_date')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'branch',
        # 'variant',
        'invoice',
        'discount',
        'order_status'
    )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('date', 'visited', 'proof_img', 'trader', 'client_branch', 'note')


@admin.register(CalendarSupervisor)
class CalendarSupervisorAdmin(admin.ModelAdmin):
    list_display = ('owner', 'meeting_date', 'employee', 'note')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('order', 'batch', 'quantity')
    
    
@admin.register(Localization)
class LocalizationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time', 'latitude', 'longitude', 'note')

