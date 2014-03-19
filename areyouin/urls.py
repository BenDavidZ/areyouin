from django.conf.urls import patterns, include, url

from areyouin import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'areyouin_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^(?P<event_id>\d+)/detail/$', views.detail, name='detail'),
    url(r'^(?P<event_id>\d+)/(?P<participant_id>\d+)/$', views.add_to_event, name='add_to_event'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^create/$', views.create_event, name='create_event'),

)
