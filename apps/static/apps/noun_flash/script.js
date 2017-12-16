$(document).ready(function()
{
    var current_noun = null;
    var controls = [$("#id_singular_span"), $("#id_plural_span"), $("#id_plural_text")];
    
    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_gender';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_noun = data.noun;
                
                $("#id_singular_span").html(current_noun.articled.nominative_definite_singular);
                $("#id_plural_span").html(current_noun.articled.nominative_definite_plural);
                $("#id_translation_span").html(current_noun.translations_text);
                
                update_colors(controls, current_noun.gender);
                setTimeout(get_noun, 2000);
            }
        });
    }
    
    get_noun();
});