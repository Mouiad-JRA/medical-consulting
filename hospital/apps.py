from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _
class HospitalConfig(AppConfig):
    name = 'hospital'
    verbose_name = _('Hospitals')
