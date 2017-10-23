# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import datetime
import bcrypt

from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# manager for validating user information
class UserManager(models.Manager):
    # validates a user as they register to verify correct information
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) == 0 or len(postData['last_name']) == 0 or len(postData['email']) == 0 or len(postData["password"]) == 0 or len(postData["confpassword"]) == 0:
            errors["all_fields_required"] = "All fields are required"
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be least 2 characters long"
        if not postData['first_name'].isalpha():
            errors['first_name_is_valid'] = "First name can only contain letters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 caracters long"
        if not postData['last_name'].isalpha():
            errors['last_name_is_valid'] = "Last name can only contain letters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email_not_valid"] = "Email must be in a valid format"
        if len(self.filter(email=postData["email"])) != 0:
            errors["email_already_registered"] = "An email matching that has already been registered"
        if len(postData["password"]) < 8:
            errors["password_too_short"] = "Password must contain at least 8 characters"
        if postData["password"] != postData["confpassword"]:
            errors["password_mismatch"] = "Password and Confirm Password must match"
        return errors
# validates a users login infromation
    def login_validator(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData["email"])
            if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
                errors["password_mismatch"] = "passwords didn't match"
        except:
            errors["email_not_found"] = "That email isn't registered"
        return errors

# database table for storing user information
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
