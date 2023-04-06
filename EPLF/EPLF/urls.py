# django_project/urls.py
import debug_toolbar
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from EPLF import views


urlpatterns = (
    [
        # path("", TemplateView.as_view(template_name="home.html"), name="home"),
        path('', login_required(views.index), name="index"),
        path("admin/", admin.site.urls),
        path("i18n/", include("django.conf.urls.i18n")),
        path("accounts/", include("accounts.urls")),
        path("managefee/", include("managefee.urls")),
        path("accounts/", include("django.contrib.auth.urls")),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
