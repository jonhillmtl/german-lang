$(document).ready(function()
{
    get_gqm(verb_random_url, 'verb', 'verb_translation_multi', get_callback);

    $(".translation").click(function()
    {
        check_translation_multi_answer(
            verb_translation_multi_url,
            $(this).data('translation_id'),
            'verb',
            'verb_translation_multi',
            check_callback
        );
    });

    function check_callback(data)
    {
        if(data.correct)
        {
            get_gqm(verb_random_url, 'verb', 'verb_translation_multi', get_callback);
        }
    }

    function get_callback(data)
    {
        $("#id_verb_span").html(current_gqm.verb);
        
        // TODO JHILL: factor up and out of here
        var index = 0;
        $("#id_buttons").children('button').each(function()
        {
            $(this).data('translation_id', current_gqm.possible_translations[index].id)
            $(this).text(current_gqm.possible_translations[index].translation);
            index++;
        });
    }
});