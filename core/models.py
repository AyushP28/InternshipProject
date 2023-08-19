from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        if not username:
            raise ValueError("The Username field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

    
class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

class Patient(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    address = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    @classmethod
    def create_patient(cls, **kwargs):
        minimum_fields = {
            'status': 'active',
        }
        minimum_fields.update(kwargs)
        try:
            return cls.objects.create(**minimum_fields)
        except ValidationError as e:
            if 'first_name' in e.message_dict and 'last_name' in e.message_dict:
                raise ValueError("First name and last name are required")
    
            if 'date_of_birth' in e.message_dict:
                raise ValueError("Invalid format, Please provide a valid date (YYYY-MM-DD).")
            
            raise ValueError("Invalid data provided. Please check the fields and try again.")

        
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

