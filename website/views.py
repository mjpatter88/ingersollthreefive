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

        context['name_value'] = request.POST.get('name')
        context['email_value'] = request.POST.get('email')
        context['phone_value']= request.POST.get('phone')
        context['comments_value'] = request.POST.get('comments')
        context['waiting_list_value'] = bool(request.POST.get('waiting_list'))

        if _valid_new_contact_input(request.POST, context):
            context['success'] = CONTACT_SUCCESS
            c = Contact(name=context['name_value'], email=context['email_value'],
                        phone=context['phone_value'], comments=context['comments_value'],
                        waiting_list=context['waiting_list_value'])
            c.save()
            messages.add_message(request, messages.SUCCESS, CONTACT_SUCCESS)

    return render(request, 'home.html', context)

def _valid_new_contact_input(form_input, context):
    valid = True
    if not form_input.get('name'):
        valid = False
        context['name_error'] = NAME_ERROR
    if not form_input.get('email'):
        valid = False
        context['email_error'] = EMAIL_ERROR

    return valid
