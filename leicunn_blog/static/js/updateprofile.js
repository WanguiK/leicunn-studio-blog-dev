$(document).ready(function () {

    $('#id_article').trumbowyg({
        autogrow: true
    });

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


    // Author creating a comment
    $('form#opinion').submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/authoraddopinion/',
            type: 'POST',
            data: $(this).serialize(),
            success : function(json) {
                swal({
                    title: "Success!",
                    text: "The comment has been posted.",
                    icon: "success",
                    buttons: false,
                    timer: 3000
                });
                $('#opinion #id_content').val('');
                $('#opinion #id_status')[0].selectedIndex = 0;
                $('#opinion').modal('hide');
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