$(document).ready(function()
{
    var controls = [
        $("#id_nominative_input"),
        $("#id_accusative_input"),
        $("#id_dative_input")
    ];

    var current_index = -1;
    var current_missing = -1;
    var selected_pronouns = null;
    
    function set_pronouns()
    {
        var new_index = Math.floor(Math.random() * 8);
        while(new_index == current_index)
            new_index = Math.floor(Math.random() * 8);
        current_index = new_index;

        selected_pronouns = [
            pronouns["nominative"][current_index],
            pronouns["accusative"][current_index],
            pronouns["dative"][current_index]
        ];

        current_missing = Math.floor(Math.random() * 3);
        
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
            increment_count(true);
        }
        else
        {
            $(this).val("");
            $(this).prop('placeholder', selected_pronouns[current_missing]);
            increment_count(false);
        }
    });

    set_pronouns();
});