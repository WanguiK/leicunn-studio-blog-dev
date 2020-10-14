$(document).ready(function () {

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#delete").click(function() {

        if($("input[type='radio']").is(':checked')) {

            var pk = $("input[type='radio']:checked").val();
            var titleid = "#quote"+pk+" .owner";
            var title = $(titleid).text();

            swal({
                title: "Warning!",
                text: "Are you sure you want to delete the quote by '"+title+"'? Once deleted you will not be able to recover it!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    deletePost(pk);
                } else {
                    swal({
                        title: "Yeey!",
                        text: "Your quote is safe.",
                        icon: "info",
                        buttons: false,
                        timer: 3500
                    });
                }
            });

        } else {
            swal({
                title: "Error!",
                text: "You have not selected a quote to delete.",
                icon: "error",
                buttons: false,
                timer: 3500
            });
        }
    });

    function deletePost(pk){
        $.ajax({
            url : "/quote/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#quote'+pk).hide();
                swal({
                    title: "Success!",
                    text: "The quote has been deleted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
            },

            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The category has not been deleted.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $("#edit").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            window.location.href = "/editquote/"+pk+"/";
        } else {
            swal({
                title: "Error!",
                text: "You have not selected a quote to edit.",
                icon: "error",
                buttons: false,
                timer: 3500
            });
        }

    });

});