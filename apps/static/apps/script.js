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
        control = controls[index];
        control.removeClass('gender_text_f');
        control.removeClass('gender_text_m');
        control.removeClass('gender_text_n');

        control.addClass('gender_text_' + gender);
    }
}

// TODO JHILL: mode, of course
function refresh_stats(mode, gqm_type)
{
    return;
    
    // TODO JHILL: make this configurable
    url = 'http://0.0.0.0:8080/api/stats?mode={}&gqm_type={}';
    url = url.format(mode, gqm_type);

    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(data)
        {
            $("#id_mode_percentage").text(data.mode_percentage);
            $("#id_all_time_percentage").text(data.all_time_percentage);
        }
    });
}

var verb_translation_multi_url = null;
var verb_random_url = null;
var verb_pp_multi_url = null;

var noun_translation_multi_url = null;
var noun_random_url = null;

function init_urls(
    verb_translation_multi,
    verb_random,
    noun_translation_multi,
    noun_random,
    verb_pp_multi
)
{
    verb_translation_multi_url = verb_translation_multi;
    verb_random_url = verb_random;

    noun_translation_multi_url = noun_translation_multi;
    noun_random_url = noun_random;

    verb_pp_multi_url = verb_pp_multi;
}

var current_gqm = null;

function check_translation_multi_answer(url, answer, gqm_type, mode, callback)
{
    post_data = {
        'answer': answer,
    }
    
    if(gqm_type == 'verb')
    {
        post_data['verb_id'] = current_gqm.id;
    }
    else
    {
        post_data['noun_id'] = current_gqm.id;
    }

    $.post({
        url: url,
        success: function(data)
        {
            callback(data);
        },
        data: JSON.stringify(post_data)
    });
}

function get_gqm(url, type, mode, callback)
{
    url = url + '?mode=' + mode;

    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(data)
        {
            current_gqm = data[type];
            callback(data);
        }
    });
}

