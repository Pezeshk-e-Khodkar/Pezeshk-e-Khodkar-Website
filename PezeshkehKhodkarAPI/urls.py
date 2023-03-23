from django.contrib import admin
from django.urls import path, include

# Website urls

urlpatterns = [
    path('admin/', admin.site.urls),    # Admin url
    path('api/', include('api.urls')),  # API pages
    path('', include('pages.urls')),    # Pages
]