# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from ..logreg_app.models import User
from .models import Comment

# Create your views here.
# function for testing login in status doesn't work atm but the two lines of code it has do...wierd
def loggedin(request):
    if "user_id" not in request.session:
        return redirect("/")

# renders the user home page where the user can navigate to other users pages
def index(request):
    # loggedin(request)
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
        "users" : User.objects.exclude(id=request.session["user_id"]).annotate(comment_count=Count("comments")).order_by("-comment_count")
    }
    return render(request, "dashboard.html", context)

# shows a specific users page with all of the comments left for them and has a form for leaving a comment
def show(request, id):
    # loggedin(request)
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "user" : User.objects.get(id=id)
    }
    return render(request, "userpage.html", context)

# process the form for leaving a comment
def comment(request):
    # loggedin(request)
    if "user_id" not in request.session:
        return redirect("/")
    if request.method == "POST":
        errors = Comment.objects.comment_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/comments/' + request.POST["user_id"])
        comment = Comment.objects.create(content=request.POST["content"], recipient=User.objects.get(id=int(request.POST["user_id"])), author=User.objects.get(id=request.session["user_id"]))
    return redirect("/users")