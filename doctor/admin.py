from django.contrib import admin
from .models import Doctor, Clinic, ClinicDoctor, Category, District, Translation
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(ClinicDoctor)
admin.site.register(Category)
admin.site.register(District)
admin.site.register(Translation)