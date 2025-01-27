from django.contrib import admin

from bond_service.core.models import Bond


# There is a simple admin configuration for the Bond model
@admin.register(Bond)
class BondAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "isin",
        "owner",
        "value",
        "interest_rate",
        "purchase_date",
        "maturity_date",
    )
    search_fields = ("name", "isin", "owner__username")
    list_filter = ("owner",)
    raw_id_fields = ("owner",)
