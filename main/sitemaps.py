from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from posts.models import Post


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()


class StaticSitesSitemap(Sitemap):
    def items(self):
        return ['main:home','main:about_us',
                'main:contact','main:result-search',
                'main:students-list','tables:exams-table-detail',
                'tables:schedule-detail','accounts:login']
    
    def location(self,item):
        return reverse(item)