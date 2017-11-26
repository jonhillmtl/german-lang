var authentication_token = '';

function init_authentication(token)
{
    authentication_token = token;
}

$(document).ready(function()
{
    $.ajaxSetup({
        headers:
        { 
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'),
            'Authorization': authentication_token,
            'Content-Type':'application/json'
        }
    });
});