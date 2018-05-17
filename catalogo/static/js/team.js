/**
 * self - vueInstance
 * */
function fetchMemberInfo(self) {
    var info = self.currentMember;
    info.name = 'D.John';
    info.description = 'ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.';
    info.tools = [
        {name: 'Herramienta 1', url: 'http://localhost:8000/catalogo/equipo/detalle/'},
        {name: 'Herramienta 2', url: 'http://localhost:8000/catalogo/equipo/detalle/'},
        {name: 'Herramienta 3', url: 'http://localhost:8000/catalogo/equipo/detalle/'}
    ];

    info.areas = [
        'UX',
        'Desarrollo Web',
        'Desarrollo Movil'
    ];

    info.projects = [
        {name: 'Proyecto N', description: 'Encargado del diseño de la interfaz de la pagina principal'},
        {name: 'Proyecto Y', description: 'Encargado modelamiento de la base de datos'},
        {name: 'Proyecto Z', description: 'Responsable de la version movil '}
    ];

    info.email = "juan.perez@conecta.te";
    info.extension = "321";
}

var app = new Vue({
    el: '#vue-app',
    data: {
        currentMember: {}
    },
    created: function () {
        fetchMemberInfo(this);
    }


});
