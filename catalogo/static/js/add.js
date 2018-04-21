var URL_BASE = window.location.origin;
var IMG_BASE = 'https://res.cloudinary.com/hn6nvsi2y/';
//http://localhost:8000/catalogo/verItem/?type=6&code=55&ver=0

TECHNOLOGY = "1"
TOOL = "2"
TUTORIAL = "3"
EXAMPLE = "4"
STRATEGY = "5"
DEVELOPMENT = "6"

var typeName = {
     "-1" :"Todas las categorias",
      "1" :  "Tecnologia",
     "2":"Herramienta",
     "3"  :"Tutorial",
      "4" :"Ejemplo",
     "5" :"Estrategia Pedagógica",
     "6":"Desarrollo"
}


Vue.use(window.vuelidate.default)

var temp =
    '<div>' +
    '<span class="btn btn-success fileinput-button">' +
    '            <i class="glyphicon glyphicon-plus"></i>' +
    '            <span>Agregar imagen...</span>' +
    '            <input id="imgInp" type="file" class="upload-button" v-on:change="newFile">' +
    '</span>' +
    '<div class="images" style="display: flex;flex-wrap:wrap; justify-content:center" v-if="images.length">' +
    '            <div class="card" v-for="img in images" >' +
    '                <img class="img-preview" v-bind:src="img.src" v-bind:class="{uploading : img.uploading}">' +
    '                <div class="wrapper" v-if="img.uploading">' +
    '                    <div class="loader-container-2">' +
    '                        <div id="search-loader" class="loader-2"></div>' +
    '                   </div>' +
    '                </div>' +
    '                <div class="delete" v-on:click="removeImg"><img style="height:50px" src="../../static/images/delete.svg"></div>' +
    '            </div>' +
    '</div>' +
    '</div>';


Vue.component('temp', {
    template: temp,
    props: {
        images: {
            type: Array,
            required: true
        }
    },
    data: function () {
        return {}

    },
    methods: {
        newFile: function (e) {
            var self = this;
            utils.readURL(e.target, function (src, file) {
                var img = {src: src, file: file, uploading: true};
                img.uploading = true;
                //Needs to have the property 'remote Id' in order for Vuelidate to detect changes on it afterwards
                img.remoteId = "";
                self.images.push(img);


                ;
                utils.uploadPhoto(file, 'big_image', function (remoteId) {
                    console.log("on up", remoteId);
                    img.remoteId = remoteId;
                    img.uploading = false;
                })
                /*
                setTimeout(function () {
                    img.uploading = false;
                },2000) */
            })
        },
        removeImg: function (i) {
            this.images.splice(i, 1);
        }
    }

});


