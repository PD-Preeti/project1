from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = 'LMS Admin'
admin.site.site_header = 'LMS Admin'
urlpatterns = [
    path('lms/', admin.site.urls),
    path('adminboard/', include('adminboard.urls')),
    path('', include('employee.urls')),
    path('api/v1/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
