$(document).ready(function()
{
    var nouns = null;
    var controls = [$("#id_singular_span"), $("#id_plural_span"), $("#id_translation_span")];
    var delay = 500;
    var current_step = 0;

    function flash_noun()
    {
        if(current_step == 0)
        {
            var random_index = Math.floor(Math.random() * nouns.length);
            current_noun = nouns[random_index];
            update_colors(controls, current_noun.gender);
            for(index = 0; index < controls.length; index++)
            {  
                control = controls[index];
                control.html('');
            }
            increment_count(true);
            console.log(current_noun);
            refresh_metadata(current_noun);
        }

        if(current_step == 0)
        {
            $("#id_singular_span").html(current_noun.articled.nominative_definite_singular);
            delay = 500;
        }
        else if(current_step == 1)
        {
            $("#id_plural_span").html(current_noun.articled.nominative_definite_plural);
            delay = 750;
        }
        else if(current_step == 2)
        {
            $("#id_translation_span").html(current_noun.translations_text);
            delay = 1000;
        }
        
        current_step++;
        if(current_step == 3)
        {
            current_step = 0;
        }

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