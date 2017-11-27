$(document).ready(function()
{
    var current_noun = null;

    get_noun();

    function update_colors(gender)
    {
        var controls = [$("#id_plural_span"), $("#id_singular_span")];

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

                update_colors(current_noun.gender);

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