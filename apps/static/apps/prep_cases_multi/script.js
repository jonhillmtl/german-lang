$(document).ready(function()
{
    console.log(prep_cases);
    var cases = [
        'dativ',
        'akkusativ',
        'either'
    ];

    var current_case = null;
    var current_prep = null;
    var correction_text = null;

    function reset_question()
    {
        current_case = cases[Math.floor(Math.random() * 3)];
        var case_prep_length = prep_cases[current_case].length;
        var prep_index = Math.floor(Math.random() * case_prep_length);
        current_prep = prep_cases[current_case][prep_index];

        $("#id_prep_span").html(current_prep);
    }

    reset_question();

    $('#id_correction_text').keyup(function(e)
    {
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });

    $("#id_correction_text").bind("enterKey", function(e)
    {
        if(correction_text == $("#id_correction_text").val())
        {
            $("#id_correction_overlay").hide();
            reset_question();
        }
        else
        {
            $("#id_correction_text").val("");
        }
    });

    $(".case").click(function()
    {
        if($(this).data("case") == current_case)
        {
            reset_question();
            increment_count(true);
        }
        else
        {
            correction_text = current_prep + " ist " + current_case;
            $("#id_correction_correct").html(correction_text);
            $("#id_correction_text").val("");
            $("#id_correction_overlay").show();
            $("#id_correction_text").focus();
            increment_count(false);
        }
    });
});