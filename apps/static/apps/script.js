$(document).ready(function()
{
    var headers =
    { 
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'),
        'Authorization': $.cookie('authentication_token'),
        'Content-Type':'application/json'
    };

    $.ajaxSetup({
        headers
    });
    
    update_time();
});

var current_time = 0;
function update_time()
{
    setInterval(function () 
    {
        current_time += 1;
        var minutes = Math.floor(current_time / 60);
        var seconds = current_time % 60;
        
        var time = minutes + "m " + seconds + "s";
        $("#id_total_time").text(time);
    
        var correct_minute = current_time / 60;
        $("#id_correct_minute").text(correct_count / correct_minute);
    }, 1000);
}

function update_colors(controls, gender)
{
    for(index = 0; index < controls.length; index++)
    {
        // TODO JHILL: factor that class up into a different css file
        control = controls[index];
        control.removeClass('gender_text_f');
        control.removeClass('gender_text_m');
        control.removeClass('gender_text_n');
        control.removeClass('gender_text_p');

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
    else if(gqm_type == 'adjective')
    {
        post_data['adjective_id'] = current_gqm.id;
    }
    else if(gqm_type == 'phrase')
    {
        post_data['phrase_id'] = current_gqm.id;
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

function refresh_metadata(current_gqm)
{
    $("#id_level").text(current_gqm.level);
    $("#id_chapter").text(current_gqm.chapter);
}

var correct_count = 0;
var total_count = 0;

function increment_count(correct)
{
    total_count += 1;
    if(correct)
    {
        correct_count += 1;
    }
    
    $("#id_correct_count").text(correct_count);
    $("#id_total_count").text(total_count);
}