var app = new Vue({
    el: '#vue-app',
    data: {
        editing: true,
        readOnly: false,
        showApprovalButton: false,
        loading: false,
        initializing: false,
        currentImage: 0,
        winStart: 0,
        winEnd: 3,
        types : {
            TECHNOLOGY: TECHNOLOGY,
            TOOL: TOOL,
            TUTORIAL: TUTORIAL,
            EXAMPLE: EXAMPLE,
            STRATEGY: STRATEGY,
            DEVELOPMENT: DEVELOPMENT
        },
        typeName: typeName,



        item: {
            id: window.itemInfo.id,
            subclassId: '',
            type: window.itemInfo.type,
            version: window.itemInfo.version || 0,
            name: '',
            description: '',
            images: [],
            thumbnail: '',
            // TECNOLOGIA
            devTechs: [],
            // HERRAMIENTA
            technology: '',
            licenseType: '',
            useRestrictions: '',
            toolUrl: '',
            toolDownloadUrl: '',
            operativeSystems: [],
            integration: false,
            functionalDescription: '',
            //EJEMPLO
            strategy: '',
            tool: '',
            exampleUrl: '',
            //TUTORIAL
            tutorialUrl: ''



        },
        strategies: {},
        tools: {},
        technologies: {},  // tecnologias del catalogo eg. sicua o moodle
        devTechs: {}, //Technologias que se usan para un desarrollo, e.g angular, node etc.. No tiene que ver con el CATALOGO
        licenseTypes : {}
    },
    methods: {
        getClass: function (fieldName) {
            return {
                'is-invalid': this.$v.item[fieldName].$error,
                'is-valid': !this.$v.item[fieldName].$error && this.$v.item[fieldName].$dirty
            }
        },
        submit: function (sendToReview) {
            console.log("Data to be sent", this.item);
            if (this.$v.$invalid) {
                this.$v.item.$touch();
                console.log("Form con errores");
                return;
            }

            var self = this;

            self.loading = true;
            if (!self.item.id) {  // si el item no existe en la bd
                utils.uploadPhoto(self.item.images[0].file, 'thumbnail', function (remoteId) {
                    self.item.thumbnail = remoteId;
                    sendData();
                });
            } else {
                sendData();
            }

            function sendData() {
                var data = utils.sliceKey(self.item, 'images');

                data.sendToReview = sendToReview || '';
                //Les deja  solo el id a las tecnologias de desarrollo
                /*
                data.devTechs = data.devTechs.map(function (tech) {
                    return tech.id;
                }) */
                //Les deja solo el id a las imagenes
                data.images = self.item.images.map(function (img) {  /* filter(function (img) {
                    return !img.id; // Ignora las que tengan Id, por que ya estan en la db
                })*/
                    return img.remoteId;
                })


                console.log("Transformed", data);


                axios.post(URL_BASE + "/catalogo/addEstrategia/", data)
                    .then(function (res) {
                        console.log("Success", res);// return;
                        window.location.href = URL_BASE + '/catalogo/?type='+self.item.type+'&busqueda='+self.item.name;

                    })
                    .catch(function (err) {
                        console.log("Error", err);
                    })
                    .finally(function () {
                        self.loading = true;
                    })

            }
        },
        sendApproval: function () {
            var self = this;
            var data = {
                'item_code': self.item.id,
                'version':  self.item.version
            };
            console.log('sending aproval',data);
            this.loading = true;

            axios.post(URL_BASE + "/catalogo/aprobarRevision/", data)
                .then(function (res) {
                    window.location.href = URL_BASE + '/catalogo/?type='+self.item.type+'&busqueda='+self.item.name;
                    console.log("Success Aproval", res);
                })
                .catch(function (err) {
                    console.log("Error Aproval", err);
                })
                .finally(function () {
                    this.loading = false;
                })

        },
        test: function () {
            console.log("Sending to review", this.item)
            this.submit(true);


        },
        moveCarousel: function (i) {
            $('.carousel').carousel(i);
        },
        changeSlide: function (i) {
            console.log("previ", i);
            var length = this.item.images.length
            i = (length + (i % length)) % length; //

            console.log("next", i);


            var offset = 0;
            /* Slides the 4-images windows  :V */
            if (i > this.winEnd) {
                offset = i - this.winEnd; //Positive offset
            } else if (i < this.winStart) {
                offset = i - this.winStart; //Negative offset
            }

            this.winStart += offset;
            this.winEnd += offset;
            this.currentImage = i;
            console.log('s', this.winStart, 'e', this.winEnd, this.currentImage);


        },
        openGalleryModal: function () {
            document.getElementsByTagName('nav')[0].style.display = "none";
            document.getElementById('galleryModal').style.display = "block";
        },

        closeGalleryModal: function () {
            document.getElementsByTagName('nav')[0].style.display = "flex";
            document.getElementById('galleryModal').style.display = "none";
        },
        showPreview: function () {
            console.log("show PReview");
            this.editing = false;
        },
        showEditMode: function () {
            this.editing = true;
        },
        getItemLink: function (item_code,type) {
            return URL_BASE + '/catalogo/verItem/?type='+type+'&code='+item_code+'&ver=2';
        },

    },
    computed: {
        currentImages: function () {
            return this.item.images.slice(this.winStart, this.winEnd + 1);
        }
    },
    validations: function(){


                 var  val ={
                         item : {
                                    name: {
                                        required: validators.required,
                                        maxLength: validators.maxLength(20)
                                    },
                                    description: {
                                        required: validators.required,
                                        maxLength: validators.maxLength(300)

                                    }
                                    ,
                                    images: {
                                        required: validators.required,
                                        $each: {
                                            remoteId: {
                                                required: validators.required
                                            }
                                        }
                                    }

                        }
                 }

                 switch (this.item.type){
                     case DEVELOPMENT:
                         val.item.devTechs = { required: validators.required }
                     break;
                     case TOOL:
                         val.item.technology = { required: validators.required }
                         val.item.licenseType = { required: validators.required }
                         val.item.useRestrictions = {
                                        required: validators.required,
                                        maxLength: validators.maxLength(300)

                                    }
                         val.item.toolUrl = {
                             required: validators.required,
                             maxLength: validators.maxLength(300),
                             url: validators.url
                         }

                         val.item.toolDownloadUrl = {
                             required: validators.required,
                             maxLength: validators.maxLength(300),
                             url: validators.url
                         }

                         val.item.operativeSystems = { required: validators.required }

                         val.item.functionalDescription = {
                                        required: validators.required,
                                        maxLength: validators.maxLength(300)
                         }

                    break;
                     case EXAMPLE:
                         val.item.strategy = { required: validators.required }
                         val.item.tool = { required: validators.required }
                         val.item.exampleUrl = {
                             required: validators.required,
                             maxLength: validators.maxLength(300),
                             url: validators.url
                         }

                     break;
                     case TUTORIAL:
                         val.item.tool = { required: validators.required }
                         val.item.tutorialUrl = {
                             required: validators.required,
                             maxLength: validators.maxLength(300),
                             url: validators.url
                         }

                     break;




                 }

                 return val;



    },
    created: function () {




        if (this.item.version == 0) {  //Si es borrador
            this.readOnly = false;
            this.editing = true;
        } else if (this.item.version > 0) { //Si no es borrador
            this.readOnly = true;
            this.editing = false;
            if (this.item.version == 1) { //Si es revision
                this.showApprovalButton = true;
            }
        }


        var self = this;
        this.mockImages = [
            'https://www.w3schools.com/howto/img_lights_wide.jpg',
            'https://www.w3schools.com/howto/img_mountains_wide.jpg',
            'https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg?auto=compress&cs=tinysrgb&h=350',
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzabaX7ooQ-ZTzDiT8RuvgsC94g7lcnpbpzLUvwu9smM7THIMc5g',
            'http://apclandscape.us.com/wp-content/themes/land3/images/sliders/slide1.jpg',
            'http://images.nationalgeographic.com.es/medio/2015/12/21/bf63ef82rio_narcea_tineo_720x480.jpg'

        ]

        loadLists(this);
        if(this.item.id > 0)
            fetchItem(self); //Solo se trae para editar


    },
    mounted: function () {


        var self = this;
        $('.carousel').on('slide.bs.carousel', function (e) {
            var slideFrom = $(this).find('.active').index();
            var slideTo = $(e.relatedTarget).index();
            console.log(slideFrom + ' => ' + slideTo);
            self.changeSlide(slideTo);
        });
    }

})

