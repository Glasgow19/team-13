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
    var json = "{ " + convertToJSONForm("worktimefrom") + ", " + convertToJSONForm("worktimeto") + ", " + multipleToJSONForm("sports")
                    + ", " + convertToJSONForm("injury") + ", " + convertToJSONForm("competition") + "}";
    
    console.log(json);
    return JSON.stringify(json);
}