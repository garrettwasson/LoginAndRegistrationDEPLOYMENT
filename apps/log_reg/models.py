# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        for key in postData:
            if postData[key] == '':
                errors['empty_fields'] = 'All input fields must be filled'  
        try: 
            if User.objects.get(email=postData['email']):
                errors['nope'] = "This email is already in use."
        except:
            pass
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name can not be blank!"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last name can not be blank!"
        if not email_regex.match(postData['email']):
            errors["email"] = "Invalid email format!"
        if len(postData['password']) < 6:
            errors["password"] = "Password must be at least 6 characters!"
        if postData['confirm_password'] != postData['password']:
            errors["confirm_password"] = "Passwords do not match!"
        return errors
        
    def hashword(self, pass_w):
        password = bcrypt.hashpw(pass_w.encode(), bcrypt.gensalt())
        return password

    def login_validator(self, postData):  
        errors = {}
        for key in postData:
            if postData[key] == '':
                errors['empty'] = 'All input fields must be filled'
                return errors

        this_user = User.objects.filter(email=postData['email'])
        
        try:
            if not bcrypt.checkpw(postData['password'].encode(), this_user[0].password.encode()):
                errors['login'] = 'User info does not match! Please try again OR register!'
        except:
            errors['login'] = 'User info does not match! Please try again OR register!'
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = UserManager()

    def __str__(self):
        return self.first_name

# Create your models here.
