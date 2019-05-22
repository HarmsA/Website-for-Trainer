from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^login_verify/$', views.login_verify, name='login_verify'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_verify/$', views.register_verify, name='register_verify'),

    url(r'^create_client/(?P<trainer_id>\d)/$', views.create_client, name='create_client'),
]