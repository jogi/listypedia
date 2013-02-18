function isValidURL(url){
    var RegExp = /(www|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;

    if(RegExp.test(url)){
        return true;
    }else{
        return false;
    }
}

function parselink(event){
    url = event.target.value;
    valid = isValidURL(url);

    if(valid){
        $.get('/pageinfo/?u=' + url, function(data) {
            $('input#name').val(data.title);
        });
    }
}