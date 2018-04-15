from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^addUser/$', views.add_user_view, name='addUser'),
    url(r'^addExample/$', views.add_example, name='addExample'),
    url(r'^example/$', views.example, name='example'),
    url(r'^searchItems/$', views.search_item, name='searchItems'),
    url(r'^tutorial/$', views.tutorial, name='tutorial'),
    url(r'^addTutorial/$', views.add_tutorial, name='addTutorial'),
    url(r'^estrategia/$', views.estrategia_view, name='estrategia'),
    url(r'^addEstrategia/$', views.add_estrategia, name='addEstrategia'),
    url(r'^caracHerramienta/$', views.carac_herramienta_view, name='caracHerramienta')
]