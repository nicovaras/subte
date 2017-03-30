function callAjax(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.responseText);
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

function check_status(text, arr){
    for(var i = 0; i < arr.length; i++){
        if (text.indexOf(arr[i]) > -1){
            return true;
        }
    }
    return false;
}

function get_status(callback) {
    callAjax("http://subte-data.null.com.ar", function(json){
        callback(JSON.parse(json));
    })
}
