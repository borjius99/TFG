from django.urls import include, re_path
from django.views.generic.base import TemplateView

from FakeApp import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^deploy/$', views.deploy_Contract, name='deploy'),
    re_path(r'^register/$', views.signup_view, name="register"),
    re_path(r'^login/$', views.login_view, name="login"),
    re_path(r'^logout/$', views.logout_view, name="logout"),
    re_path(r'^feed/$', views.principal, name='principal'),
    re_path(r'users/$', views.search_user, name='search_user'),
    re_path(r'createNews/$', views.createNews, name='create'),
    re_path(r'vote/$', views.voteNews, name='vote'),
    re_path(r'newsContent/$', views.readNews, name='read'),
    re_path(r'profile/$', views.profile, name='profile')
]
