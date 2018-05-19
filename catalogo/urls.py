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

    url(r'^equipo/detalle/$', views.integrante_view, name='detalleIntegrante'),
    # rutas para creacion de items
    url(r'^crearEstrategia/$', views.crear_estrategia_view, name='crearEstrategia'),
    url(r'^crearDesarrollo/$', views.crear_desarrollo_view, name='crearDesarrollo'),
    url(r'^crearHerramienta/$', views.crear_herramienta_view, name='crearHerramienta'),
    url(r'^crearEjemplo/$', views.crear_ejemplo_view, name='crearEjemplo'),
    url(r'^crearTutorial/$', views.crear_tutorial_view, name='crearTutorial'),
    url(r'^crearDisciplina/$', views.crear_disciplina_view, name='crearDisciplina'),

    url(r'^devTech/$', views.getDevTech, name='getDevTech'),
    url(r'^equipo/$', views.getMembers, name='getMembers'),
    url(r'^technologies/$', views.technologies, name='tecnologias'),
    url(r'^tools/$', views.tools, name='tools'),
    url(r'^strategies/$', views.strategies, name='strategies'),

    url(r'^verItem/$', views.mostrar_item, name='viewItem'),
    url(r'^aprobarRevision/$', views.aprobarRevision, name='aprobarRevision'),
    #  url(r'^verItem/([0-9]{1})/([0-9]+)/([0-9]{1})/$', views.mostrar_item, name='viewItem'),
    url(r'^item/$', views.get_item, name='getItem'),
    url(r'^caracHerramienta/$', views.crear_herramienta_view, name='caracHerramienta'),
    url(r'^taxonomiasMain/$', views.taxonomiasMain, name='taxonomiasMain')


]
