from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact


NAME_ERROR = "Please enter your name."
NAME_TAG = "NAME"
EMAIL_ERROR = "Please enter your email."
EMAIL_TAG = "EMAIL"

CONTACT_SUCCESS = "Thank you for contacting us, we appreciate your interest!"

def index(request):
    return render(request, 'home.html')

def new_contact(request):
    if request.method == "POST":
        if _valid_new_contact_input(request.POST, request):
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            comments = request.POST.get('comments')
            waiting_list = request.POST.get('waiting_list')
            c = Contact(name=name, email=email, phone=phone, comments=comments, waiting_list=True)
            c.save()
            messages.add_message(request, messages.SUCCESS, CONTACT_SUCCESS)

    return redirect('/#contact')

def _valid_new_contact_input(form_input, request):
    valid = True
    if not form_input.get('name'):
        valid = False
        messages.add_message(request, messages.ERROR, NAME_ERROR, extra_tags=NAME_TAG)
    if not form_input.get('email'):
        valid = False
        messages.add_message(request, messages.ERROR, EMAIL_ERROR, extra_tags=EMAIL_TAG)

    return valid
