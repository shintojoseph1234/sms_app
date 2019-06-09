from django.contrib import admin
from django.urls import path

from sms import views


urlpatterns = [
    # POST customer_inputs for risk_score
    path('',  views.index, name='index'),
    path('register/',  views.register, name='register'),
    path('login/',  views.signin, name='login'),
    path('add/',  views.add, name='add'),
    path('success/',  views.success, name='success'),
    path('logout/',  views.signout, name='logout'),
    path('api/send_sms/',  views.send_sms, name='send_sms'),

]
