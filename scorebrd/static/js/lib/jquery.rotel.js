(function( $ ){
  $.fn.getRotationDegrees = function() {
    var angle = 0;
    this.each(function() {
        var obj = $(this);
        var matrix = obj.css("-webkit-transform") ||
        obj.css("-moz-transform")    ||
        obj.css("-ms-transform")     ||
        obj.css("-o-transform")      ||
        obj.css("transform");
        if(!matrix) return 0;
        if(matrix !== 'none') {
/*            if ($.browser.msie && parseInt($.browser.version, 10)<9) {
              var values = matrix.split('(')[1].split(')')[0].split("deg");
              angle = parseInt(values[0]);
            } else {*/
            var values = matrix.split('(')[1].split(')')[0].split(",");
              var a = values[0];
              var b = values[1];
              angle = Math.round(Math.atan2(b, a) * (180/Math.PI));       
            //}
        } else { angle = 0; }
        if (isNaN(angle)) angle = 0;    
        return angle;
    });
    return angle;
  };  
})( jQuery );

(function( $ ){
  $.fn.rotBy = function(d) {  
    this.each(function() {
      $(this).rotTo($(this).getRotationDegrees()+d); 
    }); 
  };
})( jQuery );

(function( $ ){
  $.fn.rotTo = function(d) {  
    this.each(function() {
      var elementToRotate = $(this);
      var degreeOfRotation = d;   
      var deg = degreeOfRotation;
      var deg2radians = Math.PI * 2 / 360;
      var rad = deg * deg2radians ;
      var costheta = Math.cos(rad);
      var sintheta = Math.sin(rad);
      
      var m11 = costheta;
      var m12 = -sintheta;
      var m21 = sintheta;
      var m22 = costheta;
      var matrixValues = 'M11=' + m11 + ', M12='+ m12 +', M21='+ m21 +', M22='+ m22;
      elementToRotate.css('-webkit-transform','rotate('+deg+'deg)')
          .css('-moz-transform','rotate('+deg+'deg)')
          .css('-ms-transform','rotate('+deg+'deg)')
          .css('transform','rotate('+deg+'deg)');
      /*if ($.browser.msie && parseInt($.browser.version, 10)<9) {
           elementToRotate.css('filter', 'progid:DXImageTransform.Microsoft.Matrix(sizingMethod=\'auto expand\','+matrixValues+')')
                          .css('-ms-filter', 'progid:DXImageTransform.Microsoft.Matrix(SizingMethod=\'auto expand\','+matrixValues+')');
      }*/
    }); 
  };
})( jQuery );


