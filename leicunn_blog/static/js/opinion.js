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

    $("#reply").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            display_comment(pk);
        } else {
            swal({
                title: "Error!",
                text: "You have not selected a comment to reply to.",
                icon: "error",
                buttons: false,
                timer: 3500
            });
        }

    });

    function display_comment(pk){
        $.ajax({
            url : "/getopinion/"+pk+"/",
            type: 'GET',
            dataType: 'json',
            success : function(json) {
                console.log(json.data);
                $('#content').text(json.data[0].content);
                $('#name').text(json.data[0].name);
                $('#replyModalTitle').text("Reply To @" + json.data[0].name);
                $('#replyModal form .displaycomment').show();
                $('#replyModal').modal('show');
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been retrieved.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $("#delete").click(function() {
        var pk = $("input[type='radio']:checked").val();
        var titleid = "#commenter"+pk;
        var commenter = $(titleid).text();

        if (pk == null) {
            swal({
                title: "Error!",
                text: "You have to select a comment to delete.",
                icon: "error",
                buttons: false,
                timer: 3500
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
                        icon: "info",
                        buttons: false,
                        timer: 3500
                    });
                }
            });
        }

    });

    function deleteComment(pk){
        $.ajax({
            url : "/opinion/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#comment'+pk).hide();
                swal({
                    title: "Success!",
                    text: "The comment has been deleted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
            },
            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been deleted.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $('#replyModal form').submit(function(e){
        e.preventDefault();
        var pk = $("input[type='radio']:checked").val();
        $.ajax({
            url: '/replyopinion/' + pk + '/',
            type: 'POST',
            data: $(this).serialize(),
            success : function(json) {
                swal({
                    title: "Success!",
                    text: "The reply has been posted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
                location.reload(true);
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The reply has not been added.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });


    $("#edit").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            display_edit_comment(pk);
        } else {
            swal({
                title: "Error!",
                text: "You have not selected a comment to edit.",
                icon: "error",
                buttons: false,
                timer: 3500
            });
        }

    });


    function checkIfReply(reply) {
        $('#thereply').show();
        $('#thereply #name').text("@" + reply[0].name);
        $('#thereply #content').text('"' + reply[0].content + '"');
    }


    function display_edit_comment(pk){
        $.ajax({
            url : "/geteditopinion/"+pk+"/",
            type: 'GET',
            dataType: 'json',
            success : function(json) {
                if (json.reply.length != 0) {
                    checkIfReply(json.reply);
                }

                $('#title').text(json.title);
                $('#editModal #id_content').val(json.data[0].content);
                $('#editModal #id_name').val(json.data[0].name);
                $('#editModal #id_email').val(json.data[0].email);
                $('#editModal #id_website').val(json.data[0].website);
                $('#editModal #id_status').val(json.data[0].status);
                $('#editModal #id_image').val(json.data[0].image);
                $('#editModal #id_author').val(json.data[0].author);
                $('#editModal #id_post').val(json.data[0].post);
                $('#editModal #parent').val(json.data[0].parent);
                $('#editModalTitle').text("Edit Comment From @" + json.data[0].name);
                $('#editModal form .displaycomment').show();
                $('#editModal').modal('show');
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been retrieved.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $('#editModal form').submit(function(e){
        e.preventDefault();
        var pk = $("input[type='radio']:checked").val();
        $.ajax({
            url: '/editopinion/' + pk + '/',
            type: 'POST',
            data: $(this).serialize(),
            success : function(json) {
                swal({
                    title: "Success!",
                    text: "The reply has been edited.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
                location.reload(true);
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The reply has not been edited.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

});