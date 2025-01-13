from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('auth_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('coderr_app.api.urls')),
]
