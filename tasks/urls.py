from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.task_list_view),

    url(r'^login/$', views.login_view),
    url(r'^logout/$', views.logout_view),
    url(r'^register/$', views.register_view),

    url(r'^add/$', views.add_task_view),
    url(r'^(?P<task_id>[0-9]+)/edit/$', views.edit_task_view),

]
