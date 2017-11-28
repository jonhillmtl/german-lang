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

var verb_translation_multi_url = null;
var verb_random_url = null;

var noun_translation_multi_url = null;
var noun_random_url = null;

function init_urls(
    verb_translation_multi,
    verb_random,
    noun_translation_multi,
    noun_random
)
{
    verb_translation_multi_url = verb_translation_multi;
    verb_random_url = verb_random;

    noun_translation_multi_url = noun_translation_multi;
    noun_random_url = noun_random;
}

var current_gqm = null;
var current_gqm_type = null;

function check_translation_multi_answer(translation_id, callback)
{
    url = '';
    post_data = {
        'translation_id': translation_id
    }
    
    if(current_gqm_type == 'verb')
    {
        url = verb_translation_multi_url;
        post_data['verb_id'] = current_gqm.id;
    }
    else if(current_gqm_type == 'noun')
    {
        url = verb_translation_multi_url;
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

function get_gqm(type, mode, callback)
{
    url = '';
    if(type == 'verb')
    {
        url = verb_random_url;
    }
    else if(type == 'noun')
    {
        url = noun_random_url;
    }

    url = url + '?mode=' + mode;

    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function(data)
        {
            current_gqm = data[type];
            current_gqm_type = type;
            callback(data);
        }
    });
}

