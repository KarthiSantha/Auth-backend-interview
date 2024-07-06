from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    last_login_time = models.DateTimeField(null = True )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} - {self.role.name}"
    

