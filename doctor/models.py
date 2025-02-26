from django.db import models

""" Doctor Model """
class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    category = models.ForeignKey('Category',on_delete=models.DO_NOTHING, null=True, blank=True)
    language = models.ForeignKey('Language',on_delete=models.DO_NOTHING)
    clinics = models.ManyToManyField('Clinic', through='ClinicDoctor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

""" Clinic Model """
class Clinic(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey('District',on_delete=models.DO_NOTHING,)
    address = models.CharField(max_length=255)
    phone_no1 = models.CharField(max_length=15)
    phone_no2 = models.CharField(max_length=15, blank=True)
    consultation_fee = models.DecimalField(max_digits=7, decimal_places=2)
    prescription = models.CharField(max_length=63)
    working_hours = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

""" ClinicDoctor Many to Many Model """
class ClinicDoctor(models.Model):
    clinic = models.ForeignKey('Clinic',on_delete=models.DO_NOTHING,)
    doctor = models.ForeignKey('Doctor',on_delete=models.DO_NOTHING,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('clinic', 'doctor') # Ensure that a doctor can only be registered in a clinic once.

    def __str__(self):
        return self.clinic.name + ' - ' + self.doctor.last_name + ' ' + self.doctor.first_name

""" Category Model """   
class Category(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

""" District Model """
class District(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name

""" Language Model"""
class Language(models.Model):
    short_code = models.CharField(max_length=7)
    full_name = models.CharField(max_length=31)

    def __str__(self):
        return self.full_name
    
""" Translation Model """
class Translation(models.Model):
    lang = models.CharField(max_length=7)
    key = models.TextField()
    value = models.TextField()

    class Meta:
        unique_together = ('lang', 'key')

    def __str__(self):
        return self.value
