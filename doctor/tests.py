from django.test import TestCase, Client
from django.urls import reverse
from doctor.models import Doctor, Category, Clinic, District, Language


# Create your tests here.
class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Magicians")
        cls.district = District.objects.create(name="Wan Chai")
        cls.clinic = Clinic.objects.create(
            name="Wan Chai Clinic",
            district=cls.district,
            address="1/F, 1 Hennessy Road, Wan Chai, Hong Kong",
            phone_no1="28882888",
            consultation_fee=350.00,
            prescription="3 days",
            working_hours="Mon-Fri 9am-6pm",
        )
        cls.language = Language.objects.create(short_code="en", full_name="English")
        cls.doctor = Doctor.objects.create(
            first_name="Harry", last_name="Potter", category=cls.category, language=cls.language
        )

    def test_category_model(self):
        self.assertEqual(self.doctor.category.name, "Magicians")

    def test_district_model(self):
        self.assertEqual(self.district.name, "Wan Chai")

    def test_clinic_model(self):
        self.assertEqual(self.clinic.name, "Wan Chai Clinic")
        self.assertEqual(self.clinic.district.name, "Wan Chai")
        self.assertEqual(
            self.clinic.address, "1/F, 1 Hennessy Road, Wan Chai, Hong Kong"
        )
        self.assertEqual(self.clinic.phone_no1, "28882888")
        self.assertEqual(self.clinic.consultation_fee, 350.00)
        self.assertEqual(self.clinic.prescription, "3 days")
        self.assertEqual(self.clinic.working_hours, "Mon-Fri 9am-6pm")

    def test_doctor_model(self):
        self.assertEqual(self.doctor.first_name, "Harry")
        self.assertEqual(self.doctor.last_name, "Potter")
        self.assertEqual(self.doctor.category.name, "Magicians")
        self.assertEqual(self.doctor.language.short_code, "en")


class APITest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.category = Category.objects.create(name="Magicians")
        cls.district = District.objects.create(name="Wan Chai")
        cls.clinic = Clinic.objects.create(
            name="Wan Chai Clinic",
            district=cls.district,
            address="1/F, 1 Hennessy Road, Wan Chai, Hong Kong",
            phone_no1="28882888",
            consultation_fee=350.00,
            prescription="3 days",
            working_hours="Mon-Fri 9am-6pm",
        )
        cls.language = Language.objects.create(short_code="en", full_name="English")
        cls.doctor = Doctor.objects.create(
            first_name="Harry", last_name="Potter", category=cls.category, language=cls.language
        )

        cls.doctor_post_get_url = reverse("doctor_post_get")
        cls.get_doctor_by_id_url = reverse("doctor_post_get", args=[cls.doctor.id])

    def test_get_doctor_by_id_success(self):
        response = self.client.get(self.get_doctor_by_id_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["first_name"], "Harry")

    def test_get_doctor_by_id_fail(self):
        response = self.client.get(reverse("doctor_post_get", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_doctor_list_success(self):
        response = self.client.get(self.doctor_post_get_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()["data"]) > 0)

    def test_create_doctor_success(self):
        response = self.client.post(
            self.doctor_post_get_url,
            {
                "first_name": "Hermione",
                "last_name": "Granger",
                "category": "Magicians",
                "language": "en",
                "clinics": [{"clinic": "Wan Chai Clinic"}],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["first_name"], "Hermione")

    def test_create_doctor_fail_when_missing_fields(self):
        response = self.client.post(
            self.doctor_post_get_url,
            {
                "first_name": "Hermione",
                "category": "Magicians",
                "language": "en",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
