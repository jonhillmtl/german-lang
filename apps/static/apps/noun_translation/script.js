$(document).ready(function()
{
    var current_noun = null;
    var correction = false;

    get_noun();

    $('#id_translation_text').bind("enterKey", function(e)
    {
        var url = 'http://0.0.0.0:8080/api/nouns/translation/check/';

        $.post({
            url: url,
            success: function(data)
            {
                console.log(data);
                if(data.correct)
                {
                    correction = false;
                    get_noun();
                }
                else
                {
                    $("#id_plural_span").html(current_noun.gendered_nominative_plural);
                    $("#id_translation_text").val('');
                    $("#id_translation_text").focus();
                    $("#id_translation_span").html(current_noun.translations_text);
                    correction = true;
                }
            },
            data: JSON.stringify(
                {
                    'noun_id': current_noun.id,
                    'translation': $(this).val(),
                    'correction': correction
                }
            )
        });
    });

    $('#id_translation_text').keyup(function(e)
    {
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_translation';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_noun = data.noun;
                console.log(data);

                var controls = [$("#id_plural_span"), $("#id_singular_span")];
                update_colors(controls, current_noun.gender);

                $("#id_singular_span").html(current_noun.gendered_nominative_singular);
                $("#id_plural_span").html(current_noun.gendered_nominative_plural);

                $("#id_translation_text").val('');
                $("#id_translation_text").focus();
                $("#id_translation_span").html('');
            }
        });
    }
});