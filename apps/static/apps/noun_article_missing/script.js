$(document).ready(function()
{
    var current_noun = null;
    get_noun();
    
    function show_gender_row(gender)
    {
        $(".hideable_gender_row").hide();
        $("#id_" + gender + "_row").show();
    }
    
    var inputs = [
        $("#id_nominative_definite_singular"),
        $("#id_nominative_indefinite_singular"),
        $("#id_accusative_definite_singular"),
        $("#id_accusative_indefinite_singular"),
        $("#id_dative_definite_singular"),
        $("#id_dative_indefinite_singular"),
        $("#id_genitive_definite_singular"),
        $("#id_genitive_indefinite_singular"),
    ];
    
    var articles = [];

    function get_noun()
    {
        url = 'http://0.0.0.0:8080/api/noun/?mode=noun_article_missing';
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data)
            {
                current_noun = data.noun;

                $("#id_gender_span").html(current_noun.gender);
                $(".id_singular_span").text(current_noun.articled.nominative_definite_singular);
                $(".id_plural_span").text(current_noun.articled.nominative_definite_plural);
                $(".singular_form").text(current_noun.singular_form);
                $(".plural_form").text(current_noun.plural_form);
                $("#id_translation_span").html(current_noun.translations_text);
                show_gender_row(current_noun.gender);

                articles = [
                   current_noun.articles.nominative_definite_singular,
                   current_noun.articles.nominative_indefinite_singular,
                   current_noun.articles.accusative_definite_singular,
                   current_noun.articles.accusative_indefinite_singular,
                   current_noun.articles.dative_definite_singular,
                   current_noun.articles.dative_indefinite_singular,
                   current_noun.articles.genitive_definite_singular,
                   current_noun.articles.genitive_indefinite_singular
                ];

                update_colors([
                    $(".singular_form"),
                    $(".plural_form"),
                ], current_noun.gender);

                
                for(var i = 0; i < 8; i++)
                {
                    inputs[i].val(articles[i]);
                }
            }
        });
    }

    function submit_answer(gender)
    {

    }
});