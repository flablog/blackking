
$(document).ready(function(){

    $("#bk_main_topMenu_bottom").click(function(){
        if ($("#bk_main_play").hasClass('notDisplayed')){
            $("#intro").addClass('notDisplayed');
            $("#bk_main_play").removeClass('notDisplayed');
        }
    });
    
    $(".goTo").click(function(){
        //alert($(this).attr('toUrl'));
        window.location.href = $(this).attr('toUrl');;
    });


});