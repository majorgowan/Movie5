$(document).ready( function() {

    populateFromArray();


    $( ".droppable_bar" ).droppable({
        accept: "#containment-wrapper > img",
        drop: function( event, ui ) {
            $( this )
                .addClass( "dropped" );
            $.ajax({
                url: '/update_choice',
                dataType: "json",
                data: '',
                type: 'POST',
                success: function(response) {
                    console.log(response['nudge']);
                    console.log(ui.draggable);
                    //rearrange_other_posters(ui.draggable, response.nudge);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

    function placePosters() {

        $( ".draggable" ).draggable({ containment: "#containment-wrapper", scroll: false });
        $( ".draggable" ).tooltip({ track: true });


        $( ".draggable" ).each(function() {
            buff = $(".droppable_bar").width();
            $(this).css({ 
                top:  Math.random()*($("#containment-wrapper").height() - $("img").height()), 
                left: buff + Math.random()*($("#containment-wrapper").width() - 2*buff - $("img").width())
            });
        });
    }

    function populateFromArray() {
        /* make an AJAX call to get list of movies and image files */
        $.ajax({
            url: '/get_movie_list',
            dataType: "json",
            data: '',
            type: 'POST',
            success: function(response) {
                console.log(response);
                for (var ifilm = 0; ifilm < response.length; ifilm++) {
                    // add films to the #containment-wrapper element in DOM
                    $('<img src="/static/images/' + response[ifilm].filename + '"' + 
                     'title="' + response[ifilm].title + '"/>')
                        .addClass("ui-widget-content draggable")
                        .appendTo($("#containment-wrapper"));
                }
                placePosters();
            },
            error: function(error) {
                console.log(error);
            }
        });

    }

});
