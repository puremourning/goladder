from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goladder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('ladder.urls', namespace='ladder')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)
