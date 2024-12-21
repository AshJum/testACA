from django.shortcuts import render, get_object_or_404
from .models import Course, Lecture
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout



def index(request):
    if request.user.is_authenticated:
        objs = Course.objects.all()
        return render(request, "courseRating/index.html", {'objs':objs})
    else:
        return HttpResponseRedirect('/login')

def register(request):
    if request.method == "GET":
        return render(request, "courseRating/register.html")
    else:
        try:
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]
            age = request.POST["age"]
            email = request.POST["email"]
            password = request.POST["password"]
            repeat_password = request.POST["repeat_password"]
        except:
            return render(request, "courseRating/register", {'error_message':"missed field"})

        if password != repeat_password:
            return render(request, "courseRating/register.html", {"error_message": "Password not match."})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.firstName = first_name
        user.lastName = last_name
        user.age = age
        user.save()

        Lecture_user = Lecture(user=user, age=age)
        Lecture_user.save()

        return HttpResponseRedirect("/login")



def user_login(request):
    if request.method == "GET":
        return render(request, 'courseRating/login.html')
    else:
        try:
            username = request.POST["username"]
            password = request.POST["password"]
        except:
            return render(request, 'courseRating/login.html', {'error_message':"missed field"})

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        render(request, 'courseRating/login', {'error_message':'wrong email or password'})

    return render(request, "courseRating/login.html")


def detail(reqeuest, course_id):
    if reqeuest.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        return render(reqeuest, 'courseRating/detail.html', {'course':course})
    else:
        return HttpResponseRedirect('/login')


def rate(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)

        if request.method == "POST":
            try:
                rate_number = int(request.POST.get("rate", 0))
            except ValueError:
                return render(
                    request,
                    "courseRating/rate.html",
                    {"course": course, "error_message": "Enter a valid number for rate!"}
                )

            if rate_number < 1 or rate_number > 10:
                return render(
                    request,
                    "courseRating/rate.html",
                    {"course": course, "error_message": "Enter a number between 1 and 10!"}
                )

            course.rate = (course.rate * course.count + rate_number) / (course.count + 1)
            course.count += 1
            course.save()

            return HttpResponseRedirect('/')
    else:
        return redirect('/login')

    return render(request, "courseRating/rate.html", {"course": course})
