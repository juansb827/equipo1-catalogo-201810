var URL_BASE = window.location.origin;

var tipos = [ /* Se ponene en un array para que sean mostrados en el mismo orden siempre*/
    { key: "-1" , val :"Todas las categorias"},
    { key: "1" , val :"Tecnologia"},
    { key: "2" , val :"Herramienta"},
    { key: "3" , val :"Tutorial"},
    { key: "4" , val :"Ejemplo"},
    { key: "5" , val :"Estrategia Pedagógica"},
    { key: "6" , val :"Desarrollo"}

]

var estados = ["Borrador","En Revisión","Aprobado"]
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
        getItemLink: function (item) {
            return URL_BASE + '/catalogo/verItem/?type='+item.type+'&code='+item.item_code+'&ver='+item.version;
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

            if(scroll == false){ //Search on page reload
                self.searchOptions.type = utils.getParameterByName('type') || -1;
                self.searchOptions.words = utils.getParameterByName('busqueda') || '';
                scroll = true;
            }

            var searchParams = {
                type: self.searchOptions.type, name: self.searchOptions.words
            }

            window.history.pushState('catalogo/', 'Title', '/catalogo/?type='+searchParams.type+'&busqueda='+searchParams.name)



            console.log("searchOarams",searchParams);

            axios.get(URL_BASE + "/catalogo/searchItems",{
                params: searchParams
            }).then(function (response) {
                this.loading=false;
                var data= response.data;
                console.log("data",data);
                self.searching = false;
                self.items = data.map(function (val) {
                    var item = val.fields;
                    if (item.thumbnail)
                        item.thumbnail = utils.getImageUrl(window.CLOUDINARY_NAME, item.thumbnail);
                    else
                        item.thumbnail = '../../static/images/no_image2.svg';

                    if(!tipos[item.type]){
                        console.log("item",item);
                        return null;
                    }

                    item.typeName= tipos[item.type].val;

                    item.statusName =   estados[item.version];
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


