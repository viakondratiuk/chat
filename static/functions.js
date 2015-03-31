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

function addChatMessage(r) {
    if (r.messages) {
        $.each(r.messages, function(k, v) {
            if ($('#m' + v.id).length == 0) {
                if (v.type == 'message') {
                    m = '<div id="m'+v.id+'"><span>['+v.datetime+']</span> <b>'+v.name+':</b> <span>'+v.message+'</span></div>';
                } else if (v.type == 'system') {
                    m = '<div id="m'+v.id+'"><b>'+v.message+'</b></div>';
                } else if (v.type == 'news') {
                    m = '<div id="m'+v.id+'"></div>';
                } else if (v.type == 'command') {
                    m = '<div class="command"><b>'+v.name+':</b> <span>'+v.message+'</span></div>';
                } else if (v.type = 'search') {
                    m = '<div class="search"><span>['+v.datetime+']</span> <b>'+v.name+':</b> <span>'+v.message+'</span></div>';
                }
                $('#chat').append(m);
                document.getElementById('chat').scrollTop = 9999999;
            }
        });
    }
}

function ping() {
    $.ajax({
        url: '/refresh',
        success: function(r) {
            addChatMessage(r)
        }
    });
}

function clearChat() {
    $('#chat').html('');
    $('#message').val('')
    return false;
}

$(document).ready(function() {
    if ($('#chat').length) {
        document.getElementById('chat').scrollTop = 9999999;
        setInterval(ping, 1000);
    }

    $('#process_message').submit(function(e) {
        if ($('#message').val() == '/clear') {
            return clearChat();
        }

        e.preventDefault();
        $.ajax({
            type: 'post',
            url:  $(this).attr('action'),
            data:  $(this).serialize(),
            success: function (r) {
                addChatMessage(r);
            }
        });
        $('#message').val('')
    });
})