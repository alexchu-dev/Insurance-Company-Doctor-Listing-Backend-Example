from django.urls import path
from .views import create_doctor, get_doctor

urlpatterns = [
    path("doctor/", get_doctor, name="get_doctor"),
    path("doctor/<int:doctor_id>/", get_doctor, name="get_doctor"),
    path("create_doctor/", create_doctor, name="create_doctor"),
]
