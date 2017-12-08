$(document).ready(function()
{
    var article_mode = 'definite';
    var case_mode = 'nominative';

    var current_noun = null;
    get_noun();
    
    function show_gender_row(gender)
    {
        $(".hideable_gender_row").hide(1000);
        $("#id_" + gender + "_row").show(1000);
    }

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/nouns/?mode=noun_gender';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                console.log(data.noun);
                current_noun = data.noun;
                
                $(".singular_form").text(current_noun.singular_form);
                $(".plural_form").text(current_noun.plural_form);
                show_gender_row(current_noun.gender);
            }
        });
    }

    function submit_answer(gender)
    {

    }
});