from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^library/', include('library.urls')),
    url(r'^login/$', 'library.views.userlogin'),
    url(r'^auth/$', 'library.views.userauth'),
    url(r'^logout/$', 'library.views.userlogout'),
    url(r'^admin/', include(admin.site.urls)),

)
