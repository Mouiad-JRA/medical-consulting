from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('hospital.urls')),
    path('appointment/', include('appointment.urls')),
    path('captcha/', include('captcha.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
