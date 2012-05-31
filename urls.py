from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/?$','django.contrib.auth.views.login', {
        'template_name': 'login.html',
        }),
    url(r'^logout/?$','django.contrib.auth.views.logout', {
        'next_page': '/',
        }),
    url(r'^signup/?$', 'blog.views.signup'),
    url(r'^profile/?$', 'blog.views.profile'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('blog.views',
    url(r'^$', 'index'),
    url(r'^create$', 'create'),
    url(r'^(?P<slug>\w+)/edit$', 'edit'),
    url(r'^(?P<slug>\w+)/delete$', 'delete'),
    url(r'^(?P<slug>\w+)$', 'detail'),
)
