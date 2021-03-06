window.URL_BASE = window.location.origin;

utils = {
    readURL: function (input, cb) {

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                cb(e.target.result, input.files[0]);
            };

            reader.readAsDataURL(input.files[0]);
        }

    },
    uploadPhoto: function (file, preset, cloudinaryName, cb) {
        this.send(file, preset, cloudinaryName, function (data) {
            var res = JSON.parse(data.target.response);
            var imgPath = res.public_id;
            cb(imgPath);
        });
    },
    send: function (file, preset, cloudinaryName, cb) {
        var formData = new FormData();
        formData.append('upload_preset', preset);
        formData.append('file', file);
        var xhr = new XMLHttpRequest();
        xhr.onload = cb;

        xhr.addEventListener("progress", function (evt) {
            if (evt.lengthComputable) {
                var percentage = (evt.loaded / evt.total) * 100;
            }
        }, false);


        xhr.open("post", "https://api.cloudinary.com/v1_1/" + cloudinaryName + "/image/upload");

        xhr.send(formData);

    }

};

utils.sliceKey = function (object, key) {
    var ob = {};
    Object.keys(object)
        .filter(function (keyName) {
            return keyName !== key;
        })
        .forEach(function (key) {
            ob[key] = object[key];
        });
    return ob;
};

utils.getParameterByName = function (name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

utils.addUrlParam = function (search, key, val) {
    var newParam = key + '=' + val,
        params = '?' + newParam;

    // If the "search" string exists, then build params from it
    if (search) {
        // Try to replace an existance instance
        params = search.replace(new RegExp('([?&])' + key + '[^&]*'), '$1' + newParam);

        // If nothing was replaced, then add the new param to the end
        if (params === search) {
            params += '&' + newParam;
        }
    }

    return params;
};

/**
 *
 */

utils.getImageUrl = function (cloudinaryName, imageId) {
    return 'https://res.cloudinary.com/' + cloudinaryName + '/' + imageId;
};

utils.getItemLink = function (item_code, type) {
            return URL_BASE + '/catalogo/verItem/?type=' + type + '&code=' + item_code + '&ver=2';
}


window.utils = utils;









