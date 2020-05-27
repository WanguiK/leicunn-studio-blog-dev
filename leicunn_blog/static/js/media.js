$(document).ready(function () {

    function display(input) {
        if (input.files && input.files[0]) {
           var reader = new FileReader();
           reader.onload = function(event) {
              $('#display').attr('src', event.target.result);
           }
           reader.readAsDataURL(input.files[0]);
        }
    }
     
    $("#id_image").change(function() {
        display(this);
    });

    function convertToSlug(Text) {
        return Text
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-');
    }

    $("#id_description").keyup(function(){
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

    $("#edit").click(function() {
        if($("input[type='radio']").is(':checked')) {
            var pk = $("input[type='radio']:checked").val();
            window.location.href = "/editmedia/"+pk+"/";
        } else {
            swal({
                title: "Error!",
                text: "You have not selected an image to edit.",
                icon: "error"
            });
        }
        
    });

    $("#delete").click(function() {

        if($("input[type='radio']").is(':checked')) {
            
            var pk = $("input[type='radio']:checked").val();
            var mediaId = "#media"+pk+" .card .card-body label";
            var media = $(mediaId).text();
            console.log("Media ID: "+pk+"\n\n");

            swal({
                title: "Warning!",
                text: "Are you sure you want to delete the media captioned '"+ media +"'? Once deleted, you will not be able to recover it!",
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
                        text: "Your media item is safe.",
                        icon: "info"
                    });
                }
            });

        } else {
            swal({
                title: "Error!",
                text: "You have not selected an image to delete.",
                icon: "error"
            });
        }
    });

    function deletePost(pk){
        $.ajax({
            url : "/media/delete/"+pk+"/",
            method: 'post',
            success : function(json) {
                $('#media'+pk).hide();
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
    }

});