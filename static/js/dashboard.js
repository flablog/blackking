
$(document).ready(function(){
   
    var clickSound = new Audio('/static/nextTurn.wav');

    
    function updateDashboard(){
        $.getJSON( "../updateDashboard/" )
        .done(function( data ) {
            var items = [];
            $.each( data, function( key, val ) {
                // King MOVE
                if (key == 'KINGMOVE_LASTMSG'){
                    if (val > parseInt($("#KINGMOVE").attr('lastMove'))){
                        $("#KINGMOVE_MSG").html(data["KINGMOVE_MSG"]);
                        //clickSound.play();
                        // probablement changement du current turn au passage
                        if (data["CURRENTTURN"]>0){
                            $("#currentTurn").html("It's turn " + data["CURRENTTURN"]);
                            $('#currentTurn').attr('currentTurn', data["CURRENTTURN"]);
                        }
                    }
                    
                }
                
                // Your turn ?
                if (key == "TURN"){
                    $("#TURN").html(val);
                }
                
                // New Mission ?
                if (key == "NEWMISSION" && val == "YES"){
                    
                        $("#NEWMISSION").html("<p>You need to pick a mission:<ul><li class='GetMission' difficulty='1'>Easy</li><li class='GetMission' difficulty='2'>Medium</li><li class='GetMission' difficulty='3'>Hard</li><li class='GetMission' difficulty='4'>Very Hard</li></ul></p>");
                        $("#NEWMISSION").html("<div class='alert alert-danger' id='NEWMISSIONDIV'>You need a mission, select a difficulty:<br/><button class='btn btn-default GetMission' difficulty='1'>1</button><button class='btn btn-default GetMission' difficulty='2'>2</button><button class='btn btn-default GetMission' difficulty='3'>3</button><button class='btn btn-default GetMission' difficulty='4'>4</button></div>");

                       
                }else{
                    $("#NEWMISSION").html();
                }
                
                // Infos ?
                if (key.substring(0, 4) == "INFO") {
                    $( "#INFOS" ).prepend( "<div class=\"alert alert-info alert-dismissable\"><button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>"+ val +"</div>" );
                }
                if (key == "MISSIONS"){                    
                      for (var i=0; i<val.length; i++) {
                            // Pour chaque mission
                          var mission = val[i];
                          if ($('#mission_' + mission["ROWID"]).length == 0){
                                // la div mission n'existe pas encore
                                $('#MISSIONS').prepend("<div class=\"missionDiv\" id=\"mission_"+ mission["ROWID"] +"\" missionId=\""+ mission["ROWID"] +"\" missionStatus=\"0\">Loading mission " + mission["p1"] + mission["p2"] + mission["p3"] +mission["p4"] +"</div>");
                          }
                          
                          if (parseInt($('#mission_' + mission["ROWID"]).attr('missionStatus')) != mission['status']){
                              // mission update
                              //<div class="alert alert-warning">This is a mission</div>
                              
                              var div = '<div class="alert ';
                              
                              if (mission["status"] == 3){
                                div += 'alert-success">Mission achieved:<br/>';
                              }else{
                                div += 'alert-warning">Your current mission :<br/>';
                              }
                              
                              //div += ""+ mission["p1"] + ""+ mission["p2"] + "" + mission["p3"] + "" + mission["p4"] ;
                              
                              var p = ["p1","p2", "p3", "p4"];
                              var f = ["Peown", "Tower", "Horse", "Bishop", "Queen"];
                              for (var j=0; j<p.length; j++) {
                                    div += f[mission[p[j]]] ;
                                    if (mission[p[j] +"Color"] != 2){
                                        if (mission[p[j] +"Color"] == 0){
                                            div += '<span class="badge">b</span>';
                                        }else{
                                            div += '<span class="badge">w</span>';
                                        }
                                    }
                                    div += " ";
                              }
                              
                              if (mission["status"] == 1){
                                // mission a valider
                                div += "<br/><button class='btn btn-success btn-xs missionDone' missionId='" + mission["ROWID"] + "'>Mission Done !</button>";
                              }
                              if (mission["status"] == 2){
                                // mission en cours de vote
                                div += "<br/>Your mission is getting verified by the others";
                              }
                              
                              
                              div += '</div>';
                              
                              $('#mission_' + mission["ROWID"]).attr('missionStatus', mission['status'] );
                              $('#mission_' + mission["ROWID"]).html(div);
                              
                          }
                          
                          //alert("mission " + mission["ROWID"] + ":"+ mission["p1"] + mission["p2"] + mission["p3"] +mission["p4"]);
                      }
                }
                
                
                if (key == "POLLS"){                    
                      for (var i=0; i<val.length; i++) {
                            // Pour chaque mission
                          var poll = val[i];
                          if ($('#poll_' + poll["ROWID"]).length == 0){
                                // la div poll n'existe pas encore
                                $('#POLLS').prepend("<div class=\"pollDiv\" id=\"poll_"+ poll["ROWID"] +"\" pollId=\""+ poll["ROWID"] +"\" >Loading poll</div>");
                          
                                var div = '<div class="alert ';
                              
                              div += 'alert-danger">Another player said his mission is over:<br/>';
                              
                              var p = ["p1","p2", "p3", "p4"];
                              var f = ["Peown", "Tower", "Horse", "Bishop", "Queen"];
                              for (var j=0; j<p.length; j++) {
                                    div += f[poll[p[j]]];
                                    
                                    if (poll[p[j] +"Color"] != 2){
                                        if (poll[p[j] +"Color"] == 0){
                                            div += '<span class="badge">b</span>';
                                        }else{
                                            div += '<span class="badge">w</span>';
                                        }
                                    }
                                    div += " ";
                              }
                              
                              
                                // mission en cours de vote
                                div += "<br/>Is this mission achieved? <button class='btn btn-success btn-xs pollVote' pollId='" + poll["ROWID"] + "' vote='1'>YES</button> <button class='btn btn-danger btn-xs pollVote' pollId='" + poll["ROWID"] + "' vote='0'>NO</button>";
                              
                              
                              
                              div += '</div>';
                              
                              $('#poll_' + poll["ROWID"]).html(div);
                              
                          }
                          
                          //alert("mission " + mission["ROWID"] + ":"+ mission["p1"] + mission["p2"] + mission["p3"] +mission["p4"]);
                      }
                }
                
                if (key == "SCORE"){
                    $("#SCORE").html(val);
                }
                
            });
          
        });
    }
    
   
    // Turn Done
    $('body').on('click', '#IAMDONE', function(){
        $.get('../turnDone/');
        updateDashboard();
    });
    //  Mission DONE
    $('#MISSIONS').on('click', '.missionDone', function(){
        var missionId = $(this).attr('missionid');
        $.get('../callPoll/'+missionId+'/');
        updateDashboard();
    });
    // Get Mission
    $('#NEWMISSION').on('click', '.GetMission', function(){
        var difficulty = $(this).attr('difficulty');
        $("#NEWMISSIONDIV").remove()
        $.get('../getMission/'+difficulty+'/');
        
        updateDashboard();
        
    });
    
    // Vote
    $('#POLLS').on('click', '.pollVote', function(){
        //alert('Voting');
        var missionId = $(this).attr('pollId');
        var vote = $(this).attr('vote');
        $.get('../votePoll/'+missionId+'/' + vote + '/');
        $('#poll_' + missionId).remove();
    });
    
    setInterval(updateDashboard, 2000);
    
});