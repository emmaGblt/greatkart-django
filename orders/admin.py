from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderInline(admin.TabularInline):
    model = Order
    show_change_link = True
    can_delete = False
    fields = ["user", "total", "status"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["transaction_id", "status", "amount", "method", "created_at"]

    inlines = [OrderInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["reference", "created_at", "updated_at", "payment"]
    fieldsets = [
        (None, {"fields": ["reference", "user", "payment", "status"]}),
        (
            "Shipping info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "phone_number",
                    "email",
                    "address_line_1",
                    "address_line_2",
                    "city",
                    "state",
                    "country",
                    "note",
                ]
            },
        ),
        ("Billing info", {"fields": ["total", "tax"]}),
        ("Other", {"fields": ["ip", "created_at", "updated_at"]}),
    ]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass
