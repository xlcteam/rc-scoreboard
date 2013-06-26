$(document).ready(function () {

    var antalTiles = 27;
   
    var mapID = $_GET['id'];
    
    var map = $("#map");
    var info = $("<div></div>").prependTo(map);
    // Create the user interface
    $('<h1>Create map</h1>').appendTo(info);
    var name=$('<input type="text" id="name">').appendTo(info);
    name.before('<label for="name">Name: </label>');
    var save=$('<input type="button" value="Save!">').click(function(){
        var json = {"action": "saveMap", "mapID": mapID, "name": name.val(), "tiles": {}, "passes": {}};
        
        // Save all the tiles
        $(".location .tile").each(function(){
            json.tiles[$(this).parent().attr("id")] = {"src": $(this).children("img.path").first().attr("src"), "angle": $(this).children("img.path").first().getRotationDegrees(), "gap": $(this).data("gap"), "speedbump": $(this).data("speedbump"), "obstacle": $(this).data("obstacle"), "intersection": $(this).data("intersection")};
        });
        
        $('.room-info input').each(function(){
            if($(this).attr('name') == "evacuation"){
                if($(this).prop("checked"))
                    json["evacuation"] = $(this).val();
            }else{
                json.passes[$(this).attr('name')] = $(this).val();
            }
        });
//        console.log(json);
//
        console.log(JSON.stringify(json));
        $.ajax({
            type: "POST",
            url: "mapgen.php",
            data: {"json": JSON.stringify(json)},
            dataType: "json",
            success: function(data){alert("The map is now saved!"); mapID = data;},
            error: function(obj,errMsg){alert("Error when saving map: " + errMsg);}
        });
    }).appendTo(info);
    


    // Loop through room and add controls. 
    // Sets the value to the id of the table cell
    $('.possible-evacuation').append(function(index,html){return '<label><input type="radio" name="evacuation" value="'+$(this).attr('id')+'">Evacuation room</label><br>';});
    // Sets the name to the id of the table cell
    $('.room-info').append(function(index,html){return '<label>Possible passes:<br><input type="number" value="1" min="0" name="'+$(this).attr('id')+'"></label><br>';});



    // Loop through table and add indexes and droppables to the cells. 
    $('.location').attr('id',function(index,attr){return index;}).droppable({
        'accept': function(ui)
        {
            return $(this).is(':empty');
        },
        'addClasses': false,
        'hoverClass': 'location-hover',
        'drop': function(event, ui)
        {
            var tile = ui.draggable;
            tile.css({'top': '0px', 'left': '0px'});
            
            // If the tiles was created in the tilebox previous events should be removed, and the tile should get a meny among others. 
            if(tile.parent().is('div')){
                tile = tile.clone().data('gap',0).data('speedbump',0).data('obstacle',0).data('intersection',0).draggable({'revert': 'invalid'});
                // This have to be done separately because the variable "tile" should be assigned to the cloned object.
                tile.contextmenu(createmenu(tile),'right');
            }
            
            tile.appendTo($(this));
        }
    });
    
    
    // Create a toolbox with tiles - tilebox
    var tilesbox=$('<div></div>').attr('id','tilesbox').droppable({
        'addClasses': false,
        'accept': function(ui)
        {
            // The tile must have been placed (and therefore cloned) to be deleted
            return ui.parent().is('td');
        },
        'drop': function(event,ui){
            ui.draggable.remove();
        }
    }).appendTo(map);
    $('<h2>Tile box:</h2>').appendTo(tilesbox);
    
    // Creates all the tiles in the tilebox
    for(var i=0; i<antalTiles;i++)
    {
        $('<span></span>').addClass('tile').draggable({
            'helper': 'clone',
            'revert': 'invalid'
        }).append(
            $('<img src="' + IMG_DIR + 'img/rescueA/tiles/tile-'+i+'.png">').addClass('path').bind("contextmenu",function(e){
                $(this).rotBy(90);
                return false;// Prevents the default context menu to show up
            })
        ).appendTo(tilesbox);
    }
    
    
    // If it is a certain map we are loading
    if(mapID>0) // This is only executed during initiating, and it is okay to change the mapID when saving a newly created map
    {
        alert("Loading map!!");
        // Ask the server for tiles!
        $.ajax({
            type: "POST",
            url: "mapgen.php",
            data: {"json": JSON.stringify({"mapID": mapID, "action": "getTiles"})},
            dataType: "json",
            success: function(data){ 
                //data = {"action":"saveMap","mapID":0,"name":"Fredrik Leker","tiles":{"4":{"src":"img/tiles/tile-6.png","angle":0,"gap":0,"speedbump":0,"obstacle":0,"intersection":"1"},"8":{"src":"img/tiles/tile-0.png","angle":0,"gap":0,"speedbump":0,"obstacle":0,"intersection":"2"},"12":{"src":"img/tiles/tile-15.png","angle":0,"gap":0,"speedbump":"1","obstacle":0,"intersection":0}},"passes":{"ramp":"3","second":"3","first":"2","hallway":"1","outer":"1"},"evacuation":"first"};
                // Loads the name of the map
                name.val(data.name);
                // Loads the evacuation room
                $('#'+data.evacuation+' input[name="evacuation"]').prop('checked',true);
                
                // Loads the number of passages
                $.each(data.passes, function(id, number){
                    console.log("id: " + id + ", number: " + number);
                    $('#'+id+' input[name="'+id+'"]').val(number);
                });
                
                
                $.each(data.tiles, function(index, tileData){
                    tile = $('<span></span>').addClass('tile').data('gap',tileData.gap).data('speedbump',tileData.speedbump).data('obstacle',tileData.obstacle).data('intersection',tileData.intersection).draggable({'revert': 'invalid'}).appendTo('#'+index);

                    // This have to be done separately because the variable tile needs to be assigned
                    tile.contextmenu(createmenu(tile),'right');

                    
                    $('<img src="'+ tileData.src+'">').addClass('path').appendTo(tile);
                    tile.find("img.path").rotTo(tileData.angle);


                    if(tile.data("speedbump")>0)
                        $('<img src="'+ IMG_DIR +'img/rescueA/speedbump.png">').appendTo(tile);
                    if(tile.data("gap")>0)
                        $('<img src="'+ IMG_DIR +'img/rescueA/gap.png">').appendTo(tile);
                    if(tile.data("obstacle")>0)
                        $('<img src="'+ IMG_DIR +'img/rescueA/obstacle.png">').appendTo(tile);
                    if(tile.data("intersection")>0)
                        $('<img src="'+ IMG_DIR +'img/rescueA/intersection.png">').appendTo(tile);
                    
                });
            },
            error: function(obj,errMsg){alert("Error while fetching tiles: " + errMsg);}
        });
    }
    

    // Creates a context menu where the user can add things to a tile
    function createmenu(tile)
    {
        
        var meny = {'speedbump':null, 'gap':null,'obstacle':null,'intersection':null};
        
        
        $.each(meny,function(key,val)
               {
                   meny[key] = function(){
                       // Save the value to the tile
                       tile.data(key,window.prompt("Number of "+key+"s?","0"));
                       // Remove possible images that already have been added.
                       tile.children('img[src$="'+key+'.png"]').remove();
                       // If it should be an image here I will add it once again... // TODO: Don't remove the image first
                       if(tile.data(key)>0)
                           $('<img src="'+ IMG_DIR +'img/rescueA/'+key+'.png" class="'+key+'">').appendTo(tile);
                       
                   };
               });
        
        meny['Remove'] = function(){
            tile.remove();
        };
        return meny;
    }
    
});

