var URL_BASE = window.location.origin;


Vue.use(window.vuelidate.default)

var temp =
    '<div>'+
        '<span class="btn btn-success fileinput-button">' +
        '            <i class="glyphicon glyphicon-plus"></i>' +
        '            <span>Agregar imagen...</span>' +
        '            <input id="imgInp" type="file" class="upload-button" v-on:change="newFile">' +
        '</span>'+
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
        '</div>'+
     '</div>'   ;



Vue.component('temp', {
    template: temp,
    props: {
      images: {
        type: Array,
        required: true
      }
    },
    data: function() {
        return {

        }

    },
    methods:{
        newFile : function (e) {
            var self = this;
            utils.readURL(e.target, function (src,file) {
                var img = { src: src, file: file, uploading: true };
                self.images.push(img);
                utils.uploadPhoto(file, 'big_image', function (remoteId) {
                    console.log("on up",remoteId);
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
            this.images.splice(i,1);
        }
    }

});





var app= new Vue({
    el: '#vue-app',
    data: {
        item:{
            type: '5',
            name: '',
            description: '',
            images: [],
            thumbnail: ''
        }
    },
    methods: {
        getClass : function (fieldName) {
            return { 'is-invalid' : this.$v.item[fieldName].$error,
                     'is-valid' : !this.$v.item[fieldName].$error && this.$v.item[fieldName].$dirty  }
        },
        submit: function () {
            console.log("Data to be sent", this.item);
            if(this.$v.$invalid) {
                this.$v.item.$touch();
                console.log("Form con errores");
                return;
            }
            var self = this;
            utils.uploadPhoto(self.item.images[0].file, 'thumbnail',function (remoteId) {
                self.item.thumbnail = remoteId;

                var data = utils.sliceKey(self.item,'images');


                //Les deja solo el id a las imagenes
                data.images = self.item.images.map(function (img) {
                    return img.remoteId;
                })

                console.log("Transformed", data);

                axios.post(URL_BASE + "/catalogo/addEstrategia/", data)
                    .then(function (res) {
                        console.log("Success", err);
                    })
                    .catch(function (err) {
                        console.log("Error", err);
                    })
                    .finally(function () {

                    })
            });
        }
    },
    validations:{
        item:{
            name: {
                required: validators.required,
                maxLength: validators.maxLength(10)
            },
            description: {
                required: validators.required,
                maxLength: validators.maxLength(10)

            },
            images: {
                required: validators.required
            }
        }
    }

})
