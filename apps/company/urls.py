from django.urls import path

from .views import TimetableDetailView, intro

app_name = "company"

urlpatterns = [
    path("", intro, name="intro"),
    path("timetable/<int:id>/", TimetableDetailView.as_view(), name="timetable_detail")
]
