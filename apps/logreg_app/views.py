# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# readies and renders the register and login page
def index(request):
    return render(request, "index.html")
# validates a new users information and creates that user
def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            pwhash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=pwhash)
            request.session["user_id"] = user.id
    return redirect("/users")
# verifies the users login infromation and adds their information to session
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        user = User.objects.get(email=request.POST["email"])
        request.session["user_id"] = user.id
    return redirect("/users")
# removes the current users infromation from session and logs them out
def logout(request):
    request.session.pop("user_id")
    return redirect("/")