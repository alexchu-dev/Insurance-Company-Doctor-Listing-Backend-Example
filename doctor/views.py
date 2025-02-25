from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import (
    csrf_exempt,
)  # Cross Site Request Forgery exemption for dev
from django.shortcuts import get_object_or_404
import json
from .models import Doctor, Clinic, District, Category
from django.template import loader


@csrf_exempt
def get_doctor(request, doctor_id=None):
    if request.method == "GET":
        # List single doctor with all clinics registered
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)
            category = Category.objects.filter(id=doctor.category.id).first()
            clinics = Clinic.objects.filter(clinicdoctor__doctor=doctor)
            clinic_list = []
            for clinic in clinics:
                district = District.objects.filter(clinic=clinic).first()
                clinic_list.append(
                    {
                        "clinic_name": clinic.name,
                        "district": district.name if district else None,
                        "address": clinic.address,
                        "phone_no1": clinic.phone_no1,
                        "phone_no2": clinic.phone_no2,
                        "consultation_fee": clinic.consultation_fee,
                        "prescription": clinic.prescription,
                        "working_hours": clinic.working_hours,
                    }
                )
            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "id": doctor.id,
                        "first_name": doctor.first_name,
                        "last_name": doctor.last_name,
                        "category": doctor.category.name,
                        "clinic": clinic_list,
                    },
                }
            )
        # List all doctors or by filter if no doctor_id is provided
        else:
            doctors = Doctor.objects.all()
            district = request.GET.get("district")
            category = request.GET.get("category")
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            language = request.GET.get("language")
            # District in query
            if district:
                doctors = doctors.filter(clinics__district__name=district)
            # Category in query
            if category:
                doctors = doctors.filter(category__name=category)
            # Language in query
            if language:
                doctors = doctors.filter(language=language)
            # Price range in query
            if min_price and max_price:
                doctors = doctors.filter(
                    clinicdoctor__clinic__consultation_fee__gte=min_price,
                    clinicdoctor__clinic__consultation_fee__lte=max_price,
                )
            elif min_price:
                doctors = doctors.filter(
                    clinicdoctor__clinic__consultation_fee__gte=min_price
                )
            elif max_price:
                doctors = doctors.filter(
                    clinicdoctor__clinic__consultation_fee__lte=max_price
                )

            doctor_list = list(
                doctors.values("id", "first_name", "last_name", "category_id")
            )
            return JsonResponse({"success": True, "data": doctor_list}, safe=False)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


# Create a Doctor
@csrf_exempt
def create_doctor(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            category_name = data.get('category')

            if not first_name or not last_name:
                return JsonResponse({"success": False, "message": "First name and last name are required"}, status=400)
            
            category = Category.objects.filter(name=category_name).first()
            if not category:
                return JsonResponse({"success": False, "message": "Category not found"}, status=404)

            doctor = Doctor.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                category=category,
            )
            return JsonResponse(
                {
                    "id": doctor.id,
                    "first_name": doctor.first_name,
                    "last_name": doctor.last_name,
                    "category": doctor.category.name,
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}))