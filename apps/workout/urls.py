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

    url(r'^create_client_form/$', views.create_client_form, name='create_client_form'),
    url(r'^client_verify/$', views.client_verify, name='client_verify'),
    url(r'^client_search/$', views.client_search, name='client_search'),
    url(r'^all_clients_search/$', views.all_clients_search, name='all_clients_search'),

    url(r'^client_name_search/$', views.client_name_search, name='client_name_search'),
    url(r'^delete_client/(?P<trainer_id>\d)/(?P<client_id>\d)/$', views.delete_client, name='delete_client'),
    url(r'^edit_client/(?P<trainer_id>\d)/(?P<client_id>\d)/$', views.delete_client, name='delete_client'),

    url(r'^create_program/(?P<client_id>\d)/$', views.create_program, name='create_program'),
    url(r'^delete_program/(?P<trainer_id>\d)/(?P<client_id>\d)/$', views.create_program, name='create_program'),
    url(r'^edit_program/(?P<trainer_id>\d)/(?P<client_id>\d)/$', views.create_program, name='create_program'),

    url(r'^create_workout/$', views.create_workout, name='create_workout'),
    url(r'^workout_verify/$', views.workout_verify, name='workout_verify'),
    url(r'^workout_search/$', views.workout_search, name='workout_search'),
    url(r'^delete_workout/$', views.delete_workout, name='delete_workout'),
    url(r'^edit_workout/$', views.edit_workout, name='edit_workout'),
]