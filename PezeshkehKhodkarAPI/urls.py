from django.contrib import admin
from django.urls import path, include
from decouple import config

# Website urls

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(config("ADMIN_URL"), admin.site.urls),    # Admin url
    path('api/', include('api.urls')),  # API pages
    path('', include('pages.urls')),    # Pages
]
