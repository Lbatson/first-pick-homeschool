from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurriculumsConfig(AppConfig):
    name = "fphs.curriculums"
    verbose_name = _("Curriculums")
