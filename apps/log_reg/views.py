# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages

def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = ''
    return render(request, 'log_reg/index.html')

# Create your views here.

def create(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = User.objects.hashword(request.POST['password'])
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
        
        request.session['user_id'] = new_user.id
        request.session['name'] = new_user.first_name
        return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        this_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = this_user.id
        request.session['name'] = this_user.first_name
        return redirect('/success')   
            
def success(request):
    context = {
        "user_id" : request.session['user_id'],
        "name" : request.session['name']
    }
    return render(request, "log_reg/success.html", context)
def clear(request):
    request.session.clear()
    return redirect('/')