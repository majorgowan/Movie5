$(document).ready( function() {

    // make AJAX call to get json of movie info
    populate();


    $( ".droppable_bar" ).droppable({
        accept: "#containment-wrapper > img",
        drop: function( event, ui ) {

            console.log('draggable object has id ' + ui.draggable.attr('id'));
            console.log(JSON.stringify({'poster': ui.draggable.attr('id'), 'endzone': $(this).attr('id') }));

            // detach the image from its current parent and append it to endzone
            ui.draggable.detach();
            // append to droppable endzone and position 
            ui.draggable
                .css({
                    'position': 'static',
                    'margin': '5px auto -40px auto'
                }).appendTo($(this));
            // make AJAX call to update preferences and get new predictions
            $.ajax({
                type: 'GET',
                url: '/update_choice',
                dataType: "json",
                data: {'poster': ui.draggable.attr('id'), 'endzone': $(this).attr('id') },
                success: function(response) {
                    console.log(response);
                    for (var post in response) {
                        posx = 0.5*(response[post] + 1);
                        posy = 1-posx;                            
                        placePoster("#"+post, posx, posy);
                    }
                    //rearrange_other_posters(ui.draggable, response.nudge);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

    function placePoster(obj, relx, rely) {
        buff = $(".droppable_bar").width();
        $(obj).animate({
            top:  relx*($("#containment-wrapper").height() - $("img").height()), 
            left: buff + rely*($("#containment-wrapper").width() - 2*buff - $("img").width())
        }, 400, function() {
            // Animation complete.
        });
        //$(obj).css({ 
        //    top:  relx*($("#containment-wrapper").height() - $("img").height()), 
        //    left: buff + rely*($("#containment-wrapper").width() - 2*buff - $("img").width())
        //});
    }

    function initPosters() {

        // make objects of class .draggable, er,  draggable
        $( ".draggable" )
            .draggable({ 
                containment: "#containment-wrapper",
                revert: 'invalid', 
                scroll: false 
            });

        // display 'title' property on mouse-over
        $( ".draggable" ).tooltip({ track: true });


        // raise to top on click
        $( ".draggable" ).mousedown( function() {

            var el = $(this);

            // find maximum z-index of object's siblings
            var maxZI = 0;

            el.siblings("img").each( function () {
                var z = parseInt($(this).css("z-index"), 10);
                maxZI = Math.max(maxZI, z);
            });

            // set clicked element to a higher level
            el.css({ 'z-index': maxZI+1 });

        });

        // randomly position 
        $( ".draggable" ).each(function() {
            placePoster($(this), Math.random(), Math.random());
        });
    }

    function populate() {
        // make an AJAX call to get list of movies and image files 
        $.ajax({
            url: '/get_movie_list',
            dataType: "json",
            data: '',
            type: 'GET',
            success: function(response) {
                console.log(response);
                for (var ifilm = 0; ifilm < response.length; ifilm++) {
                    // add films to the #containment-wrapper element in DOM
                    $('<img src="/static/images/' + response[ifilm].filename + '"' + 
                            'title="' + response[ifilm].title + '"/>')
                        .addClass("ui-widget-content draggable")
                        .attr('id', 'poster_' + ifilm)
                        .appendTo($("#containment-wrapper"));
                }
                initPosters();
            },
            error: function(error) {
                console.log(error);
            }
        });

    }

});
