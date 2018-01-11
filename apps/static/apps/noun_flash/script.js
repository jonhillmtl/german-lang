$(document).ready(function()
{
    var nouns = null;
    var controls = [$("#id_singular_span"), $("#id_plural_span"), $("#id_plural_text")];
    var delay = 20;
    var upper_delay = 600;
    var increment = 20;
    
    function flash_noun()
    {
        var random_index = Math.floor(Math.random() * nouns.length);
        current_noun = nouns[random_index];
        
        $("#id_singular_span").html(current_noun.articled.nominative_definite_singular);
        $("#id_plural_span").html(current_noun.articled.nominative_definite_plural);
        $("#id_translation_span").html(current_noun.translations_text);

        update_colors(controls, current_noun.gender);

        if(delay <= 0)
        {
            increment = 20;
            delay = 20;
        }
        else if(delay >= upper_delay)
        {
            increment = -20;
        }
        delay += increment;

        setTimeout(flash_noun, delay);
    }
    
    function get_nouns()
    {
        url = 'http://0.0.0.0:8080/api/nouns/';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                nouns = data.nouns;
                flash_noun();
            }
        });
    }
    
    get_nouns();
});