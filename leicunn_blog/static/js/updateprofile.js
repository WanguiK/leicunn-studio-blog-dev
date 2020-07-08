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

});