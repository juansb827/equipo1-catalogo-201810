var URL_BASE = window.location.origin;



var tipos = [ /* Se ponene en un array para que sean mostrados en el mismo orden siempre*/
    { key: "-1" , val :"Todas las categorias"},
    { key: "1" , val :"Tecnologia"},
    { key: "2" , val :"Herramienta"},
    { key: "3" , val :"Tutorial"},
    { key: "4" , val :"Ejemplo"},
    { key: "5" , val :"Estrategia Pedagógica"},
    { key: "6" , val :"Desarrollo"},
    { key: "7"  ,  val: "Disciplina"}

]

var estados = ["Borrador","En Revisión","Aprobado"]

var app = new Vue({
    el: '#vue-app',

    data:
        {
            userId: window.userId,
            modal: {
                title: '',
                subtitle: '',
                messages: []
            },
            showStatus: window.authenticated,
            searching: false,
            searchOptions: {
                words: '',
                type: -1
            },
            items: [],
            itemsInfo: {},
            currentPage: 1,
            tipos: tipos
        }
    ,
    methods: {
        showMessages: function (messages) {
            $('#exampleModal').modal('show');
            this.modal.title = "No se puede editar el elemento";
            this.modal.subtitle = "Razones:";
            this.modal.messages = messages;
        },
        editItem: function (item) {

            var messages = [];

            if (this.itemsInfo[item.item_code]) {
                if (this.itemsInfo[item.item_code].onRevision) {
                    messages.push("El elemento tiene cambios pendientes por aprobación.");
                }

                if (this.itemsInfo[item.item_code].editingByCurrentUser) {
                    messages.push("Ya tiene una version en borrador de este elemento.");
                }
            }

            if (messages.length > 0) {
                this.showMessages(messages);
                return;
            }


            window.location = this.getItemLink(item, true);
        },
        getItemLink: function (item, edit) {
            edit = edit ? 1 : 0;
            return URL_BASE + '/catalogo/verItem/?type=' + item.type + '&e=' + edit + '&code=' + item.item_code + '&ver=' + item.version;
        },
        goToPage: function (index) {
            if (index > 0 && index <= this.pageCount) this.currentPage = index;
        },
        nextPage: function () {
            this.goToPage(this.currentPage + 1);

        },
        prevPage: function () {
            this.goToPage(this.currentPage - 1);

        },
        buscar: function (scroll) {

            this.searching = true;
            this.currentPage = 1;
            var self = this;

            if (scroll === false) { //Search on page reload
                self.searchOptions.type = utils.getParameterByName('type') || -1;
                self.searchOptions.words = utils.getParameterByName('busqueda') || '';
                scroll = true;
            }

            var searchParams = {
                type: self.searchOptions.type, name: self.searchOptions.words
            };

            window.history.pushState('catalogo/', 'Title', '/catalogo/?type=' + searchParams.type + '&busqueda=' + searchParams.name);



            self.itemsInfo = {};

            axios.get(URL_BASE + "/catalogo/searchItems", {

                params: searchParams
            }).then(function (response) {
                this.loading = false;
                var data = response.data;
                self.searching = false;
                self.items = data.map(function (val) {
                    var item = val.fields;
                    if (item.thumbnail)
                        item.thumbnail = utils.getImageUrl(window.CLOUDINARY_NAME, item.thumbnail);
                    else
                        item.thumbnail = '../../static/images/no_image2.svg';

                    if (!tipos[item.type]) {
                        return null;
                    }

                    item.typeName = tipos[item.type].val;

                    item.statusName = estados[item.version];

                    if (self.userId) {
                        if (item.version === 2) {
                            item.editable = true;
                        }

                        if (!self.itemsInfo[item.item_code]) {
                            self.itemsInfo[item.item_code] = {
                                onRevision: false,
                                editingByCurrentUser: false
                            };
                        }

                        if (item.version === 1)
                            self.itemsInfo[item.item_code].onRevision = true;
                        if (item.version === 0 && item.author === self.userId)
                            self.itemsInfo[item.item_code].editingByCurrentUser = true;

                        switch (item.version) {
                            case 0:
                                item.iconName = "draft.png";
                                break;
                            case 1:
                                item.iconName = "magnifying_glass.png";
                                break;
                            case 2:
                                item.iconName = "check.png";
                                break;
                        }

                        if (item.version === 0 && item.author !== self.userId) { //Solo el autor ve su borrador
                            return null
                        }
                    }


                    return item;
                }).filter(function (value) {
                    return value != null;
                });


                if (scroll) {
                    $("body,html").animate({
                        scrollTop: $('#palabrasBusqueda').first().offset().top
                    }, 1000)
                }

            }).catch(function (err) {
                this.loading = false;
            })


        }


    },
    computed: {
        paginatedItems: function () {

            var itemsPerPage = 6;
            var offset = (this.currentPage - 1) * itemsPerPage;
            return this.items.slice(offset, offset + itemsPerPage);
        },
        pageCount: function () {
            return Math.ceil(this.items.length / 6);
        }
    },
    filters: {
        shorten: function (texto) {
            if (texto.length <= 60) return texto;
            else return texto.slice(0, 57) + "...";

        }
    },
    created: function () {
        this.buscar(false);
    }

});


