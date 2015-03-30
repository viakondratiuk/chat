function checkPassword(id1, id2) {
    var pass1 = document.getElementById(id1);
    var pass2 = document.getElementById(id2);

    if (pass1.value != pass2.value) {
        alert('Password mismatch! Please check your password.')
        return false;
    }

    if (pass1.value.length < 5) {
        alert('The password cannot be shorter than 5 symbols.')
        return false;
    }

    return true;
}

function toggleVisibility(id) {
    var e = document.getElementById(id);
    if (e.style.display == 'block') {
        e.style.display = 'none';
    } else {
        e.style.display = 'block';
    }
}

function addChatMessage(list) {
    $.each(list, function(k, v) {
        if ($('#m' + v.id).length == 0) {
            if (v.type == 'message' or v.type == 'system') {
                m = '<div id="m'+v.id+'"><span>['+v.datetime+']</span> <b>'+v.name+':</b> <span>'+v.message+'</span></div>';
            } else if (v.type == 'system') {
                m = '<div id="m'+v.id+'"><b>'+v.message+'</b></div>';
            } else if (v.type == 'news') {
                m = '<div id="m'+v.id+'"></div>';
            }
            $('#chat').append(m);
            document.getElementById('chat').scrollTop = 9999999;
        }
    });
}

function ping() {
    $.ajax({
        url: '/refresh',
        success: function(r) {
            if (r.message_list.length > 0) {
                addChatMessage(r.message_list)
            }
        }
    });
}

$(document).ready(function() {
    if ($('#chat').length) {
        document.getElementById('chat').scrollTop = 9999999;
        setInterval(ping, 1000);
    }

    $('#add_message').submit(function(e) {
        form = $(this);
        e.preventDefault();
        $.ajax({
            type: 'post',
            url: form.attr('action'),
            data: form.serialize(),
            success: function (r) {
                if (r.exec) {
                    //$('#chat').append('<div><b>'+r.exec+'</b></div>');
                    addChatMessage(r.exec);
                }
            }
        });
        $('#message').val('')
    });
})