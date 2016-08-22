from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone', 'comments', 'date', 'waiting_list')

admin.site.register(Contact, ContactAdmin)

