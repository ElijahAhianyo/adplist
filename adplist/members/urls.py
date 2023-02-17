from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path("", views.MemberList.as_view(), name="member_list"),
    path("<int:pk>/", views.MemberDetailView.as_view(), name="member_detail"),
]
