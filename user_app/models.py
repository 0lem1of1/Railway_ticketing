from django.db import models

from django.contrib.auth.models import AbstractUser,BaseUserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin',
        PASSENGER = "PASSENGER",'Passeger'

    base_role = Role.PASSENGER

    role = models.CharField(max_length=10,choices=Role.choices)

    def save(self, *args , **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args,**kwargs)
        
class PassegerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.PASSENGER)
        
class PassegerUser(User):

    base_role = User.Role.PASSENGER

    class Meta:
        proxy = True

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.ADMIN)
        
class AdminUser(User):

    base_role = User.Role.ADMIN

    class Meta:
        proxy = True        
