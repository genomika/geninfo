function update_list() {
    $.ajax({
        type: "GET",
        url: "/?async=true"
    }).done(function(tr_home_in){
        $("#body_home").empty();
        $("#body_home").append(tr_home_in);
        console.log("Rodou")
    });
}

$(document).ready(function(){
	setTimeout(update_list, 45000);
});