function scoreTracker(options)
{
    $this = this;
    $this.team = 'Robot';
    $this.final_score = 0;
    $this.round_number = options['round_number'];
    $this.mins = 8;
    $this.secs = 0;
    $this.finished = false;
    $this.back_url = options['back_url'];
    $this.update_url = options['update_url'];

    $this.scores = {
          'floating_victim' : 0,
          'linear_victim': 0,
          'false_victim' : 0,
          'lack_of_progress': 0,
          'successful_exit': 0,
    };

    $this.scoresheet = {
          'floating_victim' : 25,
          'linear_victim': 10,
          'false_victim' : -10,
          'successful_exit': 10,
    };
}

scoreTracker.prototype = { 
    syncPerf: function (){
    },


    addEach: function (Each, string){
        if (string == 'successful_exit' && $this.scores[string] == 1){
            return;    
        }
        $this.scores[string]++;
        $(Each).html($this.scores[string] + '<span style="font-size: 50%;">x</span>');              
    }, 

    rmEach: function (Each, string){
        if ($this.scores[string] > 0)
            $this.scores[string]--;
        $(Each).html($this.scores[string] + '<span style="font-size: 50%;">x</span>');  
    },

    resetScore: function (){
        $this.final_score = 0;

        for (j in $this.scores){
            $this.scores[j] = 0;
            $("#Each" + j).html('0<span style="font-size: 50%;">x</span>');  
        }
        
    },

    newTime: function (){
	    var inpMins = $('#fmins').val();
	    var inpSecs = $('#fsecs').val();
	
        $this.mins = inpMins;
        $this.secs = inpSecs;
        $('.saved').fadeIn(200).delay(500).fadeOut(200);
        
        return false;
    },


    // stopwatch
    toggle: function (){
        if ($("#startAll").is(':visible')){
            $('#startAll').hide();
        }  

        if ($("#btnStart").html() == "Start" || $("#btnStart").html() == "Resume"){
            $("#btnStart").html('Pause')
	        $("#timeStopwatch").stopwatch({formatter: $this.format, updateInterval: 50}).stopwatch('start');
            return;
        } else if ($("#btnStart").html() == "Pause"){
            $("#btnStart").html("Resume");
	        $("#timeStopwatch").stopwatch().stopwatch('stop');
	        return;
        }
    },

    startPerf: function (){
        $this.syncPerf(); // marks the match as started
        $('#startAll').hide();
        $this.toggle();
    },

    resetTime: function (){
	    if ($("#btnStart").html() == "Resume" || $("#btnStart").html() == "Pause") {
            $("#timeStopwatch").stopwatch().stopwatch('stop');		
            $("#timeStopwatch").stopwatch().stopwatch('reset');
            $("#timeStopwatch").html("00:00,00");
            $("#btnStart").html("Start");
        }
        if ($("#startAll").is(':hidden')){
            $('#startText').html("Start "+ $this.round_number +". round");
            $('#startAll').show();
        }else {
            $('#startText').html("Start "+ $this.round_number +". round");
        }

	
        return;
    },

    format: function (millis){
        function pad2(number) {
            return (number < 10 ? '0' : '') + number;
        }
                                          
        var seconds, minutes;                                              
        minutes = Math.floor(millis / 60000);                              
        millis %= 60000;                                                   
        seconds = Math.floor(millis / 1000);                               
        millis = Math.floor(millis % 1000);                                
        millis = Math.floor(millis / 10);

        if (minutes >= $this.mins){
            if (seconds >= $this.secs){
                $("#timeStopwatch").stopwatch().stopwatch('stop');        
                $.idleTimer('destroy');
                $this.finished = true;
                $this.showD();
            }
        }
		
        return [pad2(minutes), pad2(seconds)].join(':') + ',' + pad2(millis);
    },

    showD: function () {
	    $('#dialogMain').show();    
	    $("#dialog").dialog({ 
            buttons: {
            "Send results": function() {
                window.onbeforeunload = function(){}

                var df = confirm("Are you sure you want to save these results?");

                if (df)
                    $('#dialogForm').submit();  
                else 
                    return;

                }	
            },
            width: 550,
            height: 440
        });


        for (y in $this.scores){
            $('#' + y).val($this.scores[y]);
        }

        $this.scoreCount();
        $('#time').val($('#timeStopwatch').html());
    },

    scoreCount: function (){
        $this.final_score = 0;

        // floating victims
        $this.final_score += $this.scores["floating_victim"] * $this.scoresheet["floating_victim"];
        // linear victims        
        $this.final_score += $this.scores["linear_victim"] * $this.scoresheet["linear_victim"];
        // false victims
        $this.final_score += $this.scores["false_victim"] * $this.scoresheet["false_victim"];
        // successful exit bonus
        if ($this.scores["successful_exit"])
          $this.final_score += ($this.scores["floating_victim"] + $this.scores["linear_victim"]) * $this.scoresheet["successful_exit"];

        // reliability
        var reliability = 0;
        reliability += ($this.scores["floating_victim"] + $this.scores["linear_victim"] - $this.scores["lack_of_progress"]) * 10;

        if (reliability < 0){
          reliability = 0;
        } else {
          $this.final_score += reliability;
        }    

        $('#reliability').val(reliability);
        $('#points').val($this.final_score);
    },

    recount: function () {
        for (y in $this.scores){
            $this.scores[y] = parseInt($('#' + y).val());
        }
        $this.scoreCount();
    }
}
