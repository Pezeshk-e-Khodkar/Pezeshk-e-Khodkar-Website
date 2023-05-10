from django.contrib import admin
from django.urls import path, include
from decouple import config
from django.conf.urls.static import static
from django.conf import settings
from .views import  *

# Website urls

urlpatterns = [
    path('admin/', include('admin_honeypot.urls',  # Fake Admin Page
                           namespace='admin_honeypot')),
    path(config("ADMIN_URL"), admin.site.urls),    # Admin url
    path('', include('pages.urls')),               # Pages
    path('', include('accounts.urls')),            # Pages related to Accounts
    path('', include('dashboard.urls')),           # Dashboard
    path("robots.txt", RobotTxtView.as_view()),    # robots.txt
    path("sitemap.xml", SitMapView.as_view())      # Sitemap.xml
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
