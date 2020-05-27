$(document).ready(function(){

    var width = $('#cover-image').width();
    var height = (0.36 * width) / 0.64;
    $('#cover-image').height(height);

    var cardwidth = $('.card').width();
    $('.card').height(cardwidth);

    $('.materialboxed').materialbox();

    $('#facebookShare').click(function () {
        FB.ui({
            method: 'share',
            href: $(this).attr('href'),
        }, function (response) { });
    });

    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault()

        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top,
        },
            500, 'linear'
        );
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

    $("#discuss form").submit(function(e){
        e.preventDefault();
        $.ajax({
            url: $(location).attr('href'),
            type: 'POST',
            data: $("#discuss form").serialize(),
            success : function(json) {
                swal({
                    title: "Success!",
                    text: "The comment has been added and will be displayed once approved.",
                    icon: "success"
                });
                $('#id_content').val('');
                $('#id_name').val('');
                $('#id_email').val('');
                $('#id_website').val('');
                $('.chips').hide();
            },
            error : function(xhr, errmsg, err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The comment has not been added.",
                    icon: "error"
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });

    $('.chips').chips();

    $('.reply').click(function () {
        // $('.thechip').hide();
        var reply_to = $(this).attr('id');
        $('#id_parent').val(reply_to);
        var link = '#name'+reply_to;
        var name = $(link).text();
        var chip_to_add = "<a href='" + link + "' class='thechip'><div class='chip lato'><i class='material-icons'>reply</i>Reply to: " + name + "</div></a>";
        $('#discuss .col .row form').before(chip_to_add).fadeIn(3000);

    });

});