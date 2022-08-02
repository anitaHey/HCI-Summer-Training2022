$(document).ready(function(e) {
    refresh();

    $("#send").click(function() {
        if($("#msg").val() != ""){
            $.ajax({
                type: "POST",
                url: "sendMsg.php",
                data: {
                    msg: $("#msg").val()
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                },
                success: function(output) {
                    console.log(output);
                    refresh();

                    $("#msg").val("");
                }
            });
        }
    });
});

function refresh() {
    $.ajax({
        type: "POST",
        url: "showMsg.php",
        error: function(xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        },
        success: function(output) {
            output = $.parseJSON(output);
            console.log(output);
            var table = "";
            for (var num = 0; num < output.length; num++) {
                table += "<tr><td>" + output[num][0] + "</td>";
                table += "<td>" + output[num][1] + "</td>";
                table += "<td>" + output[num][2] + "</td></tr>";
            }

            $("#message_table").html(table);
        }
    });
}