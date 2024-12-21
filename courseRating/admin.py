from django.contrib import admin

from .models import Course, Lecture

admin.site.register(Course)
admin.site.register(Lecture)

# Register your models here.
