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
        url: 'refresh',
        success: function(result) {
            $("#chat").append("<div>" + result.test + "</div>");
            document.getElementById('chat').scrollTop = 9999999;
        }
    });
}

$(document).ready(function() {
    setInterval(ping, 1000);
})
