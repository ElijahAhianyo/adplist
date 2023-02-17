from collections import namedtuple

from django.db.models.signals import post_save
from django.dispatch import receiver
from adplist.mentors.models import Slot, Schedule
from adplist.mentors.utils import create_slot

@receiver(post_save, sender=Schedule)
def create_schedule_slots(sender, instance, created, **kwargs):
    if created:
        print("Throwing offf signal")
        schedule = namedtuple("Schedule", ["start", "end", "pk"])
        create_slot(schedule(instance.opening_time, instance.closing_time, instance.pk))
        pass
