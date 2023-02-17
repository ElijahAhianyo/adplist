from django.contrib import admin
from adplist.mentors.models import Mentor, MentorshipAreas, Schedule, Slot, Appointment  # , NotAvailable


# Register your models here.
class MentorAdmin(admin.ModelAdmin):
    model = Mentor
    list_display = [
        "user",
        # "mentorship_areas",
        "is_approved",
    ]
    list_filter = ["is_approved"]
    search_fields = ["user", "is_approved", ]

    # readonly_fields = AUDIT_FIELDS + []
    # fieldsets = [
    #     (
    #         _("UPDATE"),
    #         {
    #             "fields": [
    #                 "building_name",
    #                 "street_number",
    #                 "street_name",
    #                 "town_name",
    #                 "postal_code",
    #                 "city",
    #                 "subregion",
    #                 "region",
    #                 "country",
    #                 "longitude",
    #                 "latitude",
    #             ]
    #         },
    #     ),
    #     (_("AUDIT"), {"fields": AUDIT_FIELDS}),
    # ]

    # inlines = [
    #     UserProfileAddressInline,
    #     CompanyAddressInline,
    #     JobAdvertAddressInline,
    # ]


class MentorshipAreasAdmin(admin.ModelAdmin):
    model = MentorshipAreas
    list_display = [
        "name",
        # "mentorship_areas",
        # "is_approved",
    ]
    list_filter = ["name"]
    search_fields = ["name", ]


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    list_display = [
        "mentor",
        "all_day",
        "opening_time",
        "closing_time",
    ]


class SlotAdmin(admin.ModelAdmin):
    model = Slot
    list_display = [
        "schedule",
        "status",
        "start",
        "end",
        "comments",
    ]


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment


admin.site.register(Mentor, MentorAdmin)
admin.site.register(MentorshipAreas, MentorshipAreasAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Appointment, AppointmentAdmin)
