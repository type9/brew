$(document).ready(function(){
    QUERY_BY_NAME = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=';

    //ELEM IDs
    cocktail_search_id = '#cocktail-search';
    focused_cocktail_elem = '#focused-cocktail'
    cocktail_name_elem = '#focused-cocktail-name';
    cocktail_details_elem = '#focused-cocktail-details';
    cocktail_img_elem ='#focused-cocktail-img';
    
    $(focused_cocktail_elem).hide(); // initial hiding to be revealed later

    // Autocomplete function that queries thecocktaildb.com when at least 3 chars are inputted
    DEFAULT_COMPLETE_LENGTH = 5; //sets the default amount of drinks to be returned by autocomplete
    $(cocktail_search_id).autocomplete({
        source: function(request, response){
            $.get(QUERY_BY_NAME + request.term, function(data){
                this_length = DEFAULT_COMPLETE_LENGTH; //checks to see if we return equal to or less than the default value of drink names
                request_length = data['drinks'].length;
                if(DEFAULT_COMPLETE_LENGTH > request_length){
                    this_length = request_length;
                };

                autocomplete_list = [];
                for(x = 0; x < this_length; x++){ //pulls drink names from the json objects and plops them into an array
                    name = data['drinks'][x]['strDrink']
                    autocomplete_list.push(name)
                };
                response(autocomplete_list);
            });
        },
        minLength: 3,
        delay: 100,
        classes: {
            'ui-autocomplete': 'cocktail-autocomplete',
        }
    });

    
    // Search submission detection
    MAX_DETAIL_CHARS = 100;
    function set_focused_cocktail(){ // function to run when search submitted
        searched_cocktail = $(cocktail_search_id).val();
        if(searched_cocktail.length > 0) { // checks for empty search
            $.get(QUERY_BY_NAME + searched_cocktail, function(data){ // API call to database with searched cocktail
                this_drink = data['drinks'][0] //pulls first drink from the results
                if (this_drink['strDrink'] == searched_cocktail){ // only sets if we have exact match of whats searched
                    $(cocktail_name_elem).text(this_drink['strDrink'])
                    $(cocktail_details_elem).text(this_drink['strInstructions'])
                    $(cocktail_img_elem).attr('src', this_drink['strDrinkThumb'])

                    this_text = $(cocktail_details_elem).text();
                    if (this_text.length > MAX_DETAIL_CHARS){
                        $(cocktail_details_elem).text(this_text.substring(0, MAX_DETAIL_CHARS) + '...');
                    }
                    $(focused_cocktail_elem).fadeIn('50')
                } else {
                    $(focused_cocktail_elem).fadeOut('50')
                };
            });
        };
    };

    //modified done typing function from https://stackoverflow.com/questions/4220126/run-javascript-function-when-user-finishes-typing-instead-of-on-key-up
    //setup before functions
    var typingTimer;//timer identifier
    var doneTypingInterval = 2000;//time in ms

    //on keyup, start the countdown
    $('body').on('keyup', function () {
        typingTimer = setTimeout(set_focused_cocktail(), doneTypingInterval);
        clearTimeout(typingTimer);
    });

    //on keydown, clear the countdown 
    $('body').on('keydown', function () {
        if ($(cocktail_search_id).is(':focus')){
            clearTimeout(typingTimer);
        };
    });

    
    $.post('path', { id:'', value: 23 }, function(data) {

    })
});

// fetch('the/path/to/route?drink=Mai Tai', options).then(res => res.json()).then(json => {

// })