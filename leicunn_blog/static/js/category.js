$(document).ready(function () {

    function convertToSlug(Text) {
        return Text
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-');
    }

    $("#id_category").keyup(function(){
        var Text = $(this).val();
        Text = convertToSlug(Text);
        $("#id_slug").val(Text);
    });

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
            text: "Are you sure you want to delete the category titled '"+ title +"'? All blog posts associated with this category will also be deleted and once deleted, you will not be able to recover them!",
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
                    text: "Your category is safe.",
                    icon: "info",
                    buttons: false,
                    timer: 3500
                });
            }
        });

    });

    function deletePost(pk){
        $.ajax({
            url : "/cat/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#cat'+pk).hide();
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
        var pk = $("input[type='radio']:checked").val();
        window.location.href = "/editcat/"+pk+"/";
    });

});