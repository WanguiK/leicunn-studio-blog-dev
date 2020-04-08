$(document).ready(function () {

    $('.form-group .article').trumbowyg({
        autogrow: true
    });

    function display(input) {
        if (input.files && input.files[0]) {
           var reader = new FileReader();
           reader.onload = function(event) {
              $('#display').attr('src', event.target.result);
           }
           reader.readAsDataURL(input.files[0]);
        }
    }
     
    $("#id_cover").change(function() {
        display(this);
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

});