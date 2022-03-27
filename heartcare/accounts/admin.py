from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse, re_path
from django.utils.translation import gettext_lazy as _
from .models import User, Consultation
from django.utils.html import format_html
admin.site.register(User)


# Register your models here.
class ConsultationAdmin(admin.ModelAdmin):
    model = Consultation
    verbose_name = _('Consultation')
    date_hierarchy = "created_date"
    list_display = (
        "medical_history",
        "consultation_text",
        "created_date",
        "reply",
        "status",
        "approved",
        "get_user_email",
        "account_actions",

    )
    list_filter = ("created_date",)
    order = ["-created_date"]
    fields = (
        "medical_history",
        "consultation_text",
        "reply",
        "approved",
        "status"
    )

    def has_add_permission(self, request, obj=None):
        return False

    def get_user_email(self, obj):
        return obj.user.get()

    def get_urls(self):
        urls = super(ConsultationAdmin, self).get_urls()
        custom_urls = [
            re_path(
                r"^(?P<pk>[0-9]+)/send-account-activation-mail/$",
                self.admin_site.admin_view(self.send_activation_email),
                name="candidate-activate",
            ),
        ]
        return custom_urls + urls

    def send_activation_email(self, request, pk, *args, **kwargs):
        consultation = Consultation.objects.get(pk=pk)
        print(consultation.reply)
        context = {"reply": consultation.reply}
        subject = 'Your Doctor consultation'
        consultation._send_email(
            context=context,
            subject=subject,
            template_path= "accounts/emails/consultation.html",
            to=[
                consultation.user.get(),
            ],
        )
        consultation.approved = True
        consultation.user.approved = True
        consultation.save()
        return redirect(reverse("admin:accounts_consultation_changelist"))

    def accepted(self, obj):
        return obj.filter(status=Consultation.ANSWERED).exists()

    def account_actions(self, obj):
        if obj.approved:
            return format_html(
                "<p>Reply has been sent</p>",
            )
        if not obj.is_onhold():
            return format_html(
                '<a class="button" href="{}">Send email</a>&nbsp;',
                reverse("admin:candidate-activate", args=[obj.pk]),
            )
        return None

    account_actions.short_description = "Account Actions"
    get_user_email.short_description = "User Email"
    account_actions.allow_tags = True

admin.site.register(Consultation, ConsultationAdmin)