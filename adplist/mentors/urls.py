from django.urls import path

from . import views

app_name = "mentors"

urlpatterns = [
    path("", views.MentorList.as_view(), name="mentor_list"),
    path("<int:pk>/", views.MentorDetailView.as_view(), name="mentor_detail"),
    path("appointments/", views.AppointmentList.as_view(), name="appointment_list"),
    path("appointments/<int:pk>/", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("schedules/", views.ScheduleList.as_view(), name="schedule_list"),
    path("schedules/<int:pk>/", views.ScheduleDetailView.as_view(), name="schedule_detail"),
    path("<int:pk>/approve/", views.MentorApproveView.as_view(), name="mentor_approve"),
    path("slots/", views.SlotList.as_view(), name="slot_list"),
    path("slots/<int:pk>/", views.SlotDetailView.as_view(), name="slot_detail"),

]

