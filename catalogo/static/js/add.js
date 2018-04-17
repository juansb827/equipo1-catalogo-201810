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
                img.uploading = true;
                //Needs to have the property 'remote Id' in order for Vuelidate to detect changes on it afterwards
                img.remoteId = "";
                self.images.push(img);


                ;
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
        editing: true,
        currentImage: 0,
        winStart: 0,
        winEnd: 3,
        item:{
            type: '6',
            name: 'Desarrollo 20',
            description: 'Integer tincidunt ante vel ante blandit, nec pharetra risus pulvinar. Quisque tellus velit, lobortis non quam ac, eleifend volutpat dolor. Duis at pellentesque sem, ut viverra arcu. Praesent euismod lacinia nisl, sit amet auctor urna posuere eget. ',
            devTechs: [],
            images: [],

            thumbnail: ''
        },
        devTechs: [] //Technologias que se usan para un desarrollo, e.g angular, node etc.. No tiene que ver con el CATALOGO
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


                //Les deja  solo el id a las tecnologias de desarrollo
                data.devTechs = data.devTechs.map(function (tech) {
                    return tech.id;
                })
                //Les deja solo el id a las imagenes
                data.images = self.item.images.map(function (img) {
                    return img.remoteId;
                })



                console.log("Transformed",data);

                axios.post(URL_BASE + "/catalogo/addEstrategia/", data)
                    .then(function (res) {
                        console.log("Success", res);
                    })
                    .catch(function (err) {
                        console.log("Error", err);
                    })
                    .finally(function () {

                    })
            });
        },
        moveCarousel: function(i){
			$('.carousel').carousel(i);
		},
        changeSlide: function (i) {
			console.log("previ",i);
			var length = this.item.images.length
			i = ( length + (i % length ) ) % length; //

			console.log("next",i);




            var offset=0;
            /* Slides the 4-images windows  :V */
            if( i > this.winEnd  ){
                offset = i - this.winEnd; //Positive offset
            }else if( i < this.winStart){
                offset = i -this.winStart; //Negative offset
            }

            this.winStart += offset;
            this.winEnd += offset;
            this.currentImage = i;
            console.log('s',this.winStart,'e',this.winEnd,this.currentImage);



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
        }

    },
    computed: {
        currentImages: function(){
            return this.item.images.slice(this.winStart,this.winEnd+1);
        }
    },
    validations:{
        item:{
            name: {
                required: validators.required,
                maxLength: validators.maxLength(20)
            },
            description: {
                required: validators.required,
                maxLength: validators.maxLength(300)

            },
            devTechs: {
                required: validators.required
            },
            images: {
                required: validators.required,
                $each: {
                    remoteId: {
                        required: validators.required
                    }
                }
            }
        }
    },
    created: function () {
        //this.loadDevTechs();

        var self = this;
        this.mockImages = [
            'https://www.w3schools.com/howto/img_lights_wide.jpg',
            'https://www.w3schools.com/howto/img_mountains_wide.jpg',
            'https://images.pexels.com/photos/39811/pexels-photo-39811.jpeg?auto=compress&cs=tinysrgb&h=350',
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzabaX7ooQ-ZTzDiT8RuvgsC94g7lcnpbpzLUvwu9smM7THIMc5g',
            'http://apclandscape.us.com/wp-content/themes/land3/images/sliders/slide1.jpg',
            'http://images.nationalgeographic.com.es/medio/2015/12/21/bf63ef82rio_narcea_tineo_720x480.jpg'

        ]

            axios.get(URL_BASE + "/catalogo/devTech/")
                .then(function (res) {
                    self.devTechs = res.data.map(function (entry) {
                        var fields = entry.fields;
                        fields.id = entry.pk;
                        fields.image = 'https://res.cloudinary.com/hn6nvsi2y/' + fields.image;
                        return fields;
                    });
                    console.log("DEvTEchs",self.devTechs);
                })

    },
    mounted: function(){
		var self = this;
		$('.carousel').on('slide.bs.carousel',function(e){
			var slideFrom = $(this).find('.active').index();
			var slideTo = $(e.relatedTarget).index();
			console.log(slideFrom+' => '+slideTo);
			self.changeSlide(slideTo);
		});
	}

})



