$(document).ready(function()
{
    var current_verb = null;

    get_verb();

    $(".translation").click(function()
    {
        var url = 'http://0.0.0.0:8080/api/verbs/translation/multi/check/';

        $.post({
            url: url,
            success: function(data)
            {
                if(data.correct)
                {
                    get_verb();
                }
            },
            data: JSON.stringify(
                {
                    'verb_id': current_verb.id,
                    'translation_id': $(this).data('translation_id')
                }
            )
        });
    });

    function get_verb()
    {
        url = 'http://0.0.0.0:8080/api/verbs/?mode=verb_translation_multi';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_verb = data.verb;
                console.log(data);
                $("#id_verb_span").html(current_verb.verb);
                
                var index = 0;
                $("#id_buttons").children('button').each(function()
                {
                    $(this).data('translation_id', current_verb.possible_translations[index].id)
                    $(this).text(current_verb.possible_translations[index].translation);
                    index++;
                });
            }
        });
    }
});