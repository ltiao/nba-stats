from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nba_stats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^nba/', include('nba.urls')),
    url(r'^test/', TemplateView.as_view(template_name="index.html")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
