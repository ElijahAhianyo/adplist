from collections import namedtuple

from django.db.models.signals import post_save
from django.dispatch import receiver
from adplist.mentors.models import Slot, Schedule, Appointment
from adplist.mentors.tasks import create_slot
from adplist.mentors.choices import SlotStatusChoiceTypes


@receiver(post_save, sender=Schedule)
def create_schedule_slots(sender, instance, created, **kwargs):
    if created:
        schedule = namedtuple("Schedule", ["start", "end", "pk"])
        create_slot.delay(schedule(instance.opening_time, instance.closing_time, instance.pk))


@receiver(post_save, sender=Appointment)
def update_appointment_slot(sender, instance, created, **kwargs):
    if created:
        slot = instance.slot
        slot.status = SlotStatusChoiceTypes.BUSY
        slot.save()
