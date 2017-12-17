$(document).ready(function()
{
    get_gqm(url_manifest['noun_random'], 'noun', 'noun_translation_multi', get_callback);

    $(".translation").click(function()
    {
        check_translation_multi_answer(
            url_manifest['noun_translation_multi_check'],
            $(this).data('translation_id'),
            'noun',
            'noun_translation_multi',
            check_callback
        );
    });

    function check_callback(data)
    {
        if(data.correct)
        {
            get_gqm(url_manifest['noun_random'], 'noun', 'noun_translation_multi', get_callback);
        }
    }

    function get_callback(data)
    {
        $("#id_singular_span").html(current_gqm.articled.nominative_definite_singular);
        $("#id_plural_span").html(current_gqm.articled.nominative_definite_plural);
        update_colors([$("#id_singular_span"), $("#id_plural_span")], current_gqm.gender);

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