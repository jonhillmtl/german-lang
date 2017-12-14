$(document).ready(function()
{
    function set_pronoun()
    {
        var index = Math.floor(Math.random() * 8);
        $("#id_nominative_input").val(pronouns["nominative"][index]);
        $("#id_accusative_input").val(pronouns["accusative"][index]);
        $("#id_dative_input").val(pronouns["dative"][index]);
    }
    
    set_pronoun();
});