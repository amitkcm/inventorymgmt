
$(document).ready(function() {
    $(".loginForm").click(function(e) {
       e.preventDefault();
       if ($("#username").val() != '' && $("#password").val() != '') {
            $.ajax({ 
                url: 'http://localhost:8000/token/', 
                type: 'POST', 
                data: {username: $("#username").val(), password: $("#password").val()} ,
                dataType: 'json',
            }).done(function (data) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('is_manager', data.is_manager);
                if(data.token)
                    $(window).attr("location", "http://localhost:8000/recordlist/");
                else
                    alert("Token Not Found")
            })
            .fail(function(e){
                if(e.responseJSON && e.responseJSON.error)  
                    alert(e.responseJSON.error)
            })
        }
        else
            alert("Username or Password can't be blank")
    });
    $('#password').keypress(function (e) {
        console.log("keypress")
        if (e.which == 13) {
            $(".loginForm").click();
        }
      });
 });
