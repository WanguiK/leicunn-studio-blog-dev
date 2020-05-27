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
                    icon: "info"
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
                    icon: "success"
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

});