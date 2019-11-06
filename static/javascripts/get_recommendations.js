// static/javascript/get_recommendations.js

// this script should inject an html card for each drink recommended by the server
$(document).ready(function(){
    $.post('/recommendations/get', function(data){
        console.log(data)
    })
});