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

    // Password generator
    function randomString(length, chars) {
        var result = '';
        for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
        return result;
    }
    var passcode = randomString(15, '0123456789!@#$%&*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ');
    $('#id_password1').val(passcode);
    $('#id_password2').val(passcode);

    $("#selectProfile").click(function() {
        var pk = $(".modal .modal-body input[type='radio']:checked").val();
        $('#id_image').val(pk);
        $('#profileImage').modal('hide');
    });

    $("#selectCover").click(function() {
        var pk = $(".modal .modal-body input[type='radio']:checked").val();
        $('#id_cover').val(pk);
        $('#coverImage').modal('hide');
    });


    $("#delete").click(function() {

        if($("input[type='radio']").is(':checked')) {

            var pk = $("input[type='radio']:checked").val();
            var titleid = "tr."+pk+" th.owner1";
            var name = $(titleid).text();

            swal({
                title: "Warning!",
                text: "Are you sure you want to delete '"+name.toString()+"'? Once deleted you will not be able to recover the record!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    deleteAuth(pk);
                } else {
                    swal({
                        title: "Yeey!",
                        text: "Your author is safe.",
                        icon: "info",
                        buttons: false,
                        timer: 3000
                    });
                }
            });

        } else {
            swal({
                title: "Error!",
                text: "You have not selected an author to delete.",
                icon: "error",
                buttons: false,
                timer: 3000
            });
        }
    });

    function deleteAuth(pk){
        $.ajax({
            url : "/author/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $("tr."+pk).hide();
                swal({
                    title: "Success!",
                    text: "The author has been deleted.",
                    icon: "success",
                    buttons: false,
                    timer: 3000
                });
            },

            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The author has not been deleted.",
                    icon: "error",
                    buttons: false,
                    timer: 3000
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    // $("#edit").click(function() {
    //     if($("input[type='radio']").is(':checked')) {
    //         var pk = $("input[type='radio']:checked").val();
    //         window.location.href = "/editquote/"+pk+"/";
    //     } else {
    //         swal({
    //             title: "Error!",
    //             text: "You have not selected a quote to edit.",
    //             icon: "error"
    //         });
    //     }

    // });

});