$(document).ready(function()
{
    var current_noun = null;

    get_noun();

    $(".translation").click(function()
    {
        var url = 'http://0.0.0.0:8080/api/nouns/translation/multi/check/';

        $.post({
            url: url,
            success: function(data)
            {
                if(data.correct)
                {
                    get_noun();
                }
            },
            data: JSON.stringify(
                {
                    'noun_id': current_noun.id,
                    'translation_id': $(this).data('translation_id')
                }
            )
        });
        
    });

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_translation_multi';
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

                $("#id_singular_span").html(current_noun.gendered_singular);
                $("#id_plural_span").html(current_noun.gendered_plural);
                
                var index = 0;
                $("#id_buttons").children('button').each(function()
                {
                    $(this).data('translation_id', current_noun.possible_translations[index].id)
                    $(this).text(current_noun.possible_translations[index].translation);
                    index++;
                });
            }
        });
    }
});