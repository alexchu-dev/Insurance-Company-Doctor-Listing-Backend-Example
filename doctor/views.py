from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import (
    csrf_exempt,
)  # Cross Site Request Forgery exemption for dev
from django.shortcuts import get_object_or_404
import json
from .models import Doctor, Clinic, District, Category, Language
from django.template import loader


@csrf_exempt
def doctor_post_get(request, doctor_id=None):
    """
    Single endpoint for CRUD operations on doctors/doctor
    """
    if request.method == "GET":
        """READ doctors/doctor by filters and doctor by id

        Param:
            doctor_id (int): default None for all doctors.
        Query:
            district (str): district name
            category (str): category name
            min_price (int): minimum price
            max_price (int): maximum price
            language (str): language short code

        Returns:
            JSON: Doctor dto in JsonResponse
        """
        if doctor_id:
            # List single doctor with all clinics registered
            try:
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
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=404)
        
        else:
            # List all doctors or by filter if no doctor_id is provided
            try:
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
                    if min_price > max_price:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": "min_price should be less than max_price",
                            },
                            status=400,
                        )
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
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=404)

    elif request.method == "POST":
        """CREATE doctors/doctor
        Body:
            first_name (str): first name
            last_name (str): last name
            category (str): category name
            language (str): language short code

        Returns:
            JSON: Doctor dto in JsonResponse
        """
        if not request.body:
            return JsonResponse(
                {"success": False, "message": "Request body is empty"}, status=400
            )
        
        data = json.loads(request.body)
        """
        Bulk create doctor
        https://docs.djangoproject.com/en/5.1/ref/models/querysets/#bulk-create
        """
        if isinstance(data, list):
            try:
                doctor_list = []
                for doctor in data:
                    first_name = doctor.get("first_name")
                    last_name = doctor.get("last_name")
                    category_name = doctor.get("category")
                    language = doctor.get("language")

                    field_validator(first_name, "first_name")
                    field_validator(last_name, "last_name")
                    field_validator(category_name, "category")

                    category = Category.objects.filter(name=category_name).first()
                    if not category:
                        return JsonResponse(
                            {"success": False, "message": "Category not found"}, status=404
                        )
                    
                    lang = Language.objects.filter(short_code=language).first()
                    if not lang:
                        return JsonResponse(
                            {"success": False, "message": "Language not found"}, status=404
                        )

                    doctor_list.append(
                        Doctor(
                            first_name=first_name,
                            last_name=last_name,
                            category=category,
                            language=lang,
                        )
                    )
                created_doctor = Doctor.objects.bulk_create(doctor_list)
                res = [
                    {
                        "id": doctor.id,
                        "first_name": doctor.first_name,
                        "last_name": doctor.last_name,
                        "category": doctor.category.name,
                        "language": doctor.language.short_code,
                    }
                    for doctor in created_doctor
                ]
                return JsonResponse({"success": True, "data": res}, status=201)
            except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)
        try:
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            category_name = data.get("category")
            language = data.get("language")

            field_validator(first_name, "first_name")
            field_validator(last_name, "last_name")
            field_validator(category_name, "category")

            category = Category.objects.filter(name=category_name).first()
            if not category:
                return JsonResponse(
                    {"success": False, "message": "Category not found"}, status=404
                )

            lang = Language.objects.filter(short_code=language).first()
            if not lang:
                return JsonResponse(
                    {"success": False, "message": "Language not found"}, status=404
                )

            doctor = Doctor.objects.create(
                first_name=data["first_name"],
                last_name=data["last_name"],
                category=category,
                language=lang,
            )
            return JsonResponse(
                {
                    "success": True,
                    "data": {
                        "id": doctor.id,
                        "first_name": doctor.first_name,
                        "last_name": doctor.last_name,
                        "category": doctor.category.name,
                        "language": doctor.language.short_code,
                    },
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

def field_validator(data, field: str):
    """Field validations

    Args:
        data (_type_): _description_
        field (string): _description_

    Returns:
        JsonResponse: False if field is empty
    """
    if not data:
        return JsonResponse(
            {"success": False, "message": f"{field} is required"}, status=400
        )
    return None

def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render({}))
