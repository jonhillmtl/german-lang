$(document).ready(function()
{
    get_gqm('verb', 'verb_translation_multi', get_callback);

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
            get_gqm('verb', 'verb_translation_multi', get_callback);
        }
    }
    
    function get_callback(data)
    {
        console.log(data);
        $("#id_verb_span").html(current_gqm.verb);
        
        var index = 0;
        $("#id_buttons").children('button').each(function()
        {
            $(this).data('translation_id', current_gqm.possible_translations[index].id)
            $(this).text(current_gqm.possible_translations[index].translation);
            index++;
        });
    }
});