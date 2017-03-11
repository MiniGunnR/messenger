$(function() {

    function loadContent(url) {
        $("#messages").load(url + ' #messages>*').hide().fadeIn('slow');
    }

    $(".thread_list").on('click', function(e) {
        e.preventDefault();

        var url = $(this).attr('href');

        history.pushState({}, '', url);
        loadContent(url);
    });

    $(window).on('popstate', function(e) {
        var url = location.pathname;
        loadContent(url);
    });

    $("#msg_form").on('submit', function(e) {
        e.preventDefault();

        var path = location.pathname;
        var arr = path.split('/');
        var other_user = arr[arr.length - 2];
        var url = '/' + other_user + '/send/'; // change this hardcoded URL when app is reusable
        var msg = $('#msg');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'msg': msg.val()
            },

            success: function(data) {
                console.log(data);
                $("#messages").append('<p>' + 'Me - ' + data.text + '</p><hr/>');
                msg.val('');
            }
        });
    });

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // -! using jQuery

});
