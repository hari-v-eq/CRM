from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
import math
from django.urls import reverse

class User(models.Model):
    email = models.EmailField(unique=True,blank=False)
    password = models.CharField(max_length=20)
    otp =models.IntegerField(default=459)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10)
    first_time_login=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now=True,blank=False)

    def __str__(self):
        return self.email+ "- "+self.role

class CEO(models.Model):
    user_id = models.ForeignKey(User,on_delete=CASCADE, related_name='CEO',null=False)
    firstname = models.CharField(max_length=50)
    lastname =models.CharField(max_length=50)
    contact = models.CharField(max_length=11)
    address=models.TextField(max_length=500)
    profile_pic=models.FileField(upload_to='media/images',default='static/default.jpg')
    gender = models.CharField(max_length=30)
    

    def __str__(self):
        return self.firstname 

class Manager(models.Model):   
    user_id = models.ForeignKey(User,on_delete=CASCADE, related_name='Manager',null=False) 
    firstname = models.CharField(max_length=50)
    lastname =models.CharField(max_length=50)
    gender=models.CharField(max_length=20)
    contact = models.CharField(max_length=11)
    address=models.TextField(max_length=500)
    job_profile=models.TextField(max_length=500)
    birthdate=models.DateField(blank=True,null=True) 
    joiningdate=models.DateField(blank=True,null=True)
    salary=models.IntegerField()
    marital_status=models.CharField(max_length=20)
    id_proof=models.FileField(upload_to='media/images',default='static/default.jpg')
    profile_pic=models.FileField(upload_to='media/files',blank=True,null=True)

    def __str__(self):
          return self.firstname+ "- "+self.job_profile

class Employee(models.Model):   
    user_id = models.ForeignKey(User,on_delete=CASCADE, related_name='Employee',null=False) 
    firstname = models.CharField(max_length=50)
    lastname =models.CharField(max_length=50)
    gender=models.CharField(max_length=20)
    contact = models.CharField(max_length=11)
    address=models.TextField(max_length=500)
    job_profile=models.TextField(max_length=500)
    birthdate=models.DateField(blank=True,null=True) 
    joiningdate=models.DateField(blank=True,null=True)
    salary=models.IntegerField()
    marital_status=models.CharField(max_length=20)
    id_proof=models.FileField(upload_to='media/images',default='static/default.jpg')
    profile_pic=models.FileField(upload_to='media/files',blank=True,null=True)

    def __str__(self):
          return self.firstname+ "- "+self.job_profile


class Task(models.Model):
    
    
    firstname = models.CharField(max_length=50)
    title = models.CharField(max_length=50,unique=True)
    description =models.TextField(max_length=200)
    priority=models.CharField(max_length=20,default="None")
    start_date=models.DateTimeField(blank=True, null=True)
    end_date=models.DateField(blank=True, null=True)
    status=models.CharField(max_length=20,default="Pending")
    created_at = models.DateTimeField(auto_now=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    
    def __str__(self):
          return self.title

class Message(models.Model):

    firstname = models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    message =models.TextField(max_length=200)
    status=models.CharField(max_length=20,default="Pending")
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True) 
    def __str__(self):
            return self.message

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT) 
    created_on = models.DateTimeField(auto_now=True,blank=True)
    action_taken = models.CharField(max_length=255)
    
    def __str__(self):
        return self.action_taken

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    def __str__(self):
        return self.title
@property
def get_html_url(self):
    url = reverse('CEO/calender', args=(self.id,))
    return f'<a href="{url}"> {self.title} </a>'
   