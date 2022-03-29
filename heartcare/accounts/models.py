from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))

CHEST_PAIN_CHOICES = (
    ('asympt', 'Asympt'),
    ('atyp_angina', 'Atyp_angina'),
    ('non_anginal', 'Non_anginal')
)

REST_ELECTRO_CHOICES = (
    ('normal', _('Normal')),
    ('left_vent_hyper', _('Left_vent_hyper')),
    ('st_t_wave_abnormality', _('St_t_wave_abnormality'))
)


class Consultation(models.Model):
    ANSWERED = "answered"
    ONHOLD = "hold"

    STATUS_CHOICES = (
        (ANSWERED, ("Answered")),
        (ONHOLD, ("On Hold")),
    )
    status = models.CharField(
        ("Status"), max_length=50, choices=STATUS_CHOICES, default=ONHOLD
    )

    medical_history = models.TextField()
    consultation_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(_("Is Approved"), default=False, blank=True)

    reply = models.TextField(null=True)

    def is_answered(self):
        if self.status == "answered":
            return True
        return False

    def is_onhold(self):
        if self.status == "hold":
            return True
        return False

    def _send_email(self, context=None, subject="", template_path=None, to=None):
        context = context
        context.update({"site": Site.objects.get_current()})

        email = EmailMessage()
        email.subject = subject
        email.body = render_to_string(template_path, context=context)
        email.to = to
        email.content_subtype = "html"
        email.send()

    class Meta:
        verbose_name = _('Consultation')
        verbose_name_plural = _('Consultations')


class User(AbstractUser):
    # username = None
    role = models.CharField(_('role'), max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(_('gender'), max_length=10, blank=False, null=True, choices=GENDER_CHOICES, default="")
    email = models.EmailField(_('Email'), unique=True, blank=False, null=True,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    age = models.PositiveIntegerField(_('age'), blank=False, null=True,
                                      error_messages={
                                          'Negative integer': "Please enter a Valid age",
                                      })
    phone_number = models.CharField(_('Phone Number'), unique=True, blank=True, null=True, max_length=20,
                                    error_messages={
                                        'unique': "A user with that phone number already exists."
                                    })
    approved = models.BooleanField(_("Is Approved"), default=False, blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, null=True, related_name="user")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __unicode__(self):
        return self.username

    objects = UserManager()


class Person(models.Model):
    age = models.PositiveIntegerField(_('age'), blank=False, null=True,
                                      error_messages={
                                          'Negative integer': "Please enter a Valid age",
                                      })
    chest_pain_type = models.CharField(_('chest pain'), max_length=20, blank=False, null=True,
                                       choices=CHEST_PAIN_CHOICES, default="")
    rest_electro = models.CharField(_('rest electro'), max_length=22, blank=False, null=True,
                                    choices=REST_ELECTRO_CHOICES, default="")
    rest_blood_pressure = models.PositiveIntegerField(_('rest blood pressure'), blank=False, null=True,
                                                      error_messages={
                                                          'Negative integer': "Please enter a Valid age",
                                                      })
    max_heart_rate = models.PositiveIntegerField(_('max heart rate'), blank=False, null=True,
                                                 error_messages={
                                                     'Negative integer': "Please enter a Valid age",
                                                 })
    blood_sugar = models.BooleanField(_("blood sugar"), default=False, blank=True)
    exercice_angina = models.BooleanField(_("exercice angina"), default=False, blank=True)
