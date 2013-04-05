// taken from
// http://www.lucaongaro.eu/blog/2012/12/02/easy-two-way-data-binding-in-javascript/
function DataBinder( object_id ) {
  // Use a jQuery object as simple PubSub
  var pubSub = jQuery({});

  // We expect a `data` element specifying the binding
  // in the form: data-bind-<object_id>="<property_name>"
  var data_attr = "bind-" + object_id,
      message = object_id + ":change";

  // Listen to change events on elements with the data-binding attribute and proxy
  // them to the PubSub, so that the change is "broadcasted" to all connected objects
  jQuery( document ).on( "change", "[data-" + data_attr + "]", function( evt ) {
    var $input = jQuery( this );

    pubSub.trigger( message, [ $input.data( data_attr ), $input.val() ] );
  });

  // PubSub propagates changes to all bound elements, setting value of
  // input tags or HTML content of other tags
  pubSub.on( message, function( evt, prop_name, new_val ) {
    jQuery( "[data-" + data_attr + "=" + prop_name + "]" ).each( function() {
      var $bound = jQuery( this );

      if ( $bound.is("input, textarea, select") ) {
        $bound.val( new_val );
      } else {
        $bound.html( new_val );
      }
    });
  });

  return pubSub;
}

function TeamScore( uid ) {
  binder = new DataBinder( uid ),

      score = {
        attributes: {},

        // The attribute setter publish changes using the DataBinder PubSub
        set: function( attr_name, val ) {
          this.attributes[ attr_name ] = val;
          binder.trigger( uid + ":change", [ attr_name, val, this ] );
        },

        get: function( attr_name ) {
          return this.attributes[ attr_name ];
        },

        _binder: binder
      };

  // Subscribe to the PubSub
  binder.on( uid + ":change", function( evt, attr_name, new_val, initiator ) {
    if ( initiator !== user ) {
      score.set( attr_name, new_val );
    }
  });

  return score;
}

function TeamTable( uid ) {
  binder = new DataBinder( uid ),

      score = {
        attributes: {},

        // The attribute setter publish changes using the DataBinder PubSub
        set: function( attr_name, val ) {
          this.attributes[ attr_name ] = val;
          binder.trigger( uid + ":change", [ attr_name, val, this ] );
        },

        get: function( attr_name ) {
          return this.attributes[ attr_name ];
        },

        _binder: binder
      };

  // Subscribe to the PubSub
  binder.on( uid + ":change", function( evt, attr_name, new_val, initiator ) {
    if ( initiator !== user ) {
      score.set( attr_name, new_val );
    }
  });

  return score;
}


tables = new Array();
$(document).ready(function() {
  carousel = $('#slider').scrollingCarousel( {
    scrollerAlignment : 'horizontal',
    autoScroll: true,
    autoScrollSpeed: 20000
  });

  $('.matches').each(function() {
    $(this).css('height', $(window).height() - 230 - $(this).prev().height());
    $(this).scrollingCarousel({
        scrollerAlignment : 'vertical',
        autoScroll: true,
        autoScrollSpeed: 10000
      });
  });

  $('.results').each(function(){
    $(this).css('max-height', $(window).height() - 180);
  });

  $('.table').each(function(){
    tables.push($(this));
  });

  setInterval(function() {
    $.get(FEED_URL, function(data){
        $("#slider ul").html(data);
    });
  }, 10000);

  setInterval(function() {
    $.get(TABLES_URL, function(data){
        tbls = $('<div/>').html(data).contents().toArray();
        tbls = tbls.slice(1, tbls.length - 1);
        var i = 0;
        $('.table').each(function(){
            $(this).html($(tbls[0]).html());
            i += 1;
        });

        $('.matches').each(function() {
          $(this).css('height', $(window).height() - 230 - $(this).prev().height());
          $(this).scrollingCarousel({
              scrollerAlignment : 'vertical',
              autoScroll: true,
              autoScrollSpeed: 10000
            });
        });


        $('.results').each(function(){
          $(this).css('max-height', $(window).height() - 180);
        });
    });
  }, 10000);



  if (tables.length <= 2) {
    return;
  }

  for (var i = 2; i < tables.length; i++) {
    tables[i].hide();
  };

  setInterval(function(){
    table = tables.shift();
    table.fadeOut('slow');
    tables[tables.length-1].fadeIn('slow');
    //console.log(tables[tables.length-1].find('.group_name').text());
    tables.push(table);

  }, 10000);

});
