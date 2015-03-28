function comparePasswords(id1, id2) {
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

function ping() {
    $.ajax({
        url: 'refresh?time=' + $.now(),
        success: function(result) {
            if (result.message_list.length > 0) {
                $.each(result.message_list, function(k, v) {
                    $('#chat').append('<div><span>['+v.datetime+']</span> <b>'+v.name+':</b> <span>'+v.message+'</span></div>');
                    document.getElementById('chat').scrollTop = 9999999;
                });
            }
        }
    });
}

$(document).ready(function() {
    if ($('#chat').length) {
        document.getElementById('chat').scrollTop = 9999999;
        setInterval(ping, 1000);
    }
})
