from django.contrib import admin
from .models import (Slider, Service, Item, Doctor, Expertize, Faq, Gallery)

admin.site.register(Slider)
admin.site.register(Item)
admin.site.register(Doctor)
admin.site.register(Expertize)
admin.site.register(Faq)
admin.site.register(Gallery)


class ServiceAdmin(admin.ModelAdmin):
    model = Service

    list_filter = ("created_date",)
    order = ["-created_date"]


admin.site.register(Service, ServiceAdmin)