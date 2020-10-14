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
        var titleid = "#title"+pk;
        var title = $(titleid).text();

        swal({
            title: "Warning!",
            text: "Are you sure you want to delete the blog post titled '"+ title +"'? Once deleted, you will not be able to recover it!",
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
                    text: "Your blog post is safe.",
                    icon: "info",
                    buttons: false,
                    timer: 3500
                });
            }
        });

    });

    function deletePost(pk){
        $.ajax({
            url : "/post/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#post'+pk).hide();
                swal({
                    title: "Success!",
                    text: "The blog post has been deleted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
            },

            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The blog post has not been deleted.",
                    icon: "error"
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    $("#edit").click(function() {
        var pk = $("input[type='radio']:checked").val();
        window.location.href = "/editpost/"+pk+"/";
    });


    var pk = '';
    $(".addcomment").click(function() {
        var elem = $(this).parents('tr').attr('id');
        pk = elem.replace("post", "");
        display_post(pk);
    });


    // Display post details before adding comment
    function display_post(pk){
        $.ajax({
            url : "/getpost/"+pk+"/",
            type: 'GET',
            dataType: 'json',
            success : function(json) {
                console.log(json.data);
                $('#title').text(json.data[0].title);
                $('#summary').text(json.data[0].summary);
                $('#commentModal form .displaypost').show();
                $('#commentModal').modal('show');
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The post has not been retrieved.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    // Author creating a comment
    $('#commentModal form').submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/authoraddcomment/' + pk + '/',
            type: 'POST',
            data: $(this).serialize(),
            success : function(json) {
                swal({
                    title: "Success!",
                    text: "The comment has been posted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
                $('#commentModal #id_content').val('');
                $('#commentModal #id_status')[0].selectedIndex = 0;
                $('#commentModal').modal('hide');
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been added.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

});