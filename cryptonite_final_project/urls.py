from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cryptonite_final_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^game/', include('notfirstapp.urls',namespace='game')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
