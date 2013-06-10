from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('library.views',
    url(r'^$', 'index'),
    url(r'^details/$', 'mydetails'),
    url(r'^addbook/$', 'addbook'),
    url(r'^addstudent', 'addstudent'),
    url(r'^studentdetail','studentdetail'),
    url(r'^(?P<bb_id>\d+)/issue$', 'issuebook'),
    url(r'^(?P<b_id>\d+)/confirm$', 'confirmation'),
    url(r'^details/returnbook$', 'returnbook'),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'library/login.html'}),
    #url(r'^return/$', 'returnbook'), 

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    
)

#urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
 #   url(r'^admin/', include(admin.site.urls)),
#)
