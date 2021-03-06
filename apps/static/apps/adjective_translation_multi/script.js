$(document).ready(function()
{
    get_gqm(url_manifest['adjective_random'], 'adjective', 'adjective_translation_multi', get_callback);

    $(".translation").click(function()
    {        
        check_translation_multi_answer(
            url_manifest['adjective_translation_multi_check'],
            $(this).data('translation_id'),
            'adjective',
            'adjective_translation_multi',
            check_callback
        );
    });

    function check_callback(data)
    {
        if(data.correct)
        {
            get_gqm(
                url_manifest['adjective_random'],
                'adjective',
                'adjective_translation_multi',
                get_callback
            );
        }
    }

    function get_callback(data)
    {
        $("#id_adjective_span").html(current_gqm.adjective);

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