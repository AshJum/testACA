from django.urls import path

from . import views


app_name = 'courseRating'
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("<int:course_id>/", views.detail, name="detail"),
    path("<int:course_id>/rate/", views.rate, name="rate"),
]