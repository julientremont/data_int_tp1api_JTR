from django.db import models 
from django.contrib.auth.models import User

class Product(models.Model): 
    name = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.name
    
class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)  # Code technique
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    api_key = models.CharField(max_length=64, unique=True, null=True, blank=True)
    is_api_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'No Role'}"
    
    def has_permission(self, permission_code):
        if not self.role:
            return False
        return self.role.permissions.filter(code=permission_code).exists()
    
