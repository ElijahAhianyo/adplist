from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MentorsConfig(AppConfig):
    name = 'adplist.mentors'
    verbose_name = _("Mentors")

    def ready(self):
        try:
            import adplist.mentors.signals  # noqa F401
        except ImportError:
            pass
