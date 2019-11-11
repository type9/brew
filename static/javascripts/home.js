$(document).ready(function(){
    QUERY_BY_NAME = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=';

    recommendations_id = '#recommendations-container';
    NUM_RECOMMENDATIONS = 15;
    //insertion of drink data into recommendations section
    $.post('/recommendations/get',function(data) {
        drink_list = JSON.parse(data)
        for(x = 0; x < NUM_RECOMMENDATIONS; x++){
            this_drink = drink_list[x]
            if(this_drink != undefined){
                drink_id = this_drink['idDrink']
                drink_name = this_drink['strDrink']
                drink_img = this_drink['strDrinkThumb']
                var drink_card = `
                    <div id='drinkid-${drink_id}'class='card mb-4' style='width:200px; margin:auto;'>
                        <img src='${drink_img}' class='card-img-top' alt='${drink_name}'>
                        <div class='card-body'>
                            <h5 class='card-title'>${drink_name}</h5>
                            <p class='card-text'></p>
                        </div>
                    </div>
                `;
                $(recommendations_id).append(drink_card)
            } else {
                break;
            }
            //drink card layout for recommendations
            
        }
    });

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
        },
        select: function(event, ui){
            set_focused_cocktail(ui.item.label);
        }
    });

    
    // Search submission detection
    MAX_DETAIL_CHARS = 100;
    function set_focused_cocktail(cocktail){ // default takes search bar value, if a value is passed the search bar value is overridden
        if (cocktail != null){ // if a value is passed through it overrides the search bar value
            searched_cocktail = cocktail;
        } else {
            searched_cocktail = $(cocktail_search_id).val();
        };
        
        if(searched_cocktail.length > 0) { // checks for empty search
            $.get(QUERY_BY_NAME + searched_cocktail, function(data){ // API call to database with searched cocktail
                this_drink = data['drinks'][0] //pulls first drink from the results
                if (this_drink['strDrink'] == searched_cocktail){ // only sets if we have exact match of whats searched
                    $(cocktail_name_elem).text(this_drink['strDrink'])
                    $(cocktail_details_elem).text(this_drink['strInstructions'])
                    $(cocktail_img_elem).attr('src', this_drink['strDrinkThumb'])

                    $(cocktail_name_elem).parent().attr('name', this_drink['idDrink'])

                    this_text = $(cocktail_details_elem).text();
                    if (this_text.length > MAX_DETAIL_CHARS){
                        $(cocktail_details_elem).text(this_text.substring(0, MAX_DETAIL_CHARS) + '...');
                    }
                    $(focused_cocktail_elem).fadeIn('50')
                } else {
                    $(focused_cocktail_elem).fadeOut('25')
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
    $('.cocktail-autocomplete').on('click', function(){
        set_focused_cocktail();
    });

    //rating button press function
    $('.focus-cocktail-rating').on('click', function(){
        drink_id = $(this).parent().parent().attr('name');
        drink_rating = 0;
        button_value = $(this).attr('value');
        console.log($(this).attr('value'));
        if(button_value == 'Really like'){
            drink_rating = '2';
        } else if(button_value == 'Like'){
            drink_rating = '1';
        } else if(button_value == 'Dislike'){
            drink_rating = '-1';
        }
        console.log(drink_id)
        console.log(drink_rating) // TODO: check logs, drink_rating is not setting properly causing DB errors
        $.post('/', {'drink_id': drink_id, 'preference': drink_rating}, function(data) {
            if(data == 'success'){
                alert('Your review went through');
            } else{
                alert('[Error]Review not submitted');
            }
        })
    });
    
});