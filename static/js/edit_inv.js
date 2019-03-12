
$(document).ready(function() {
    var url = window.location.pathname;
    var id = url.substring(url.lastIndexOf('/') - 1);
    $.ajax({
        url: "http://localhost:8000/inv/"+id,
        type: 'GET',
        headers: {"Authorization": 'Token 55b0e86cef72c41914ec493f5f0fb7e8e7728285'}
      }).done(function(data){
          console.log(data)
          
          })
    
      .fail(function(e){
        if(e.responseJSON && e.responseJSON.error)  
            alert(e.responseJSON.error)
    })
});
