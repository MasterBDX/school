from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from main.sitemaps import PostSitemap,StaticSitesSitemap

import debug_toolbar

sitemaps = {
    'posts':PostSitemap,
    'static':StaticSitesSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemaps.xml', sitemap,{'sitemaps':sitemaps }),
    path('admin/defender/', include('defender.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('main.urls', namespace='main')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('tables/', include('school_tables.urls', namespace='tables')),
    path('students/', include('students.urls', namespace='students')),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns