$(document).ready(function() {
    $('.toast').toast('show');

    $('#exampleModalCenter').on('show.bs.modal', function(event) {
        var cardFrom = $(event.relatedTarget) // Button that triggered the modal
        var itemData = cardFrom.data('whatever') // Extract info from data-* attributes
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: '/manage_sy/modal/item-detail/',
            type: 'POST',
            data: {
                id: itemData,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                $('.modal-content').html(response);
            },
            error: function() {
                console.log('something went wrong here');
            },
        });
    })

    $('#modalnewitemform').on('show.bs.modal', function(event) {
        backdrop: 'static'

            var cardFrom = $(event.relatedTarget) // Button that triggered the modal
        var itemData = cardFrom.data('whatever') // Extract info from data-* attributes
        var apologytype = cardFrom.data('apologytype') // Extract info from data-* attributes
        var url = '/manage_sy/modal/item-new/' + apologytype + '/'
        var mtype = 'POST'
        if (itemData != null) {
            url = '/manage_sy/modal/item-edit/' + itemData + '/'
            mtype = 'GET'
        }
        console.log('URL now is: ' + url);
        console.log('Method is now is: ' + mtype);
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: url,
            type: mtype,
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response) {
                console.log(response)
                $('#new-item-form').html(response);
            },
            error: function() {
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

    // $(document).on('mousedown', '.addctrlplus', function () {
    //     console.log("in the div..........")
    //     $(this).find("#addctrlfaceddev").show();
    //     // $(this).find("#addctrlplus").hide();
    // });


    $('#closeButton').on('click', function(event) {
        $("#addctrlfaceddev").slideUp();

    })
    $('.addctrlplus').on('click', function(event) {
        $("#addctrlfaceddev").slideDown(600);
    })

    $(document).click(function(e) {
        console.log('targets is' + e.target.parentNode.parentNode.parentNode.id)
        var container = 'addctrlplus'
            // if the target of the click isn't the container nor a descendant of the container
        if (!(container == e.target.parentNode.parentNode.parentNode.id) && !$(e.target).hasClass("addctrlplus") &&
            $(e.target).parents(".addctrlfaceddev").length === 0) {
            $(".addctrlfaceddev").slideUp();
        }
    });


    $("#inv_code_copy").click(function(e) {
        var result = copyToClipboard($("#inv_code").text());
        if (result == true) {
            $("#inv_code_copy").html().split("<sub> copied to clipboard</sub>", "").join("");
            $("#inv_code_copy").html('<i class="fas fa-paste" ></i><sub> <small>copied to clipboard</small></sub>')
        }
    });

    if (window.location.href.indexOf('#inv_code') != -1) {
        $('#modelWindow').modal('show');
    }

    function copyToClipboard(text) {
        if (window.clipboardData && window.clipboardData.setData) {
            // IE specific code path to prevent textarea being shown while dialog is visible.
            return clipboardData.setData("Text", text);

        } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
            var textarea = document.createElement("textarea");
            textarea.textContent = text;
            textarea.style.position = "fixed"; // Prevent scrolling to bottom of page in MS Edge.
            document.body.appendChild(textarea);
            textarea.select();
            try {
                return document.execCommand("copy"); // Security exception may be thrown by some browsers.
            } catch (ex) {
                console.warn("Copy to clipboard failed.", ex);
                return false;
            } finally {
                document.body.removeChild(textarea);
            }
        }
    }


});


function checkNewEditCancel() {
    var ret = confirm('Do you really want to close before sending!?');
    if (ret) {
        $('#modalnewitemform').modal('hide');
        return true;
    } else {
        $('#modalnewitemform').modal('show');
        return false;
    }
}



function signup_by_inv_code() {
    inv_code = document.getElementById("signup-by-inv-code").value;
    var action_src = "/manage_sy/signup-bycode/" + inv_code;
    var currentPath = window.location.href
    var signup_by_inv_code_form = document.getElementById('signup_by_inv_code_form');
    signup_by_inv_code_form.action = action_src;
    return true;
}