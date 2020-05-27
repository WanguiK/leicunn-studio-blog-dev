$(document).ready(function () {

    $('#id_article').trumbowyg({
        autogrow: true
    });

    $("#selectCover").click(function() {
        var pk = $(".modal .modal-body input[type='radio']:checked").val();
        $('#id_image').val(pk);
        $('#selectImage').modal('hide');
    });

});