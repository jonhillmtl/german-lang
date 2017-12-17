$(document).ready(function()
{
    var nouns = null;
    var controls = [$("#id_singular_span"), $("#id_plural_span"), $("#id_plural_text")];
    
    function flash_noun()
    {
        var random_index = Math.floor(Math.random() * nouns.length);
        current_noun = nouns[random_index];
        
        $("#id_singular_span").html(current_noun.articled.nominative_definite_singular);
        $("#id_plural_span").html(current_noun.articled.nominative_definite_plural);
        $("#id_translation_span").html(current_noun.translations_text);
        
        update_colors(controls, current_noun.gender);
        setTimeout(flash_noun, 10);
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