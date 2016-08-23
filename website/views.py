from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact


NAME_ERROR = "Please enter your name."
EMAIL_ERROR = "Please enter your email."
CONTACT_SUCCESS = "Thank you for contacting us, we appreciate your interest!"
CONTACT_ANCHOR = 'contact'

def index(request):
    context = {}
    if request.method == "POST":
        context['anchor'] = CONTACT_ANCHOR
        if _valid_new_contact_input(request.POST, request):
            context['success'] = True
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            comments = request.POST.get('comments')
            waiting_list = request.POST.get('waiting_list')
            c = Contact(name=name, email=email, phone=phone, comments=comments, waiting_list=True)
            c.save()
            messages.add_message(request, messages.SUCCESS, CONTACT_SUCCESS)

    return render(request, 'home.html', context)

def _valid_new_contact_input(form_input, request):
    valid = True
    if not form_input.get('name'):
        valid = False
    if not form_input.get('email'):
        valid = False

    return valid
