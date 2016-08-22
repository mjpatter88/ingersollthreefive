from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact

def index(request):
        if request.method == "POST":
            print("POST received.")
            c = Contact(name="Liz", email="lpatterson@gmail.com", waiting_list=True)
            c.save()
        return render(request, 'home.html')
