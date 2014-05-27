from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import router, task_router, TaskView, create_user, TestToken


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'crocoapi.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^', include(router.urls)),
                       url(r'^', include(task_router.urls)),
                       url(r'^user/$',create_user),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^test/', TestToken.as_view() ),
                       url(r'^admin/', include(admin.site.urls)),
)
