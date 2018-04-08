var URL_BASE = window.location.origin;
/*var thumbnail=item.fields.thumbnail;
                    if(thumbnail)
                        thumbnail='https://res.cloudinary.com/hn6nvsi2y/'+thumbnail;
                    else
                        thumbnail='../../static/images/no_image2.svg';

                    var _itemBox =  '<div class="col-md-4 col-lg-4 col-sm-12">' +
                        '<div class="card">' +
                            '<div class="card-img">' +
                                '<img src="{{item.thumbnail}}}">' +
                            '</div>' +

                            '<div class="card-body">' +
                                '<h4 class="card-title">{{ item.name }}</h4>' +
                                '<p class="card-text">{{ item.description }}</p>' +
                            '</div>' +
                            '<div class="card-footer">' +
                                '<a style="color:#007bff" class="card-link" >TIPO</a>' +
                            '</div>' +
                            '</div>' +
                        '</div>';
*/

Vue.component('greeting', {

    template: '<p>{{a}} - {{ items.length }}</p>',//_itemBox
    data: function () {
        return {
            a: 1,
            items: []
        }
    },
    methods: {
        update: function () {
            var self = this;

            $.getJSON(URL_BASE + "/catalogo/searchItems", {type: '-1', name: ''}).done(function (data) {
                var items = data.map(function (val) {
                    var item = val.fields;
                    if (item.thumbnail)
                        item.thumbnail = 'https://res.cloudinary.com/hn6nvsi2y/' + item.thumbnail;
                    else
                        item.thumbnail = '../../static/images/no_image2.svg';
                    return item;
                });
                self.items = items;
                console.log('Processed', this.items);
            })
        }
    },
    created: function () {

    }


});


var tipos = [
    { key: "-1" , val :"Todas las categorias"},
    { key: "1" , val :"Tecnologia"},
    { key: "2" , val :"Herramienta"},
    { key: "3" , val :"Tutorial"},
    { key: "4" , val :"Ejemplo"},
    { key: "5" , val :"Estrategia Pedagógica"}

]
var app = new Vue({
    el: '#vue-app',
    data:
        {
            searching: false,
            searchOptions: {
                words: '',
                type: -1
            },
            items: [],
            currentPage: 1,
            tipos: tipos
        }
    ,
    methods: {
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

            axios.get(URL_BASE + "/catalogo/searchItems",{
                params:{
                    type: self.searchOptions.type, name: self.searchOptions.words
                }
            }).then(function (response) {
                this.loading=false;
                var data= response.data;
                console.log("data",data);
                self.searching = false;
                self.items = data.map(function (val) {
                    var item = val.fields;
                    if (item.thumbnail)
                        item.thumbnail = 'https://res.cloudinary.com/hn6nvsi2y/' + item.thumbnail;
                    else
                        item.thumbnail = '../../static/images/no_image2.svg';
                    item.typeName= tipos[item.type].val;
                    return item;
                });
                console.log('Processed - Self ', self.items);



                if(scroll){
                    $("body,html").animate({
                        scrollTop: $('#palabrasBusqueda').first().offset().top
                    },1000)
                }

            }).catch(function (err) {
                this.loading=false;
                console.log("Error en la busqueda", err);
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
            console.log('pc', Math.ceil(this.items.length / 6));
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


