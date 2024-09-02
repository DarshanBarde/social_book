from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.utils.translation import gettext as _
from sqlalchemy import Column, Integer, String, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from rest_framework.authtoken.models import Token
from .database import engine
# Create your models here.

class CustomUser(AbstractUser):
    birth_year = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    public_visiblity = models.BooleanField(default = False)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_set',  # Specify a unique related_name
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_set',  # Specify a unique related_name
        related_query_name='custom_user',
    )
    def register(self):
        self.save()
    
    @staticmethod
    def get_customer_by_username(username):
        try:
            return CustomUser.objects.get(username=username)
        except:
            return False

    def isExists(self):
        if CustomUser.objects.filter(username=self.username):
            return True
        
        return False
    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None

def validate_file_extension(value):
    if not value.name.endswith(('.pdf', '.jpeg','.jpg')):
        raise ValidationError('Only PDF and JPEG files are allowed')


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    year_published = models.IntegerField()
    file = models.FileField(upload_to='', validators=[validate_file_extension])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    


Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'social_book_app_customuser'
    id = Column(Integer, primary_key=True)
    name = Column(String)

Session = sessionmaker(bind=engine)

def fetch_data():
    session = Session()
    result = session.execute(text("SELECT * FROM social_book_app_customuser"))
    data = [dict(row) for row in result]
    return data


class AuthToken(models.Model):
    objects = models.Manager()