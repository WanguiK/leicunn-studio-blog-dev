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

    // function display(input) {
    //     if (input.files && input.files[0]) {
    //        var reader = new FileReader();
    //        reader.onload = function(event) {
    //           $('#display').attr('src', event.target.result);
    //        }
    //        reader.readAsDataURL(input.files[0]);
    //     }
    // }

    // var imageText = $("#id_cover option:selected").text();
    // var cover = 'http://'+location.hostname+':8000/media/'+imageText;
    // // var cover = location.hostname+'/media/'+imageText;
    // $(function(){
    //     display(cover);
    //     // alert(cover);
    // });

    // $('#id_cover').change(function() {
    //     var imageurl = $(this).find(":selected").text();
    //     var url = 'http://'+location.hostname+':8000'+imageurl;
    //     // var url = location.hostname+imageurl;
    //     console.log(url);
    //     display(imageurl);
    // });

});