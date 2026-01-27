from django.contrib import admin
from .models import Payment, Order, OrderProduct


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["reference", "created_at", "updated_at"]
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
