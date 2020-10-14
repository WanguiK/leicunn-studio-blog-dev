$(document).ready(function () {

    $('.form-group .article').trumbowyg({
        autogrow: true
    });

    function convertToSlug(Text) {
        return Text
            .toLowerCase()
            .replace(/[^\w ]+/g,'')
            .replace(/ +/g,'-');
    }

    $("#id_title").keyup(function(){
        var Text = $(this).val();
        Text = convertToSlug(Text);
        $("#id_slug").val(Text);
    });

    $("#selectCover").click(function() {
        var pk = $(".modal .modal-body input[type='radio']:checked").val();
        $('#id_cover').val(pk);
        $('#selectImage').modal('hide');
    });

});