from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^addUser/$', views.add_user_view, name='addUser'),
    url(r'^addExample/$', views.add_example, name='addExample'),
    url(r'^example/$', views.example, name='example'),
    url(r'^searchItems/$', views.search_item, name='searchItems')
]