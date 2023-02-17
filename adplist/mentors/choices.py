from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class SlotStatusChoiceTypes(TextChoices):
    """
    status of slots. Could have other status like busy-unavailable,
    busy-tentative, entered-in-error, but that's probably an overkill for
    this task

    """
    BUSY = "BUSY", _("busy")
    FREE = "FREE", _("free")


class AppointmentStatusChoiceTypes(TextChoices):
    """
    status of slots. Could have other status like proposed, noshow, entered-in-error, waitlist, but that's probably an overkill for
    this task

    """
    PENDING = "PENDING", _("pending")
    BOOKED = "BOOKED", _("booked")
    CANCELLED = "CANCELLED", _("cancelled")
    FULFILLED = "FULFILLED", _("fulfilled")


class ScheduleDaysChoiceTypes(TextChoices):

    MON = "MON", _("monday")
    TUE = "TUE", _("Tuesday")
    WED = "WED", _("wednesday")
    THU = "THU", _("thursday")
    FRI = "FRI", _("friday")
    SAT = "SAT", _("saturday")
    SUN = "SUN", _("sunday")
