from django.conf.urls import url
from tracker import views

urlpatterns = [
    url(r'^newskill/', views.newskill, name='newskill'),
    url(r'^skills/', views.skills, name='skills'),
    url(r'^newuser/', views.newuser, name='newuser'),
    url(r'^users/', views.users, name='users'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^download_users_csv/', views.download_users_csv, name='download_users_csv'),
    url(r'^$', views.index, name='index'),
]
