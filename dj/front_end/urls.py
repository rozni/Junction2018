from django.urls import path

from . import views


app_name = 'front_end'
urlpatterns = [
    path('v1/', views.v1),
    path('v2/', views.v2),
]
