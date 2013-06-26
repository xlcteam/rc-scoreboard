$(document).ready(function () {
    
    var mapID = $_GET['id'];

    var map = $("#map");
    // Skapar userinterface
    $('<h1>Create Rescue B map</h1>').appendTo(map);
    var name=$('<input type="text" id="name">').appendTo(map);
    name.before('<label for="name">Name: </label>');
    var save=$('<input type="button" value="Save!">').click(function(){
        var json = {"action": "saveMaze", "mapID": mapID, "name": name.val(), "walls": {}, "squares": {}};
        
        // Iterate through walls and save them, and also every victims etc. 
        $("td.border").each(function(i){
            if($(this).hasClass('wall'))
                json.walls[i] = true;
        });
        $("td.square").each(function(i){
            // If there is /any/ data, we need to create the square
            if($(this).hasClass('victim') || $(this).children('.start').length == 1 || $(this).hasClass('black-tile')){
                json.squares[i] = {};
                
                if($(this).hasClass('victim'))
                    json.squares[i].victim = true;
                if($(this).children('.start').length == 1)
                    json.squares[i].start = true;
                if($(this).hasClass('black-tile'))
                    json.squares[i].black = true;
            }
        });
        $.ajax({
            type: "POST",
            url: MAP_SAVE_URL,
            data: {"json": JSON.stringify(json)},
            dataType: "json",
            success: function(data){alert("The map is now saved!"); mapID = data;},
            error: function(obj,errMsg){alert("Error when saving map: " + errMsg);}
        });
    }).appendTo(map).after('<br>');
    /*
    // Ask the server for field details!
    $.ajax({
        type: "POST",
        url: "mapgen.php",
        data: {"json": JSON.stringify({"mapID": mapID, "action": "getField"})},
        dataType: "json",
        success: function(data){*/
            var lowerHeight = 10;//data.lowerHeight;
            var upperHeight = 3;//data.upperHeight;
            var lowerRamp = 7;//data.lowerRamp;
            var upperRamp = 3;//data.upperRamp;
            var left = true;//data.left;

            // creates an empty arena with a table
            var field = $('<table></table>').addClass('field').appendTo(map);
            if(left)
                var horizontalBorders = '<tr><td class="empty ramp"></td><td class="empty ramp"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td></tr>';
            else
                var horizontalBorders = '<tr><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="border"></td><td class="empty"></td><td class="empty ramp"></td><td class="empty ramp"></td></tr>';
            
            for(var h=0; h<lowerHeight; h++)
            {
                // Create a row of borders
                var row = $(horizontalBorders).appendTo(field);
                if(h==0)
                    row.children('.border').removeClass('border').addClass('wall');
                if(h == lowerRamp-1)
                    row.children('.ramp').addClass('wall');
                
                
                var row = $('<tr></tr>').appendTo(field);
                for(var b=0; b<4;b++)
                {
                    if(b==0 && (!left || h!=lowerRamp-1))
                        $('<td class="wall"></td>').appendTo(row);
                    else
                        $('<td class="border"></td>').appendTo(row);
                    
                    $('<td class="square"></td>').appendTo(row);
                }
                // Create the rightmost wall
                $('<td class="'+((left || h!=lowerRamp-1)?'wall':'')+'"></td>').appendTo(row);
                
                // If we also should draw the ramp area
                if(h >= lowerRamp-1)
                {
                    if(left)
                $('<td class="wall ramp"></td><td class="square ramp"></td>').prependTo(row);
                    else
                        $('<td class="square ramp"></td><td class="wall ramp"></td>').appendTo(row);
                }else{
                    if(left)
                        $('<td class="empty ramp"></td><td class="empty ramp"></td>').prependTo(row);
                    else
                        $('<td class="empty ramp"></td><td class="empty ramp"></td>').appendTo(row);
                    
                }
                
                
            }
            // Create the last boundary of the lower floor
            var row = $(horizontalBorders).appendTo(field);
            row.children('.border').removeClass('border').addClass('wall');
            
            // Draw one empty row with just the ramp
            if(left)
                $('<tr><td class="wall ramp"></td><td class="square ramp"></td><td class="wall ramp"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td></tr>').appendTo(field);
            else
                $('<tr><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="empty"></td><td class="wall ramp"></td><td class="square ramp"></td><td class="wall ramp"></td></tr>').appendTo(field);
            
            
            
            
            for(var h=0; h<upperHeight; h++)
            {
                // Create a row of borders
                var row = $(horizontalBorders).appendTo(field);
                if(h==0)
                    row.children('.border').removeClass('border').addClass('wall');
                if(h == upperRamp)
                    row.children('.ramp').addClass('wall');
                
                
                var row = $('<tr></tr>').appendTo(field);
                for(var b=0; b<4;b++)
                {
                    if(b==0 && (!left || h!=upperRamp-1))
                        $('<td class="wall"></td>').appendTo(row);
                    else
                        $('<td class="border"></td>').appendTo(row);
                    $('<td class="square"></td>').appendTo(row);
                }
                // Create the rightmost wall
                $('<td class="'+((left || h!=upperRamp-1)?'wall':'')+'"></td>').appendTo(row);
                
                // If we also should draw the ramp area
                if(h <= upperRamp-1)
                {
                    if(left)
                        $('<td class="wall ramp"></td><td class="square ramp"></td>').prependTo(row);
                    else
                        $('<td class="square ramp"></td><td class="wall ramp"></td>').appendTo(row);
                }else{
                    if(left)
                        $('<td class="empty ramp"></td><td class="empty ramp"></td>').prependTo(row);
                    else
                        $('<td class="empty ramp"></td><td class="empty ramp"></td>').appendTo(row);
                    
                }
                
                
            }
            // Create the last boundary of the upper floor
            var row = $(horizontalBorders).appendTo(field);
            row.children('.border').removeClass('border').addClass('wall');
            if(upperRamp == upperHeight)
                row.children('.ramp').addClass('wall');
            
            
            $('.border').click(function(){
                $(this).toggleClass("wall");    
            });
            
            $('.square').click(function(){
                if($(this).hasClass('black-tile')){
                    $(this).removeClass('black-tile');
                }else if($(this).hasClass('victim')){
                    $(this).addClass('black-tile').removeClass('victim').children('.victim').remove();;
                }else{
                    var x = e.pageX - this.offsetLeft - 8;
                    var y = e.pageY - this.offsetTop - 113;
                    if(plusminus(y, 25, 10) && plusminus(x, 10, 10)) {
                    	$(this).addClass('victim').append('<img src="' + IMG_DIR + 'img/rescueB/victim0.png" class="victim">'); // left
                    }
                    else if(plusminus(y, 25, 10) && plusminus(x, 40, 10)) {
                    	$(this).addClass('victim').append('<img src="' + IMG_DIR + 'img/rescueB/victim2.png" class="victim">'); // right
                    }
                    else if(plusminus(y, 5, 5) && plusminus(x, 25, 10)) {
                    	$(this).addClass('victim').append('<img src="' + IMG_DIR + 'img/rescueB/victim3.png" class="victim">'); // top
                    }
                    else if(plusminus(y, 45, 5) && plusminus(x, 25, 10)) {
                    	$(this).addClass('victim').append('<img src="' + IMG_DIR + 'img/rescueB/victim1.png" class="victim">'); // bottom
                    }              
                }
            }).contextmenu(function(){
                $('.start').remove();
                $(this).append('<img src="' + IMG_DIR + 'img/rescueB/start.png" class="start">');
                return false;
            });
            
            
            
            // If we are loading a map
            if(mapID>0) // This is only executed during initiating, and it is okay to change the mapID when saving a newly created map
            {
                alert("Loading map!!");
                // Ask the server for maze data!
                $.ajax({
                    type: "POST",
                    url: MAP_SAVE_URL,
                    data: {"json": JSON.stringify({"mapID": mapID, "action": "getMaze"})},
                    dataType: "json",
                    success: function(data){
                        name.val(data.name);
                        // Iterate through walls and load walls
                        $("td.border").each(function(i){
                            if(data.walls[i])
                                $(this).addClass('wall');
                        });
                        // Iterate through squares and load data
                        $("td.square").each(function(i){
                            // If the square exists (contains any data at all)
                            if(data.squares[i]){
                                if(data.squares[i].victim){
                                    $(this).addClass('victim').append('<img src="' + IMG_DIR + 'img/rescueB/victim'+Math.floor(1+Math.random()*3)+'.png" class="victim">');
                                }else if(data.squares[i].black){
                                    $(this).addClass('black-tile');
                                }
                                if(data.squares[i].start){
                                    $(this).append('<img src="' + IMG_DIR + 'img/rescueB/start.png" class="start">');
                                }
                            }
                        });
                
                    },
                    error: function(obj,errMsg){alert("Error while fetching maze: " + errMsg);}
                });
            }
            
       /* },
        error: function(obj,errMsg){alert("Error while fetching field: " + errMsg);}
    });*/
});

// checks a value lies within +- of target value
function plusminus(val, comp, pad) {
	return (val >= (comp - pad) && val <= (comp + pad));	
}
