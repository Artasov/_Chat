from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('Core.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),
    path('rooms/', include('APP_Room.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)