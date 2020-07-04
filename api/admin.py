from django.contrib import admin
from .models import Country, Produced, Pending, Rejected

# Register your models here.
admin.site.register(Country)
admin.site.register(Produced)
admin.site.register(Pending)
admin.site.register(Rejected)

