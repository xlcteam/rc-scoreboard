$(document).ready(function () {

    var antalTiles = 27;
   
    var mapID = $_GET.id;// The variable needs to be set in the page that loads this js-file
    
    
    var map = $("#map");
    // Create the user interface
    $('<h1>Create map</h1>').appendTo(map);
    var name=$('<input type="text" id="name">').appendTo(map);
    name.before('<label for="name">Name: </label>');
    var save=$('<input type="button" value="Save!">').click(function(){
        var json = {"action": "saveMap", "mapID": mapID, "name": name.val(), "tiles": {}};
        
        $(".location .tile").each(function(){
            json.tiles[$(this).parent().attr("id")] = {"src": $(this).children("img.path").first().attr("src"), "angle": $(this).children("img.path").first().getRotationDegrees(), "gap": $(this).data("gap"), "speedbump": $(this).data("speedbump"), "obstacle": $(this).data("obstacle"), "intersection": $(this).data("intersection")};
        });
        $.ajax({
            type: "POST",
            url: "mapgen.php",
            data: {"json": JSON.stringify(json)},
            dataType: "json",
            success: function(data){alert("The map is now saved!"); mapID = data;},
            error: function(obj,errMsg){alert("Error when saving map: " + errMsg);}
        });
    }).appendTo(map).after('<br>').before('<br>');
    

    // Creates an empty arena with a table
    var field = $('<table></table>').addClass('field').appendTo(map);
    for(var h=0; h<11; h++)
    {
        var row = $('<tr></tr>').appendTo(field);
        
        for(var b=0; b<4;b++)
        {
            $('<td></td>').addClass('location').attr('id',b + '_' + h).droppable({
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
            }).appendTo(row);

        }

        if(h==2 || h==3 || h==6 || h==7)
        {
            field.append('<tr><td class="separator" colspan="4"></td></tr>');
        }
    }


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
            $('<img src="img/tiles/tile-'+i+'.png">').addClass('path').bind("contextmenu",function(e){
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

                name.val(data.name);
                $.each(data.tiles, function(index, tileData){
                    tile = $('<span></span>').addClass('tile').data('gap',tileData.gap).data('speedbump',tileData.speedbump).data('obstacle',tileData.obstacle).data('intersection',tileData.intersection).draggable({'revert': 'invalid'}).appendTo('#'+tileData.x+'_'+tileData.y);

                    // This have to be done separately because the variable tile needs to be assigned
                    tile.contextmenu(createmenu(tile),'right');

                    
                    $('<img src="'+ tileData.src+'">').addClass('path').appendTo(tile);
                    tile.find("img.path").rotTo(tileData.angle);


                    if(tile.data("speedbump")>0)
                        $('<img src="img/speedbump.png">').appendTo(tile);
                    if(tile.data("gap")>0)
                        $('<img src="img/gap.png">').appendTo(tile);
                    if(tile.data("obstacle")>0)
                        $('<img src="img/obstacle.png">').appendTo(tile);
                    if(tile.data("intersection")>0)
                        $('<img src="img/intersection.png">').appendTo(tile);
                    
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
                       tile.data(key,window.prompt("Number of "+key+"s?","0"));
                       if(tile.data(key)>0)
                           $('<img src="img/'+key+'.png">').appendTo(tile);
                       else
                            tile.children('.'+key).remove();// TODO: There are no class to remove... 
                   };
               });
        
        meny['Remove'] = function(){
            tile.remove();
        };
        return meny;
    }
    
});

