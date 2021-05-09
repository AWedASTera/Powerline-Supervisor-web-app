$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('update_page', async function() {
        //maintain a list of ten numbers
        console.log(0);
        let response = await fetch('http://' + document.domain + ':' + location.port + '/todo/api/v1.0/pillars');
        let pillars = await response.json(); //extract JSON from the http response   
        console.log(pillars);    
        pillars_string = '';
        for (var i = 0; i < pillars.pillars.length; i++){
            pillars_string = pillars_string + '<div class="container">' + '<hr class="my-4">' + (pillars.pillars[i][3] ? '<h1 class="display-7" >' + pillars.pillars[i][0] :'<h1 class="display-7 text-danger" >' + pillars.pillars[i][0]) + '</h1>' + '<p class="lead">' + pillars.pillars[i][1] + '</p>' + '<p class="lead">' + pillars.pillars[i][2] + '</p>' + '<button type="button" class="btn btn-secondary btn-sm "  onclick="sendDelete(event, ' + pillars.pillars[i][0] + ')" >Delete</button><hr class="my-4"></div>'
        }
        $('#log').html(pillars_string);
    });

});
function sendDelete(event,number){
    var xhttp = new XMLHttpRequest();
    console.log(1);
    event.preventDefault();
    console.log(2);
    xhttp.open("DELETE", '/todo/api/v1.0/pillars/' + number, true);
    console.log(number);
    console.log(3);
    xhttp.send();
};