$(document).ready(function()
{
    var article_mode = 'definite';
    var case_mode = 'nominative';
    var articled_key = case_mode + '_' + article_mode + '_singular';

    var current_noun = null;

    refresh_stats();
    get_noun();

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

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_gender';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                console.log(data.choice_mode);
                console.log(data.noun);
                current_noun = data.noun;
                console.log(articled_key);
                
                $("#id_singular_span").html(current_noun.singular_form);
                $("#id_plural_span").html(current_noun.plural_form);
                $("#id_translation_span").html(current_noun.translations_text);
                $("#id_correction_correct").html(current_noun.articled[articled_key]);
                $("#id_level").text(current_noun.level);
                $("#id_chapter").text(current_noun.chapter);
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
                    var controls = [$("#id_correction_correct"), $("#id_correction_text")];
                    update_colors(controls, current_noun.gender);
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