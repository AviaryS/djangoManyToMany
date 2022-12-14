from django.shortcuts import render, redirect
from datetime import date
from engine.models import *
from engine.forms import *


def index(request):
    students = Student.objects.all()
    return render(request, 'engine/index.html', context={'students': students})


def create(request):
    initialize()
    form = StudentCreateForm()
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            course_ids = request.POST.getlist("courses")
            courses = Course.objects.filter(id__in=course_ids)
            student.courses.set(courses, through_defaults={"date": date.today(), "mark": 0})
        return redirect("home")
    return render(request, "engine/create.html", {"form": form})


def initialize():
    if Course.objects.all().count() == 0:
        Course.objects.create(name="Python")
        Course.objects.create(name="Django")
        Course.objects.create(name="FastAPI")

