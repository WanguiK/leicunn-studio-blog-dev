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

    $(".dropdown-item.delete").click(function() {
        var nid = $(this).find('span').text();
        delete_notif(nid);
    });

    function delete_notif(pk){
        var name = "table tbody tr.notif"+pk;
        $.ajax({
            url: "/deletenotif/",
            method: "POST",
            data: {
                pk: pk
            },
            success:  function(){
                $(name).hide();
                swal({
                    title: "Success!",
                    text: "The notification has been deleted.",
                    icon: "success",
                    buttons: false,
                    timer: 3500
                });
            },
            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "An error has occurred. The notification has not been deleted.",
                    icon: "error",
                    buttons: false,
                    timer: 3500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    };


    // View button
    $(".dropdown-item.view").click(function() {
        var next = $(this).attr('href');
        changeReadStatus(this, next);
    });

    // Mark as read button
    $(".dropdown-item.status").click(function() {
        var next = 'r';
        changeReadStatus(this, next);
    });

    function changeReadStatus(loc, next) {
        var current = $(loc).find('span').text();
        var className = $(loc).parents('tr').attr('class');
        var nid = className.replace('notif','');
        if (next == 'r') { //mark as
            if (current == 0) {
                status_notif(nid, 1, next);
            } else {
                status_notif(nid, 0, next);
            }
        } else { // view
            if (current == 0) {
                status_notif(nid, 1, next);
            } else {
                location.href = next;
            }
        }
    }

    function status_notif(pk, status, next){
        $.ajax({
            url: "/notifstatus/",
            method: "POST",
            data: {
                pk: pk,
                status: status
            },
            success:  function(){
                if (next == 'r') {
                    location.reload(true);
                } else {
                    location.href = next;
                }
            },
            error : function(xhr,errmsg,err) {
                swal({
                    title: "Error!",
                    text: "Cannot 'Mark as read'.",
                    icon: "error",
                    buttons: false,
                    timer: 2500
                });
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });

    };

});