$(document).ready( function() {

    // make AJAX call to get json of movie info
    populate();

    // display 'title' property on mouse-over of both axes
    $( "#collaborative-span" )
        .tooltip({ 'track': false, 
            'position': {'my': 'center top+50', 
                'at': 'center bottom'}, 
                'tooltipClass': 'instructions'
        });

    $( "#content-span" )
        .tooltip({ 'track': false, 
            'position': {'my': 'right top', 
                'at': 'left-20 center-50'}, 
                'tooltipClass': 'instructions'
        });

    // make endzones "droppable" and define action to take 
    // when poster dropped inside
    $( ".droppable_bar" ).droppable({
        accept: "#containment-wrapper > img",
        drop: function( event, ui ) {

            // detach the image from its current parent
            ui.draggable.detach();
            // disable tooltip (to reenable in new position, but that doesn't work for now) 
            ui.draggable.tooltip('disable'); 

            // append to droppable endzone 
            toEndzone(ui.draggable, $(this));

            // make AJAX call to update preferences and get new predictions
            $.ajax({
                type: 'GET',
                url: '/update_choice',
                dataType: "json",
                data: {'poster': ui.draggable.attr('id'), 'endzone': $(this).attr('id') },
                success: function(response) {
                    for (var post in response) {
                        // shift position to between 0 and 1 (model prediction between -1 and 1)
                        posx = 0.5*(1.0 + response[post][0]);
                        posy = 0.5*(1.0 + response[post][1]);                            
                        // place poster
                        placePoster("#"+post, posx, posy);
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });

    function toEndzone(poster, endzone) {
        // add poster image to endzone
        $(poster)
            .css({
                'position': 'static',
                'transform': 'scale(0.75,0.75)',
                'margin': '5px auto -50px auto',
            }).appendTo($(endzone));
    }

    function placePoster(obj, relx, rely) {
        var container_width = $("#containment-wrapper").width();
        var container_height = $("#containment-wrapper").height();
        var img_height = Math.max(100,$(obj).height());
        var img_width = Math.max(68,$(obj).width());
        var buff = $(".droppable_bar").width();

        $(obj).animate({
            top:  rely*(container_height - img_height), 
            left: buff + relx*(container_width - 2*buff - img_width)
        }, 400, function() {});
    }

    // initialize posters
    function initPosters() {
        // make objects of class .draggable, er,  draggable
        $( ".draggable" )
            .draggable({ 
                containment: "#containment-wrapper",
                revert: 'invalid', 
                scroll: false 
            });

        // display' title' property on mouse-over
        $( ".draggable" ).tooltip({
            track: true,
            hide: { effect: "scale", duration: 300 }
        });

        // raise to top on click
        $( ".draggable" ).mousedown( function(ev) {
            // for touchscreen prevent select on 'click'
            ev.preventDefault();
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
                // console.log(response);
                for (var ifilm = 0; ifilm < response.length; ifilm++) {
                    // add films to the #containment-wrapper element in DOM
                    $('<img src="/static/images/posters/' + response[ifilm].filename + '"' + 
                            'title="' + response[ifilm].title + '"/>')
                        .addClass("ui-widget-content draggable")
                        .attr('id', 'poster_' + ifilm)
                        .appendTo($("#containment-wrapper"));
                }
                // initialize poster properties and positions
                initPosters();
            },
            error: function(error) {
                console.log(error);
            }
        });

    }

});
