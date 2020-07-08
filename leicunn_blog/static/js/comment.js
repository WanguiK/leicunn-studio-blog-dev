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
        var pk = $("input[type='radio']:checked").val();
        var titleid = "#commenter"+pk;
        var commenter = $(titleid).text();

        if (pk == null) {
            swal({
                title: "Error!",
                text: "You have to select a comment to delete.",
                icon: "error"
            });
        } else {
            swal({
                title: "Warning!",
                text: "Are you sure you want to delete the comment by '"+ commenter +"'? All replies associated with this comment will also be deleted and once deleted, you will not be able to recover them!",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
            .then((willDelete) => {
                if (willDelete) {
                    deleteComment(pk);
                } else {
                    swal({
                        title: "Yeey!",
                        text: "Your comment is safe.",
                        icon: "info"
                    });
                }
            });
        }

    });

    function deleteComment(pk){
        $.ajax({
            url : "/comment/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#comment'+pk).hide();
                swal({
                    title: "Success!",
                    text: "The comment has been deleted.",
                    icon: "success"
                });
            },
            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been deleted.",
                    icon: "error"
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $("#edit").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            window.location.href = "/editcomment/"+pk+"/";
        } else {
            swal({
                title: "Error!",
                text: "You have not selected a comment to edit.",
                icon: "error"
            });
        }

    });

    $("#reply").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            display_comment(pk);
        } else {
            swal({
                title: "Error!",
                text: "You have not selected a comment to edit.",
                icon: "error"
            });
        }

    });

    function display_comment(pk){
        $.ajax({
            url : "/getcomment/"+pk+"/",
            type: 'GET',
            dataType: 'json',
            success : function(json) {
                console.log(json.data);
                $('#content').text(json.data[0].content);
                $('#name').text(json.data[0].name);
                $('#id_post').val(json.data[0].post_id);
                $('#id_parent').val(json.data[0].id);
                $('form .displaycomment').show();
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been retrieved.",
                    icon: "error"
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    // function editComment(pk){
    //     $.ajax({
    //         url : "/editcomment/"+pk+"/",
    //         type: 'POST',
    //         data: $("#form").serialize(),
    //         success : function(json) {
    //             swal({
    //                 title: "Success!",
    //                 text: "The comment has been edited.",
    //                 icon: "success"
    //             });
    //             $('#id_id').val("");
    //             $('#id_content').val("");
    //             $('#id_name').val("");
    //             $('#id_status').val("");
    //             $('#id_email').val("");
    //             $('#id_website').val("");
    //             $('#commentChanges').modal('dispose');
    //         },
    //         error : function(xhr, errmsg, err) {
    //             swal({
    //                 title: "Error!",
    //                 text: "An error has occurred. The comment has not been edited.",
    //                 icon: "error"
    //             });
    //             console.log(xhr.status + ": " + xhr.responseText);
    //         }
    //     });
    // };

    // $("#form").submit(function(e){
    //     e.preventDefault();
    //     $.ajax({
    //         url : "/comments/",
    //         type: 'POST',
    //         data: $("#form").serialize(),
    //         success : function(json) {
    //             swal({
    //                 title: "Success!",
    //                 text: "The comment has been added.",
    //                 icon: "success"
    //             });
    //         },
    //         error : function(xhr, errmsg, err) {
    //             swal({
    //                 title: "Error!",
    //                 text: "An error has occurred. The comment has not been edited.",
    //                 icon: "error"
    //             });
    //             console.log(xhr.status + ": " + xhr.responseText);
    //         }
    //     });
    // });

});