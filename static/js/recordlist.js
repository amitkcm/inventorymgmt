
$(document).ready(function() { 
    $('.menu-content').hide();
    var auth_token = 'Token'+' '+localStorage.getItem('token');
    var is_manager = localStorage.getItem('is_manager') && localStorage.getItem('is_manager') ==1 ? true:false
    if(!localStorage.getItem('token')){
        $(window).attr("location", "http://localhost:8000/login/");
    }
    else{
        var inv_by_id = {};
        var to_approve_inv_by_id = {};
        if(localStorage.getItem('is_manager') && localStorage.getItem('is_manager') ==1)
            $('.inv_pending_menu').show();
        else
            $('.inv_pending_menu').hide();

        $('#logout_session').on("click",function(){
            window.localStorage.removeItem("token");
            window.localStorage.removeItem("is_manager");
            $(window).attr("location", "http://localhost:8000/login/");
        });
        $('.inv_menu').on("click",function(){
            $('.menu-content').hide();
            $('.nav-link').removeClass("active");
            $.ajax({
                url: "http://localhost:8000/inv/",
                type: 'GET',
                headers: {"Authorization": auth_token}
            }).done(function(data){
                $('#inventory_list').show();
                $('.inv_menu').addClass("active");
                $(".inventory_list tbody tr").remove();
                data.forEach(element => {
                    inv_by_id[element.id] = element;
                    if(element.status == "pending" && element.operation == "delete")
                        return;
                    $('.inventory_list tbody').append(
                            '<tr' +' '+ 'id='+element.id+' '+'>'+
                            '<td>' + element.product_id +
                            '</td><td>' + element.product_name +
                            '</td><td>' + element.vendor +
                            '</td><td>' + element.mrp + 
                            '</td><td>' + element.batch_number + 
                            '</td><td>' + element.quantity + 
                            '</td><td>' + element.status + 
                            '<td><button class="edit"' +'data-href ='+element.id+'>Edit</button></td>'+
                            '<td><button class="delete"' +'data-href ='+element.id+'>Delete</button></td>'+
                            '</td></tr>'
                        )
                });
                $('.table .edit').on('click',function(e){
                    let inv_id = $(this).attr('data-href');
                    $('.menu-content').hide();
                    $('.update_inventory').show();
                    var edit_inv = inv_by_id[inv_id];
                    $('.update_inventory .form-control').each(function(idx,el){
                        el.value = edit_inv[el.name] || '';
                    });
                    (function ($) {
                        $("#datepicker").datepicker();
            
                    })
                });
                $('.table .delete').on('click',function(e){
                    let self = this;
                    let inv_id = $(this).attr('data-href');
                    if(is_manager){
                        $.ajax({
                            url: "http://localhost:8000/inv/"+inv_id+'/',
                            type: 'DELETE',
                            headers: {"Authorization": auth_token}
                        }).done(function(data){
                            swal(
                                'Record Deleted!',
                                 "Record is sucessfully deleted",
                                'success'
                            ).then(res =>{
                                $(self).closest('tr').remove();
                            })
                            
                        })
                        .fail(function(e){
                            if(e.responseJSON && e.responseJSON.error)  
                                swal("Error", e.responseJSON.error, "error")
                            else if(e.responseText)
                                swal("Error", e.responseText, "error")
                            else if(e.statusText)
                                swal("Error", e.statusText, "error")
                        })
                    }
                    else{
                        $.ajax({
                            url: "http://localhost:8000/inv/"+inv_id+'/',
                            type: 'DELETE',
                            headers: {"Authorization": auth_token}
                        }).done(function(data){
                            swal('Request Created!',data.message,'success').then(res =>{
                                $(self).closest('tr').remove();
                            })
                            
                        })
                        .fail(function(e){
                            if(e.responseJSON && e.responseJSON.error)  
                                swal("Error", e.responseJSON.error, "error")
                            else if(e.responseText)
                                swal("Error", e.responseText, "error")
                            else if(e.statusText)
                                swal("Error", e.statusText, "error")
                        })
                    }
                 });
            })
            .fail(function(e){
                $('#inventory_list').hide();
                if(e.responseJSON && e.responseJSON.error)  
                    swal("Error", e.responseJSON.error, "error");
                else if(e.responseJSON && e.responseJSON.detail)
                    alert(e.responseJSON.detail);
            })

        });
        $('.inv_menu').click();
        $('.edit_form_save_details').on("click",function(e){               
            let fields = {};
            $('.update_inventory .form-control').each(function(idx,el){
                fields[el.name] = el.value || null;
            });
            var person = new Object();  
            person.product_id = 12;  
            person.product_name = "Kayal";
            $.ajax({  
                url: 'http://localhost:8000/inv/'+ fields.id+'/',  
                type: 'PATCH',  
                dataType: 'json',
                headers: {"Authorization": auth_token},
                data: fields,  
                success: function (data, textStatus, xhr) {  
                    console.log(data)
                    let msg = data && data.message?data.message:"You have successfully updated Inventory"
                    swal(
                        'Inventory Updated!',
                         msg,
                        'success'
                    )
                    .then(value =>{
                        $('.inv_menu').click();                        
                    })
                },  
                error: function (xhr, textStatus, errorThrown) {  
                    console.log('Error in Operation');  
                }  
            })
            .fail(function(e){
                if(e.responseJSON && e.responseJSON.error)  
                    swal("Error", e.responseJSON.error, "error")
                else if(e.responseText)
                    swal("Error", e.responseText, "error")
                else if(e.statusText)
                    swal("Error", e.statusText, "error")
            });
        });
        $('.inv_pending_menu').on("click", function(e){
            $('.menu-content').hide();
            $('.nav-link').removeClass("active");
            $('.inv_pending_menu').addClass("active");
            $.ajax({
                url: "http://localhost:8000/inv/",
                type: 'GET',
                headers: {"Authorization": auth_token}
            }).done(function(data){
                $('#to_approved_list').show();
                $("#to_approved_list tbody tr").remove();
                data.forEach(element => {
                    to_approve_inv_by_id[element.id] = element;
                    if(is_manager && element.status == "approved")
                        return;
                    $('#to_approved_list tbody').append(
                            '<tr' +' '+ 'id='+element.id+' '+'>'+
                            '<td>' + element.product_id +
                            '</td><td>' + element.product_name +
                            '</td><td>' + element.vendor +
                            '</td><td>' + element.mrp + 
                            '</td><td>' + element.batch_number + 
                            '</td><td>' + element.quantity + 
                            '</td><td>' + element.status + 
                            '</td><td>' + element.operation + 
                            '<td><button class="approved"' +'data-href ='+element.id+'>Approved</button></td>'+
                            '</td></tr>'
                        )
                });
                $('.table .approved').on('click',function(e){
                    let self = this;
                    let inv_id = $(this).attr('data-href');
                    let inv_record = to_approve_inv_by_id[inv_id];
                    if(inv_record && inv_record.operation =="delete"){
                        $.ajax({
                            url: "http://localhost:8000/inv/"+inv_id+'/',
                            type: 'DELETE',
                            headers: {"Authorization": auth_token}
                        }).done(function(data){
                            swal(' Request Approved!',"Record Deleted",'success').then(res =>{
                                $(self).closest('tr').remove();
                            })
                            
                        })
                    }
                    else
                        $.ajax({  
                            url: 'http://localhost:8000/inv/'+ inv_id+'/',  
                            type: 'PATCH',  
                            dataType: 'json',
                            headers: {"Authorization": auth_token},
                            data: {"status":"approved"},  
                            success: function (data, textStatus, xhr) {  
                                swal(
                                    'Approved!!!',
                                     'Your '+inv_by_id.operation +' request is approved',
                                    'success'
                                )
                                $(self).closest('tr').remove();
                            },  
                            error: function (xhr, textStatus, errorThrown) {  
                                console.log('Error in Operation');  
                            }  
                        });  
                    
                });
            })
            .fail(function(e){
                if(e.responseJSON && e.responseJSON.error)  
                    swal("Error", e.responseJSON.error, "error")
                else if(e.responseText)
                    swal("Error", e.responseText, "error")
                else if(e.statusText)
                    swal("Error", e.statusText, "error")
            });
        });

        $('#add_inventory').on("click",function(){
            $('.menu-content').hide();
            $('.add_inventory').show();
            var date=new Date();
            alert.log("eeeee")
            $('.add_inventory .form-control').each(function(idx,el){

                console.log('el',el)
                el.value = '';
            });
        })
        $('.create_inventory').on("click",function(e){               
            let fields = {};
            $('.add_inventory .form-control').each(function(idx,el){
                fields[el.name] = el.value || null;
            });
            if(is_manager)
                fields.status = "approved";
            fields.operation = "create";
            $.ajax({  
                url: 'http://localhost:8000/inv/',  
                type: 'POST',  
                dataType: 'json',
                headers: {"Authorization": auth_token},
                data: fields,  
                success: function (data, textStatus, xhr) {  
                    let msg = data && data.message?data.message:"You have successfully created Inventory"
                    swal(
                        'Inventory Created!',
                         msg,
                        'success'
                    ).then(value =>{
                        $(window).attr("location", "http://localhost:8000/recordlist/");               
                    })
                },  
                error: function (xhr, textStatus, errorThrown) {  
                    console.log('Error in Operation');  
                }  
            })
            .fail(function(e){
                if(e.responseJSON && e.responseJSON.error)  
                    swal("Error", e.responseJSON.error, "error")
                else if(e.responseText)
                    swal("Error", e.responseText, "error")
                else if(e.statusText)
                    swal("Error", e.statusText, "error")
            })
        });
    } 
});
