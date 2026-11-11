from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views

admin.site.site_header = "Godfred online shop Admin"
admin.site.site_title = "Godfred online shop Admin"
admin.site.index_title = "Welcome to Godfred online shop Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store_views.home, name='home'),
    path('panel/', include('dashboard.urls')),
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

