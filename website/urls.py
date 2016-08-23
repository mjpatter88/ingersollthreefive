from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^new_contact$', views.new_contact, name='new_contact'),
]
