from django.db import models
from django.contrib.auth import get_user_model
from adplist.base.models import TimeStampedModel
from adplist.mentors.choices import SlotStatusChoiceTypes, AppointmentStatusChoiceTypes, ScheduleDaysChoiceTypes
from adplist.members.models import Member

user = get_user_model()


class MentorshipAreas(TimeStampedModel):
    name = models.CharField(max_length=40)


class Mentor(TimeStampedModel):
    user = models.ForeignKey(user, related_name="+", on_delete=models.CASCADE)
    mentorship_areas = models.ManyToManyField(MentorshipAreas, related_name="+")
    is_approved = models.BooleanField(default=False)


class Schedule(TimeStampedModel):
    mentor = models.ForeignKey(Mentor, related_name="+", on_delete=models.CASCADE)
    all_day = models.BooleanField('Always available? e.g. 24 hour service', default=False)
    opening_time = models.DateTimeField('Opening time of day (ignored if allDay = true)', blank=True, null=True)
    closing_time = models.DateTimeField('Closing time of day (ignored if allDay = true)', blank=True, null=True)


# class DaysOfWeek(TimeStampedModel):
#     schedule = models.ForeignKey(Schedule, related_name='+', on_delete=models.CASCADE)
#     day = models.CharField('day of the week', max_length=250, choices=ScheduleDaysChoiceTypes.choices)
#
#
# class NotAvailable(TimeStampedModel):
#     schedule = models.ForeignKey(Schedule, related_name='+', on_delete=models.CASCADE)
#     description = models.TextField('The reason that can be presented to the user as to why this time is not available.')
#     period_start = models.DateField('Service is not available (seasonally or for a public holiday) from this date.')
#     period_end = models.DateField('Service is not available (seasonally or for a public holiday) from this date.')
#

class Slot(TimeStampedModel):
    schedule = models.ForeignKey(Schedule, related_name="+", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=SlotStatusChoiceTypes.choices, default=SlotStatusChoiceTypes.FREE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    comments = models.TextField(null=True, blank=True)


class Appointment(TimeStampedModel):
    mentor = models.ForeignKey(Mentor, related_name="+", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name="+", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=AppointmentStatusChoiceTypes.choices, default=AppointmentStatusChoiceTypes.PENDING)
    slot = models.ForeignKey(Slot, related_name="+", on_delete=models.DO_NOTHING)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    minutes_duration = models.IntegerField(null=True)
