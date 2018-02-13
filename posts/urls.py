from django.urls import re_path
from . import views

app_name = "posts"

urlpatterns = [
        re_path(r'^$', views.home, name="home"),
        re_path(r'^staff/articles/$', views.all, name="all"),
        re_path(r'^staff/articles/new/$', views.new, name="new"),
        re_path(r'^staff/articles/(?P<id>\d+)/$', views.toggle_publish, name="toggle_publish"),
        re_path(r'^refresh/$', views.refresh, name="refresh"),
        re_path(r'^mail/$', views.mail, name="mail"),
]