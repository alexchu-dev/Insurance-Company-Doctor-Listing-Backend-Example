from django.urls import path
from .views import doctor_post_get
from . import views

urlpatterns = [
    path("doctor/", doctor_post_get, name="doctor_post_get"),
    path("doctor/<int:doctor_id>/", doctor_post_get, name="doctor_post_get"),
    path("clinic/", views.create_clinic, name="create_clinic"),
    path("", views.main, name="main"),
]
