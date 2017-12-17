$(document).ready(function()
{
    get_gqm(url_manifest['verb_random'], 'verb', 'verb_pp_multi', get_callback);

    $(".translation").click(function()
    {
        check_translation_multi_answer(
            url_manifest['verb_pp_multi_check'], 
            $(this).data('pp'),
            'verb',
            'verb_pp_multi',
            check_callback
        );
    });

    function check_callback(data)
    {
        if(data.correct)
        {
            get_gqm(url_manifest['verb_random'], 'verb', 'verb_pp_multi', get_callback);
        }
    }

    function get_callback(data)
    {
        $("#id_verb_span").html(current_gqm.verb);
        $("#id_translation_span").html(current_gqm.translations_text);
        
        // TODO JHILL: factor up and out of here
        var index = 0;
        $("#id_buttons").children('button').each(function()
        {
            $(this).data('pp', current_gqm.possible_past_participles[index])
            $(this).text(current_gqm.possible_past_participles[index]);
            index++;
        });
    }
});