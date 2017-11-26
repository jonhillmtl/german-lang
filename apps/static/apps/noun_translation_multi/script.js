$(document).ready(function()
{
    var current_noun = null;

    get_noun();

    $(".noun_translation_button").click(function()
    {
        var url = 'http://0.0.0.0:8080/api/nouns/translations/multi/check/';

        $.post({
            url: url,
            success: function(data)
            {
                console.log(data.correct)
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
        url = 'http://0.0.0.0:8080/api/nouns/';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_noun = data.noun;

                $("#singular_span").html(current_noun.singular_form);
                $("#plural_span").html(current_noun.plural_form);
                
                var index = 0;
                $("#id_buttons").children('button').each(function()
                {
                    $(this).text(data['translations'][index]['answer']);
                    $(this).data('translation_id', data['translations'][index]['id'])
                    index++;
                });
            }
        });
    }
});