utils = {
        readURL: function(input,cb) {

            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    cb( e.target.result, input.files[0]);
                }

                reader.readAsDataURL(input.files[0]);
            }

        },
        uploadPhoto: function (file, preset, cb) {
                send(file, preset, function (data) {
                    var res = JSON.parse(data.target.response);
                    var imgPath = res.public_id;
                    cb(imgPath);
                });
        },
        send: function (file, preset, cb) {
            var formData = new FormData();
            formData.append('upload_preset', preset);
            formData.append('file', file);
            var xhr = new XMLHttpRequest();
            xhr.onload = cb;

            xhr.addEventListener("progress", function (evt) {
                console.log("progress", evt);
                if (evt.lengthComputable) {
                    var percentage = (evt.loaded / evt.total) * 100;
                    console.log("pro", percentage);
                }
            }, false)


            xhr.open("post", "https://api.cloudinary.com/v1_1/hn6nvsi2y/image/upload");

            xhr.send(formData);

        },

}

utils.sliceKey = function(object, key){
            var ob = {};
            Object.keys(object)
                .filter(function (keyName) {
                    return keyName != key;
                })
                .forEach(function (key) {
                    ob[key] = object[key];
                })
            return ob;
}




window.utils = utils;









