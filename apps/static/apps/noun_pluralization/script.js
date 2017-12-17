$(document).ready(function()
{
    var current_noun = null;
    var correction = false;
    
    var article = 'definite';
    var case_mode = 'nominative';

    get_noun();

    // TODO JHILL: factor out somewhere
    $('#id_plural_text').bind("enterKey", function(e)
    {
        var url = 'http://0.0.0.0:8080/api/nouns/pluralization/check/';

        $.post({
            url: url,
            success: function(data)
            {
                if(data.correct)
                {
                    correction = false;
                    get_noun();
                }
                else
                {
                    $("#id_plural_span").html(current_noun.articled.nominative_definite_plural);
                    $("#id_plural_text").val('');
                    $("#id_plural_text").focus();
                    correction = true;
                }
            },
            data: JSON.stringify(
                {
                    'noun_id': current_noun.id,
                    'plural': $(this).val(),
                    'correction': correction
                }
            )
        });
    });

    $('#id_plural_text').keyup(function(e)
    {
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/noun/?mode=noun_pluralization';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_noun = data.noun;

                var controls = [$("#id_singular_span"), $("#id_plural_span"), $("#id_plural_text")];
                update_colors(controls, current_noun.gender);

                $("#id_singular_span").html(current_noun.articled.nominative_definite_singular);
                $("#id_translation_span").html(current_noun.translations_text);
                $("#id_plural_text").val('');
                $("#id_plural_text").focus();
                $("#id_plural_span").html("");
            }
        });
    }
});