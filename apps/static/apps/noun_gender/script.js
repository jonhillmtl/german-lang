$(document).ready(function()
{
    var current_noun = null;

    refresh_stats();
    get_noun();

    function update_correction_colors(gender)
    {
        var controls = [$("#id_correction_text"), $("#id_correction_correct")];

        for(index = 0; index < controls.length; index++)
        {
            text = controls[index];
            text.removeClass('gender_text_f');
            text.removeClass('gender_text_m');
            text.removeClass('gender_text_n');

            text.addClass('gender_text_' + gender);
        }
    }

    $("#id_neutral_answer").click(function(){
        submit_answer('n');
    });

    $("#id_feminine_answer").click(function(){
        submit_answer('f');
    });

    $("#id_masculine_answer").click(function(){
        submit_answer('m');
    });
    
    $('#id_correction_text').keyup(function(e)
    {
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    $('#id_correction_text').bind("enterKey", function(e)
    {
        var url = 'http://0.0.0.0:8080/api/nouns/gender/correction/';
        $.post({
            url: url,
            success: function(data)
            {
                if(data.success)
                {
                    refresh_stats();
                    get_noun();

                    $("#id_correction_overlay").hide();
                }
                else
                {
                    $("#id_correction_text").val('')
                    $("#id_correction_text").focus();
                }
            },
            data: JSON.stringify(
                {
                    'noun_id': current_noun.id,
                    'correction': $("#id_correction_text").val()
                }
            )
        });
    });

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

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_gender';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                $("#id_singular_span").html(data.noun.singular_form);
                $("#id_plural_span").html(data.noun.plural_form);
                $("#id_translation_span").html(data.noun.translations_text);
                current_noun = data.noun;
                console.log(data.choice_mode)
            }
        });
    }

    function submit_answer(gender)
    {
        var url = 'http://0.0.0.0:8080/api/nouns/gender/check/';
        $.post({
            url: url,
            success: function(data)
            {
                if(data.correct)
                {
                    refresh_stats();
                    get_noun();
                }
                else
                {
                    update_correction_colors(data.correct_answer);
                    $("#id_correction_correct").html(data.correction_hint);
                    $("#id_correction_overlay").show();
                    $("#id_correction_text").val('')
                    $("#id_correction_text").focus();
                }
            },
            data: JSON.stringify(
                {
                    'noun_id': current_noun.id,
                    'gender': gender
                }
            )
        });
    }
});