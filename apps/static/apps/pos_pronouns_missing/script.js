$(document).ready(function()
{
    var genders = [
        "masculine", "feminine", "neutral", "plural"
    ];

    var controls = [
        $("#id_nominative_input"),
        $("#id_accusative_input"),
        $("#id_dative_input")
    ];

    var pronoun_index = -1;
    var gender_index = -1;
    var missing_index = -1;
    var selected_pronouns = null;

    function set_pronouns()
    {
        var new_gender_index = Math.floor(Math.random() * 4);
        while(new_gender_index == gender_index)
            new_gender_index = Math.floor(Math.random() * 4);
        gender_index = new_gender_index;

        $("#id_gender_span").html(genders[gender_index]);
        update_colors([$("#id_gender_span")], genders[gender_index][0]);

        pronoun_index = Math.floor(Math.random() * 8);
        $("#id_pronoun_span").html(pronouns["pronoun"][pronoun_index]);

        missing_index = Math.floor(Math.random() * 3);

        selected_pronouns = [
            pronouns["nominative"][genders[gender_index]][pronoun_index],
            pronouns["accusative"][genders[gender_index]][pronoun_index],
            pronouns["dative"][genders[gender_index]][pronoun_index]
        ];
        
        for(var i = 0; i < 3; i++)
        {
            if(i == missing_index)
            {
                controls[i].val("");
                controls[i].prop('readonly', false);
                controls[i].focus();
            }
            else
            {
                controls[i].val(selected_pronouns[i]);
                controls[i].prop('readonly', true);
            }
            
            controls[i].prop('placeholder', "");
        }
    }

    $('.case_input').keyup(function(e)
    {
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    $('.case_input').bind("enterKey", function(e)
    {
        var answer = $(this).val();

        if(answer == selected_pronouns[missing_index])
        {
            set_pronouns();
        }
        else
        {
            $(this).val("");
            $(this).prop('placeholder', selected_pronouns[missing_index]);
        }
    });

    set_pronouns();
});