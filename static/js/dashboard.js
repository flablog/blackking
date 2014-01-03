
$(document).ready(function(){
   

    
    function updateDashboard(){
        $.getJSON( "../updateDashboard/" )
        .done(function( data ) {
            
            var items = [];
            $.each( data, function( key, val ) {
                
                if (key == "TURN"){
                    $("#TURN").html(val);
                }

                if (key.substring(0, 4) == "INFO") {
                    $( "#INFOS" ).prepend( "<div class=\"alert alert-info alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>"+ val +"</div>" );
                }
                if (key.substring(0,12) == "MISSION_MSG_"){
                    var missionid = key.split("_")[2];
                    
                    if ($("#mission_"+ missionid).length == 0){
                        $( "#MISSIONS" ).prepend("<div id='mission_" + missionid + "' missionStatus='LOADING'>Mission "+ missionid + ": Loading" + "</div>");
                    }
                    
                    if ($("#mission_"+ missionid).attr("missionStatus") != data["MISSION_STS_" + missionid]){
                        //Update de la mission
                        if ( data["MISSION_STS_" + missionid] == "RUNNING"){
                            $("#mission_"+ missionid).html("<div class=\"alert alert-warning\">"+ val +"</div>")
                        }
                        
                    }
                    
                    
                    
                }
            });
          
        });
    }
    
   
    // Turn Done
    $('body').on('click', '#IAMDONE', function(){
        $("#TURN").html("Please wait...");
        $.get('../turnDone/');
        updateDashboard()
    });
    
    setInterval(updateDashboard, 2000);
    
});