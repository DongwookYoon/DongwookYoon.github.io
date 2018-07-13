/**
 * Created by ukka123 on 6/26/18.
 */

function loadBody(){
    function traverse (x) {
        if (isArray(x)) {
            traverseArray(x)
        } else if ((typeof x === 'object') && (x !== null)) {
            traverseObject(x)
        }
    }
    function traverseArray (arr) {
        arr.forEach(function (x) {
            x.last=false;
            traverse(x)
        });
        if(arr.length>0)
            arr[arr.length-1].last = true;
    }
    function traverseObject (obj) {
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                traverse(obj[key])
            }
        }
    }
    function isArray (o) {
        return Object.prototype.toString.call(o) === '[object Array]'
    }
    $.get('files/data.json', function(data) {
        $.get('body_template.html', function(body_template) {
            traverse(data);
            for(let i = 0; i < data['publications'].length; ++i){
                data['publications'][i]['no'] = data['publications'].length - i;
            }
            $('body').html(Mustache.render(body_template, data));
        })
    });
       
}