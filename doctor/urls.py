from django.urls import path
from .views import doctor_post_get, create_clinic, assign_doctor
from . import views

urlpatterns = [
    path("doctor/", doctor_post_get, name="doctor_post_get"),
    path("doctor/<int:doctor_id>/", doctor_post_get, name="doctor_post_get"),
    path("clinic/", views.create_clinic, name="create_clinic"),
    path("assign_doctor/", views.assign_doctor, name="assign_doctor"),
    path("", views.main, name="main"),
]
