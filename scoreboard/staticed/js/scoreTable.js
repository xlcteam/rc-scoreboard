function arrange() {
   $('.matches').each(function() {
     $(this).css('height', $(window).height() - 230 - $(this).prev().height());
     $(this).scrollingCarousel({
         scrollerAlignment : 'vertical',
         autoScroll: true,
         autoScrollSpeed: 10000
       });
   });


   $('.results').each(function(){
     $(this).css('max-height', $(window).height() - 200);
   });
}

tables = new Array();
$(window).load(function() {
  carousel = $('#slider').scrollingCarousel( {
    scrollerAlignment : 'horizontal',
    autoScroll: true,
    autoScrollSpeed: 20000
  });
    
  arrange();

  $('.table').each(function(){
    tables.push($(this));
  });

  setInterval(function() {
    $.get(FEED_URL, function(data){
        $("#slider ul").html(data);
    });
  }, 10000);

  setTimeout(function(){
      window.location = window.location;
  }, 60000);

  setInterval(function() {
    $.get(TABLES_URL, function(data){
        console.log('sending', data);
        $('tables').html(data);
      //tbls = $('<div/>').html(data).contents().toArray();
      //console.log(tbls);
      //tbls = tbls.slice(1, tbls.length - 1);
      //var i = 0;
      //$('.table').each(function(){
      //    $(this).html($(tbls[i]).html());
      //    i += 1;
      //});

      //arrange();
    });
  }, 10000);



  if (tables.length <= 2) {
    return;
  }

//for (var i = 2; i < tables.length; i++) {
//  tables[i].hide();
//};

//setInterval(function(){
//  table = tables.shift();
//  table.fadeOut('slow');
//  tables[tables.length-1].fadeIn('slow');
//  //console.log(tables[tables.length-1].find('.group_name').text());
//  tables.push(table);

//}, 10000);

});
