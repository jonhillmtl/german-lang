$(document).ready(function()
{
    get_gqm(verb_random_url, 'verb', 'verb_pp_multi', get_callback);

    $(".translation").click(function()
    {
        check_translation_multi_answer(
            verb_pp_multi_url, 
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
            get_gqm(verb_random_url, 'verb', 'verb_pp_multi', get_callback);
        }
    }

    function get_callback(data)
    {
        $("#id_verb_span").html(current_gqm.verb);
        console.log(current_gqm);
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