/** Trae el item de la db para ver o editar*/
function fetchItem(self) {
    self.initializing = true;
    axios.get(URL_BASE + "/catalogo/item/", {
        params: {
            id: window.itemInfo.id,
            type: window.itemInfo.type,
            version: window.itemInfo.version,
        }
    })
        .then(function (res) {
            self.initializing = false;
            console.log("All", res.data);
            var images = JSON.parse(res.data.images);
            var item = JSON.parse(res.data.item);
            if (item.length == 0) {
                console.log("No se encontro el item");
                return
            }

            console.log("Images", images);
            console.log("Data", item[0]);
            var data = item[0];
            self.item.name = data.fields.name;
            self.item.description = data.fields.description;
            self.item.thumbnail = data.fields.thumbnail;

            self.item.images = images.map(function (img) {
                img.src = IMG_BASE + img.remoteId;
                return img;
            })

            cargarInfo(self, res, data);

        })


}

/** Carga info especifica del item que se va a ver/editar*/
function cargarInfo(self, res, data) {

    var subItem = null;
    if(res.data.subItem){
        subItem = JSON.parse(res.data.subItem);
        subItem = subItem[0];
    }

    console.log("Subitem",subItem);


    switch (self.item.type) {
        case DEVELOPMENT: //Carga tecnologias de desarrollo
            self.item.subclassId = data.fields.development;
            var techs = JSON.parse(res.data.techs);
            console.log("Techs del item", techs);
            self.item.devTechs = techs.map(function (value) {
                return value.pk;
            })
        break;
        case TOOL:
            self.item.technology = subItem.fields.technology;
            self.item.licenseType = subItem.fields.license_type;
            self.item.useRestrictions = subItem.fields.use_restrictions;
            self.item.toolUrl = subItem.fields.url;
            self.item.toolDownloadUrl = subItem.fields.download_url;
            self.item.integration = subItem.fields.integration;
            self.item.functionalDescription = subItem.fields.functional_description;
            self.item.operativeSystems = subItem.fields.operating_systems.split(',');

        break;
        case EXAMPLE:
            self.item.strategy = subItem.fields.strategy;
            self.item.tool = subItem.fields.tool;
            self.item.exampleUrl = subItem.fields.url;
        break;
        case TUTORIAL:
            self.item.tool = subItem.fields.tool;
            self.item.tutorialUrl = subItem.fields.url;
        break;
    }


}

