    function send_code() {
        if (document.getElementById('state').value == 'code') {
        $.ajax({
          type: "POST",
          url: '/send_code',
          data: {"username": document.getElementById('username').value, "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value, "action": "create"},
          success: function(data) {
            if (data['success']) {
                document.getElementById('code').hidden = false;
                document.getElementById('enter').firstChild.data = "Вход";
                document.getElementById('state').value = "verify";
            } else {
                const p = document.getElementById('message');
                p.firstChild.data = data['message'];
            }
        }});
        } else {
        $.ajax({
          type: "POST",
          url: '/send_code',
          data: {"username": document.getElementById('username').value, "code": document.getElementById('code').value, "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value, "action": "check"},
          success: function(data) {
            if (data['success']) {
                window.location.href = '/';
            } else {
                p.firstChild.data = data['message'];
            }
            },
        });
        }
    }