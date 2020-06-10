from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/defender/', include('defender.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('main.urls', namespace='main')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('tabels/', include('school_tabels.urls', namespace='tabels')),
    path('students/', include('students.urls', namespace='students')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns