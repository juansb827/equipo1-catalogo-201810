from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^addUser/$', views.add_user_view, name='addUser'),
    url(r'^addExample/$', views.add_example, name='addExample'),
    url(r'^example/$', views.example, name='example'),
    url(r'^addTool/$', views.add_tool, name='addTool'),
    url(r'^tool/$', views.tool, name='tool'),
    url(r'^searchItems/$', views.search_item, name='searchItems'),
    url(r'^tutorial/$', views.tutorial, name='tutorial'),
    url(r'^addTutorial/$', views.add_tutorial, name='addTutorial'),
    url(r'^estrategia/$', views.estrategia_view, name='estrategia'),
    url(r'^addEstrategia/$', views.add_estrategia, name='addEstrategia'),
    # rutas para creacion de items
    url(r'^crearEstrategia/$', views.crear_estrategia_view, name='crearEstrategia'),
    url(r'^crearDesarrollo/$', views.crear_desarrollo_view, name='crearDesarrollo'),
    url(r'^devTech/$', views.getDevTech, name='getDevTech'),
    url(r'^verItem/$', views.mostrar_item, name='viewItem'),
    url(r'^aprobarRevision/$', views.aprobarRevision, name='aprobarRevision'),
    #  url(r'^verItem/([0-9]{1})/([0-9]+)/([0-9]{1})/$', views.mostrar_item, name='viewItem'),
    url(r'^item/$', views.get_item, name='getItem'),

]
