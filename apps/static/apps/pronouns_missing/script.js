$(document).ready(function()
{
    var controls = [
        $("#id_nominative_input"),
        $("#id_accusative_input"),
        $("#id_dative_input")
    ];

    var current_index = 0;
    var current_missing = 0;
    var selected_pronouns = null;
    
    function set_pronouns()
    {
        current_index = Math.floor(Math.random() * 8);

        selected_pronouns = [
            pronouns["nominative"][current_index],
            pronouns["accusative"][current_index],
            pronouns["dative"][current_index]
        ];

        current_missing = Math.floor(Math.random() * 3);
        console.log(current_missing);
        
        for(var i = 0; i < 3; i++)
        {
            if(i == current_missing)
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
        if(answer == selected_pronouns[current_missing])
        {
            set_pronouns();
        }
        else
        {
            $(this).val("");
            $(this).prop('placeholder', selected_pronouns[current_missing]);
        }
    });

    set_pronouns();
});