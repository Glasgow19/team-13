function convertToJSONForm(x){
   var answer = document.getElementById(x).value;
   return  x + ": " + "\"" + answer + "\"";
}

function multipleToJSONForm(x){ 
    var selected = document.getElementById(x);
    let all = selected && selected.options;
    var collection = [];

    var count;
    for (count = 0; count < all.length; count++) {
        if (all[count].selected) {
            collection.push(all[count].value);
        }
    }

    var answer = "[\"";
    var i;
    for (i = 0; i < collection.length; i++) {
        if (collection.length == 1) {
            return  x + ": " + "\"" + collection[i] + "\""; 
        }

        answer += collection[i] + "\"";
        
        if (i < collection.length - 1) {
            answer += ", ";
        }
    }
    return x + ": " + answer + "]";
}

function convertToJSON(){
    var allElements = document.getElementsByTagName("*");
    var allIds = [];
    var i;
    for (i = 0, n = allElements.length; i < n; ++i) {
        var el = allElements[i];
        if (el.id) { allIds.push(el.id); }
    }
    
    var json = "{ ";
    
    var list;
    for (list = 0; list < allIds.length; list++) {
        if (allIds[list] == "sports") {
            json += multipleToJSONForm("sports");
            json += ", ";
            // continue;
        }

        json += convertToJSONForm(allIds[list]);

        if (list < allIds.length - 1) {
            json += ", "
        }
    }

    json += "}";
    console.log(json);

    return JSON.stringify(json);
}