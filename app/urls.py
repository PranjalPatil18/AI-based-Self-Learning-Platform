from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path("", views.index, name= "home"),
    path("log_in", views.log_in, name= "log_in"),
    path("register", views.register, name= "register"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("result", views.result, name= "result"),
    path("add_sentences", views.add_sentences, name= "add_sentences"),
    path("log_out", views.log_out, name= "log_out"),
    path('dashboard_record', views.dashboard_record, name='dashboard_record'),
]