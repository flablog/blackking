
$(document).ready(function(){
   

    
    function updateDashboard(){
        $.getJSON( "../updateDashboard/" )
        .done(function( data ) {
            
            var items = [];
            $.each( data, function( key, val ) {
                // King MOVE
                
                
                if (key == 'KINGMOVE_LASTMSG'){
                    if (val > $("#KINGMOVE").attr('lastMove')){
                        $("#KINGMOVE").html(data["KINGMOVE_MSG"]);
                        
                    }
                    
                }
                
                /*
                obj["KINGMOVE_MSG"] = lastKingMove[0]
                obj["KINGMOVE_IMGSRC"] = lastKingMove[1]
                obj["KINGMOVE_LASTMSG"] = lastKingMove[2]


<div id="KINGMOVE" lastMove="0">
                    Hello says the king
                    
                    </div>
                    */
                
                // Your turn ?
                if (key == "TURN"){
                    $("#TURN").html(val);
                }
                
                // New Mission ?
                if (key == "NEWMISSION" && val == "YES"){
                    
                        $("#NEWMISSION").html("<p>You need to pick a mission:<ul><li class='GetMission' difficulty='1'>Easy</li><li class='GetMission' difficulty='2'>Medium</li><li class='GetMission' difficulty='3'>Hard</li><li class='GetMission' difficulty='4'>Very Hard</li></ul></p>");
                       
                }else{
                    $("#NEWMISSION").html();
                }
                // Infos ?
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
        $.get('../turnDone/');
        updateDashboard();
    });
    
    // Get Mission
    $('#NEWMISSION').on('click', '.GetMission', function(){
        $.get('../getMission/');
        updateDashboard();
    });
    
    setInterval(updateDashboard, 2000);
    
});