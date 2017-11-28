$(document).ready(function()
{
    get_gqm('noun', 'noun_translation_multi', get_callback);

    $(".translation").click(function()
    {
        check_translation_multi_answer(
            $(this).data('translation_id'),
            check_callback
        );
    });
    
    function check_callback(data)
    {
        if(data.correct)
        {
            get_gqm('noun', 'noun_translation_multi', get_callback);
        }
    }
    
    function get_callback(data)
    {
        $("#id_singular_span").html(current_gqm.singular_form);
        $("#id_plural_span").html(current_gqm.plural_form);

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