$(document).ready(function(){
    $('.toast').toast('show');

    $('#exampleModalCenter').on('show.bs.modal', function (event) {
        var cardFrom = $(event.relatedTarget) // Button that triggered the modal
        var itemData = cardFrom.data('whatever') // Extract info from data-* attributes
        var csrftoken = getCookie('csrftoken');
         $.ajax({
                    url:'/manage_sy/modal/item-detail/',
                    type:'POST',
                    data: {id:itemData,
                            csrfmiddlewaretoken:csrftoken
                            },
                    success:function(response){
                         $('.modal-content').html(response);
                    },
                    error:function(){
                        console.log('something went wrong here');
                    },
          });
    })

    $('#modalnewitemform').on('show.bs.modal', function (event) {
    backdrop: 'static'

    var cardFrom = $(event.relatedTarget) // Button that triggered the modal
    var itemData = cardFrom.data('whatever') // Extract info from data-* attributes
    var url = '/manage_sy/modal/item-new/'
    var mtype = 'POST'
    if (itemData != null){
        url = '/manage_sy/modal/item-edit/'+itemData+'/'
        mtype = 'GET'
    }
    console.log('URL now is: '+url);
    console.log('Method is now is: '+mtype);
    var csrftoken = getCookie('csrftoken');
    $.ajax({
                url:url,
                type:mtype,
                data: {csrfmiddlewaretoken:csrftoken
                        },
                success:function(response){
                    console.log(response)
                     $('#new-item-form').html(response);
                },
                error:function(){
                    console.log('something went wrong here');
                },
      });
    })



    $('#id_date_of_birth').datepicker({
        clearBtn: true,
        autoclose: true
    });





    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
        }
        return cookieValue;
    }


});


function checkNewEditCancel(){
    var ret =  confirm('Do you really want to close before sending!?');
    if(ret){
         $('#modalnewitemform').modal('hide');
         return true;
    }else{
         $('#modalnewitemform').modal('show');
         return false;
    }
}
