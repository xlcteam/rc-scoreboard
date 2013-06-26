$(document).ready(function () {
    // If it is a mobile browser except an iPhone or other i-device
    var mobile = ('ontouchstart' in document.documentElement) && !(navigator.userAgent.match(/(iPad|iPhone|iPod)/g) ? true : false );
    
    var runid = $_GET['id'];
        
    var map = $("#map");
    var info = $("<div></div>").prependTo(map);    
    $('<h1 id="title"></h1>').appendTo(info);

    var timetitle = $('<h2></h2>').appendTo(info);

    $('<span id="time">00:00</span>').appendTo(timetitle);

    var running;    
    $('<button type="button">Start the timer</button>').click(function(){

        if($(this).text() == "Start the timer"){
            running = true;
            var curr = $('#time');
            var json = {"action": "startTime", "currentValue": curr.text(), "started": (new Date()).valueOf() }
//            var offset = new Date(0,0,0,0,parseInt(curr.text().split(':')[0]),parseInt(curr.text().split(':')[1]),0);
            

            // Fix offset
            json.started += 1000*(parseInt(curr.text().split(':')[0])*60 + parseInt(curr.text().split(':')[1]));

            // Change the text of the button
            $(this).text('Stop the timer');
            
            (function tick(){
                $(this).val(new Date());
                var sec = Math.floor((new Date() - json.started)/1000);
                console.log((new Date()).valueOf(), json.started.valueOf());
                console.log(json.started);
                console.log(sec);
                var min = Math.floor(sec/60);
                sec -= min*60;
                curr.text((min<=9?'0':'') + min + ':' + (sec<=9?'0':'') + sec);
                console.log(running);
                if(running)
                    setTimeout(tick, 1000);
            })();
            
            
        }else{
            running = false;
            console.log("S: "  +running);
            // Change the text of the button
            $(this).text('Start the timer');
            var json = {"action": "stopTime", "currentValue": $('#time').text()}
        }
        
        console.log(json);
        $.ajax({
            type: "POST",
            url: "scoring.php",
            data: {"json": JSON.stringify(json)},
            dataType: "json",
            success: function(data){
                if(data=="forbidden"){
                    alert("You're not logged in anymore!");
                }
            },
            error: function(obj,errMsg){alert("Could not save: " + errMsg);}
        });        
    }).appendTo(timetitle);

    

    var info = $("<div></div>").attr('id','confirmation').appendTo(map);
    // Adds the verified time
    $('<strong>Verified time: </strong><br>').appendTo(info);
    $('<label for="min">Minutes: </label><input id="min" type="number" min="0" max="8"><br>').appendTo(info);
    $('<label for="sec">Seconds: </label><input id="sec" type="number" min="0" max="60"><br>').appendTo(info);
    // Add a sign/confirm button
    $('<button type="button">Sign!</button>').click(function(){
        $.ajax({
            type: "POST",
            url: SCORING_SAVE_URL,
            data: {"json": JSON.stringify({"action":"sign", "runID": runid, "sec":$('#sec').val(), "min":$('#min').val(), "score": $('#'+runid+'_poang').text()})},
            dataType: "json",
            success: function(data){
                // Skriver ut success-meddelande
                alert(data);
            },
            error: function(obj,errMsg){alert("Could not sign: " + errMsg);}
        });
        
        return false;
    }).appendTo(info);
    $('<br><strong>By clicking the "Sign!" button, you accept that the score (<span id="'+runid+'_poang"></span>) and time assigned above are correct.<br>Your team also further undertakes to not appeal the score at a later stage.</strong>').appendTo(info);
    


    // Loop through table and add indexes to the squares 
    $('.location').attr('id',function(index,attr){return index;});
    
    
    
    // Ask the server for tiles!
    $.ajax({
        type: "POST",
        url: SCORING_SAVE_URL,
        data: {"json": JSON.stringify({"runID": runid, "action": "getTiles"})},
        dataType: "json",
        success: function(data){ 
            $('#title').text(data.teamName + ' runs ' + data.roundName);
            $('#' + runid + '_poang').text(data.score);
            //console.log(data.tiles);


            $.each(data.tiles, function(index, tileData){
                var tile = $('<span></span>').addClass('tile').data('gap',tileData.gap).data('speedbump',tileData.speedbump).data('obstacle',tileData.obstacle).data('intersection',tileData.intersection).appendTo('#'+index);
                
                $('<img src="'+tileData.src+'">').addClass('path').appendTo(tile).rotTo(tileData.angle);// rotTo is impossible to chain

                var totaltAntal = +tileData.gap + +tileData.speedbump + +tileData.obstacle + +tileData.intersection;
                var tilePoints = {"action":"saveTile", "tileID":tileData.id, "runID":runid};
                
                var antal = +(tileData.scoredGap||0) + +(tileData.scoredSpeedbump||0) + +(tileData.scoredObstacle||0) + +(tileData.scoredIntersection||0);
                
                if(totaltAntal>0 && antal==totaltAntal)
                    var status = $('<img src="'+ IMG_URL +'img/rescueA/done.png">').appendTo(tile);
                else if(antal>0)
                    var status = $('<img src="'+ IMG_URL +'img/rescueA/halfdone.png">').appendTo(tile);
                else if(totaltAntal>0)
                    var status = $('<img src="'+ IMG_URL +'img/rescueA/undone.png">').appendTo(tile);
                
                // Creates a select list or dialog modal for each tile
                if(mobile)
                    var poangval = $('<select name="'+tileData.id+'"></select>').attr('multiple','multiple').change(function(){
                        tilePoints.gaps = [];
                        tilePoints.speedbumps = [];
                        tilePoints.obstacles = [];
                        tilePoints.intersections = [];
                        var antal=0;                       
                        
                        poangval.find("option").each(function(){
                            var tmp = $(this).val().split(" ");
                            switch(tmp[0])
                            {
                            case "Gap":
                                tilePoints.gaps[tmp[1] - 1] = $(this).prop("selected");
                                break;
                            case "Speedbump":
                                tilePoints.speedbumps[tmp[1] - 1] = $(this).prop("selected");
                                break;
                            case "Obstacle":
                                tilePoints.obstacles[tmp[1] - 1] = $(this).prop("selected");
                                break;
                            case "Intersection":
                                tilePoints.intersections[tmp[1] - 1] = $(this).prop("selected");
                                break;
                            }
 
                            if($(this).prop("selected"))
                                antal++;
                        });
                                                
                        if(antal==totaltAntal)
                            status.attr("src", IMG_URL + "img/rescueA/done.png");
                        else if(antal>0)
                            status.attr("src", IMG_URL + "img/rescueA/halfdone.png");
                        else
                            status.attr("src", IMG_URL + "img/rescueA/undone.png");
                        
                        save(tilePoints);
                    }).appendTo(tile);
                else
                    var poangval = $('<div title="Select points"></div>').css({'width':200});
                


                // Adds the alternatives
                for(var i = 1; i <= tileData.gap; i++){
                    if(mobile)
                        $('<option value="Gap '+i+'">Gap '+i+' (10p)</option>').prop("selected",i<=tileData.scoredGap).appendTo(poangval);
                    else
                        $('<input name="'+tileData.id+'" type="checkbox" value="Gap '+i+'">Gap '+i+' (10p)<br>').prop("checked",i<=tileData.scoredGap).appendTo(poangval);
                }
                for(var i = 1; i <= tileData.speedbump; i++){
                    if(mobile)
                        $('<option value="Speedbump '+i+'">Speedbump '+i+' (5p)</option>').prop("selected",i<=tileData.scoredSpeedbump).appendTo(poangval);
                    else
                        $('<input name="'+tileData.id+'" type="checkbox" value="Speedbump '+i+'">Speedbump '+i+' (5p)<br>').prop("checked",i<=tileData.scoredSpeedbump).appendTo(poangval);
                }
                for(var i = 1; i <= tileData.obstacle; i++){
                    if(mobile)
                        $('<option value="Obstacle '+i+'">Obstacle '+i+' (10p)</option>').prop("selected",i<=tileData.scoredObstacle).appendTo(poangval);
                    else
                        $('<input name="'+tileData.id+'" type="checkbox" value="Obstacle '+i+'">Obstacle '+i+' (10p)<br>').prop("checked",i<=tileData.scoredObstacle).appendTo(poangval);
                }
                for(var i = 1; i <= tileData.intersection; i++){
                    if(mobile)
                        $('<option value="Intersection '+i+'">Intersection '+i+' (10p)</option>').prop("selected",i<=tileData.scoredIntersection).appendTo(poangval);
                    else
                        $('<input name="'+tileData.id+'" type="checkbox" value="Intersection '+i+'">Intersection '+i+' (10p)<br>').prop("checked",i<=tileData.scoredIntersection).appendTo(poangval);
                }



                // If the judge clicks the tile
                tile.click(function(){
                    if(totaltAntal>1)
                    {
                        if (mobile)
                        {
                            var event;
                            event = document.createEvent('MouseEvents');
                            event.initMouseEvent('mousedown', true, true, window);
                            poangval[0].dispatchEvent(event);
                        }else{
                            poangval.dialog({
                                modal: true, 
                                draggable: false,
                                height: 300,
                                position: { my: "left top", at: "left top", of: tile },
                                buttons: [{ text: "OK", click: function() {
                                    tilePoints.gaps = [];
                                    tilePoints.speedbumps = [];
                                    tilePoints.obstacles = [];
                                    tilePoints.intersections = [];
                                   

                                    var antal = 0;
                                    // Iterate through the checkboxes and saves the checked ones
                                    poangval.find("input:checkbox").each(function(){
                                      
                                        
                                        var tmp = $(this).val().split(" ");
                                        switch(tmp[0])
                                        {
                                        case "Gap":
                                            tilePoints.gaps[tmp[1] - 1] = this.checked;
                                            break;
                                        case "Speedbump":
                                           tilePoints.speedbumps[tmp[1] - 1] = this.checked;
                                            break;
                                        case "Obstacle":
                                            tilePoints.obstacles[tmp[1] - 1] = this.checked;
                                            break;
                                        case "Intersection":
                                            tilePoints.intersections[tmp[1] - 1] = this.checked;
                                            break;
                                        }
                                        
                                        if(this.checked)
                                            antal++;
                                    });
                                    
                                    if(antal==totaltAntal)
                                        status.attr("src", IMG_URL + "img/rescueA/done.png");
                                    else if(antal>0)
                                        status.attr("src", IMG_URL + "img/rescueA/halfdone.png");
                                    else
                                        status.attr("src", IMG_URL + "img/rescueA/undone.png");
                                    save(tilePoints);
                                    $(this).dialog( "close" ); 
                                } } ] 
                           });
                        }
                    }else if(totaltAntal==1){
                        
                        // Toggle the src attribute
                        if(status.attr("src") == IMG_URL + "img/rescueA/done.png")
                            status.attr("src", IMG_URL + "img/rescueA/undone.png");
                        else
                            status.attr("src", IMG_URL + "img/rescueA/done.png");

                        var tmp = poangval.find("input, option").val().split(" ");
                        
                        switch(tmp[0])
                        {
                        case "Gap":
                            tilePoints.gaps = [];
                            tilePoints.gaps[0] = (status.attr("src") == IMG_URL + "img/rescueA/done.png");
                            break;
                        case "Speedbump":
                            tilePoints.speedbumps = [];
                            tilePoints.speedbumps[0] = (status.attr("src") == IMG_URL + "img/rescueA/done.png");
                            break;
                        case "Obstacle":
                            tilePoints.obstacles = [];
                            tilePoints.obstacles[0] = (status.attr("src") == IMG_URL + "img/rescueA/done.png");
                            break;
                        case "Intersection":
                            tilePoints.intersections = [];
                            tilePoints.intersections[0] = (status.attr("src") == IMG_URL + "img/rescueA/done.png");
                            break;
                        }
                        
                        save(tilePoints);
                    }
                    
                });

                // Display the various things existing at this tile
                if(tile.data("speedbump")>0)
                    $('<img src="'+ IMG_URL +'img/rescueA/speedbump.png">').appendTo(tile);
                if(tile.data("gap")>0)
                    $('<img src="'+ IMG_URL +'img/rescueA/gap.png">').appendTo(tile);
                if(tile.data("obstacle")>0)
                    $('<img src="'+ IMG_URL +'img/rescueA/obstacle.png">').appendTo(tile);
                if(tile.data("intersection")>0)
                    $('<img src="'+ IMG_URL +'img/rescueA/intersection.png">').appendTo(tile);
                
            });
        },
        error: function(obj,errMsg){alert("Error when fetching data: " + errMsg);}
    });
    
        
    
    
    
    // Ask for room points
    $.ajax({
        type: "POST",
        url: "scoring.php",
        data: {"json": JSON.stringify({"runID": runid, "action": "getModules"})},
        dataType: "json",
        success: function(modulesData){ 
            
            if(modulesData == "Unknown action")
                modulesData = {"first": {"passes":3,"LoPs":[0,1,0],"dones":[true,true,false]},
                               "second": {"passes":2,"LoPs":[1,3],"dones":[true,true]},
                               "ramp": {"passes":1,"LoPs":[0],"dones":[false]},
                               "outer": {"lifted": false,"passes":1,"LoPs":[2],"dones":[true]},
                               "hallway": {"passes":1,"LoPs":[0],"dones":[false]}};
  

            $.each(modulesData, function(moduleID, moduleData){
                var module = $('#'+moduleID);
                
                var passTable = $('<table></table>').appendTo(module);
                
                var passDones = $('<tr></tr>').appendTo(passTable);
                var passTitles = $('<tr></tr>').appendTo(passTable);
                var passLoPs = $('<tr></tr>').appendTo(passTable);
                
                for(var i = 0; i < moduleData.passes; i++)
                {
                    (function(pass){
                        $('<td>Pass '+(pass+1)+'</td>').appendTo(passTitles);
                        $('<td><label><input type="checkbox">Done?</label></td>').appendTo(passDones).find('input').change(function(){
                            save({"action": "saveModule", "runID": runid, "module": moduleID, "pass": pass, "done": $(this).prop('checked')});
                        }).prop('checked',moduleData.dones[pass]);
                        
                        //$('<td><img src="img/plus.png" class="plus"><span class="counter">'+moduleData.LoPs[pass]+'</span><img src="img/minus.png" class="minus"></td>').appendTo(passLoPs);
                        var row = $('<td></td>').appendTo(passLoPs);
                        
                        
                        $('<img src='+ IMG_URL +'img/rescueA/minus.png" class="minus">').appendTo(row).click(function(){
                            var modulePoints = {"action": "saveModule", "runID": runid, "module": moduleID, "pass": pass, "LoPs": Math.max(0,+$(antalLoP).text()-1)};
                            antalLoP.text(modulePoints.LoPs);
                            save(modulePoints);
                        }).appendTo(row);
                        var antalLoP = $('<span class="count">'+moduleData.LoPs[pass]+'</span>').appendTo(row);
                        $('<img src='+ IMG_URL +'img/rescueA/plus.png" class="plus">').appendTo(row).click(function(){
                            var modulePoints = {"action": "saveModule", "runID": runid, "module": moduleID, "pass": pass, "LoPs": +$(antalLoP).text()+1};
                            antalLoP.text(modulePoints.LoPs);
                            if(modulePoints.LoPs >= '3')
                                alert("The team *may* move to next room now.");
                            save(modulePoints);
                        }).appendTo(row);
                        
                    })(i);
                }
            
                
                // If it's a secondary team competing here
                if(typeof moduleData.lifted != 'undefined'){
                    $('<img src='+ IMG_URL +'img/rescueA/'+(moduleData.lifted?'':'un')+'lifted.png">').addClass('lifted').click(function(){
                        var modulePoints = {"action": "saveModule", "runID": runid, "module": moduleID};
                        if($(this).attr("src")== IMG_URL +'img/rescueA/lifted.png'){
                            modulePoints.lifted = false;
                            $(this).attr("src", IMG_URL +"img/rescueA/unlifted.png");
                        }else{
                            modulePoints.lifted = true;
                            $(this).attr("src",IMG_URL +"img/rescueA/lifted.png");
                        }
                        save(modulePoints);
                    }).appendTo(module);
                }
            });
        },
        error: function(obj,errMsg){alert("Error while fetching module data: " + errMsg);}
    });
    
    
    function save(poang)
    {
        // TODO: Prevent this from being send twice for some things
        $.ajax({
            type: "POST",
            url: "scoring.php",
            data: {"json": JSON.stringify(poang)},
            dataType: "json",
            success: function(data){
                if(data=="forbidden"){
                    alert("You'r not logged in anymore!");
                }else{
                    // Updates the scoring in the signing-box
                    $('#'+runid+'_poang').text(data);
                }
            },
            error: function(obj,errMsg){alert("Could not save the points: " + errMsg);}
        });     
    }
});
