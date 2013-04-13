function scoreTracker(options)
{
    $this = this;
    $this.team = 'Robot';
    $this.final_score = 0;

    $this.mins = 8;
    $this.secs = 0;
    $this.finished = false;
    $this.back_url = options['back_url'];
    $this.update_url = options['update_url'];

    $this.scores = {
        'try' : {
            'room1' : 0,
            'room2' : 0,
            'room3' : 0,
            'ramp'  : 0,
            'hallway':0,
            'victim': 0,
        },
        'each' : {
            'gap' : 0,
            'obstacle': 0,
            'speed_bump': 0,
            'intersection': 0,
            'lift': 0,
        }
    };

    $this.scoresheet = {
        'try' : {
            'room1' : {1 : 60, 2 : 40, 3 : 20, '---' : 0},
            'room2' : {1 : 60, 2 : 40, 3 : 20, '---' : 0},
            'room3' : {1 : 60, 2 : 40, 3 : 20, '---' : 0},
            'ramp'  : {1 : 30, 2 : 20, 3 : 10, '---' : 0},
            'hallway':{1 : 30, 2 : 20, 3 : 10, '---' : 0},
            'victim': {1 : 60, 2 : 40, 3 : 20, '---' : 0},      
        },
        'each' : {
            'gap' : 10,
            'obstacle': 10,
            'speed_bump': 5,
            'intersection': 10,
            'lift': 20,
        }
    }
}

scoreTracker.prototype = { 
    syncPerf: function (){
    },

    addTry: function (Try, string){
        if ($this.scores["try"][string] < 3){
            $this.scores["try"][string]++;
            $(Try).html($this.scores["try"][string] + '. <span style="font-size: 50%;">try<span>');
        } else {
            $this.scores["try"][string] = 4;
            $(Try).html("-----");
        }
    },

    rmTry: function (Try, string){
        if ($this.scores["try"][string] > 0){
            $this.scores["try"][string]--;
            if ($this.scores["try"][string] == 0){
                $(Try).html('-----');  
            } else {
                $(Try).html($this.scores["try"][string] + '. <span style="font-size: 50%;">try<span>');  
            }
        } 
    },

    addEach: function (Each, string){
        if (string == 'lift' && $this.scores["each"][string] == 1){
            return;    
        }
        $this.scores["each"][string]++;
        $(Each).html($this.scores["each"][string] + '<span style="font-size: 50%;">x</span>');              
    }, 

    rmEach: function (Each, string){
        if ($this.scores["each"][string] > 0)
            $this.scores["each"][string]--;
        $(Each).html($this.scores["each"][string] + '<span style="font-size: 50%;">x</span>');  
    },

    resetScore: function (){
        $this.final_score = 0;

        for (i in $this.scores["try"]){
            $this.scores["try"][i] = 0;
            $("#Try" + i).html("-----")
        }
        for (j in $this.scores["each"]){
            $this.scores["each"][i] = 0;
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
            $('#startText').html("Start round");
            $('#startAll').show();
        }else {
            $('#startText').html("Start round");
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

        for (x in $this.scores["try"]){
            if ($this.scores["try"][x] == 4){
                $('#' + x).val(0);
            } else {
                $('#' + x).val($this.scores["try"][x]);
            }        
        }

        for (y in $this.scores["each"]){
            $('#' + y).val($this.scores["each"][y]);
        }

        $this.scoreCount();
        $('#time').val($('#timeStopwatch').html());
    },

    scoreCount: function (){
        $this.final_score = 0;
        for (x in $this.scores["try"]){
            if ($this.scores["try"][x] > 0 && $this.scores["try"][x] < 4)
                $this.final_score += $this.scoresheet['try'][x][$this.scores["try"][x]];
        }
        for (y in $this.scores["each"]){
            $this.final_score += $this.scores["each"][y] * $this.scoresheet['each'][y];
        }

        $('#points').val($this.final_score);
    },

    recount: function () {
        for (x in $this.scores["try"]){
            if ($this.scores["try"][x] == '' ||
                    $this.scores["try"][x] == '---' || $this.scores["try"][x] == 0){
                $this.scores["try"][x] = 4;
            }else {
                $this.scores["try"][x] = $('#' + x).val();
            }        
        }

        for (y in $this.scores["each"]){
            $this.scores["each"][y] = $('#' + y).val();
        }
        $this.scoreCount();
    }
}
