from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'django_apis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('common.urls', namespace='common')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
)