/** Carga las listas necesarias para el tipo de item que se esta creando o editando*/
function loadLists(self) {
    self.initializing = true;
    switch (self.item.type) {

        case DEVELOPMENT:
            axios.get(URL_BASE + "/catalogo/devTech/")
                .then(function (res) {
                    res.data.map(function (entry) {
                        var fields = entry.fields;
                        fields.image = IMG_BASE + fields.image;
                        self.$set(self.devTechs,entry.pk,fields);// devTechs[] = fields;
                    });
                    self.initializing = false;
                    //self.vm.$set('devTechs', self.devTechs);
                    console.log("DEvTechs", self.devTechs);
                })
        break;
        case TOOL:

            axios.get(URL_BASE + "/catalogo/technologies/")
                .then(function (res) {
                    res.data.map(function (entry) {
                        var fields = entry.fields;
                        //fields.image = IMG_BASE + fields.image;
                        self.$set(self.technologies, entry.pk, fields);// devTechs[] = fields;
                    });
                    self.initializing = false;
                    console.log("Tecnologias", self.technologies);
            })


            self.licenseTypes = [
                "Licencia de Software Libre",
                "Licencia de Dominio Público",
                "Licencia de Software Comercial",
                "Licencia Freeware",
                "Licencia de Software Propietario",

            ]
            self.operativeSystems = {
                "1": { name : "Windows" , img : ""},
                "2": { name : "Linux" , img : ""},
                "3": { name : "macOS" , img : ""}
            }


        break;
        case EXAMPLE:



            axios.get(URL_BASE + "/catalogo/tools/")
                .then(function (res) {
                    res.data.map(function (entry) {
                        var fields = entry.fields;
                        fields.item= entry.pk;
                        self.$set(self.tools, fields.tool, fields);// devTechs[] = fields;
                    });
                    console.log("Tools", self.tools);
            })

            axios.get(URL_BASE + "/catalogo/strategies/")
                .then(function (res) {
                    console.log("Purestra",res.data);
                    res.data.map(function (entry) {
                        var fields = entry.fields;
                        fields.item= entry.pk;

                        self.$set(self.strategies, fields.strategy, fields);// devTechs[] = fields;
                    });
                    self.initializing = false;
                    console.log("Strategies", self.strategies);
            })

        break;
        case TUTORIAL:
            axios.get(URL_BASE + "/catalogo/tools/")
                .then(function (res) {
                    res.data.map(function (entry) {
                        var fields = entry.fields;
                        fields.item= entry.pk;
                        self.$set(self.tools, fields.tool, fields);// devTechs[] = fields;
                    });
                    self.initializing  = false;
                    console.log("Tools", self.tools);
            })
        break;
        case STRATEGY:
            self.initializing = false;
            break;







    }

}

