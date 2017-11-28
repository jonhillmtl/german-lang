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

function update_colors(controls, gender)
{
    for(index = 0; index < controls.length; index++)
    {
        // TODO JHILL: factor that class up into a different css file
        text = controls[index];
        text.removeClass('gender_text_f');
        text.removeClass('gender_text_m');
        text.removeClass('gender_text_n');

        text.addClass('gender_text_' + gender);
    }
}

// TODO JHILL: mode, of course
function refresh_stats()
{
    url = 'http://0.0.0.0:8080/api/nouns/gender/stats/';
    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(data)
        {
            $("#id_mode_percentage").text(data.mode_percentage);
            $("#id_all_time_percentage").text(data.all_time_percentage);
            $("#id_last_24h_percentage").text(data.last_24h_percentage);
            $("#id_mode_last_24h_percentage").text(data.mode_last_24h_percentage);
        }
    });
}

