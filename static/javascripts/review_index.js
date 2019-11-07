$(document).ready(function(){
    QUERY_BY_ID = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=';

    // this function calls the app's API to get the user's reviews and loads it into the page
    review_container = '#review-list-container'
    marked_preference_class = 'disabled';
    $.get('/reviews/get', async function(data){
        review_data = JSON.parse(data);

        for(x = 0; x < review_data.length; x++){
            this_review = review_data[x];
            drink_id = this_review['drink_id'];

            
            let drink_data = new Promise((resolve, reject) => {
                $.get(QUERY_BY_ID + drink_id, function(drink_data){
                    console.log(drink_data);
                    resolve(drink_data);
                });
            });
            let drink_object = await drink_data;
            drink_info = drink_object['drinks']['0'];

            drink_preference = this_review['preference'];
            console.log(drink_preference)
            drink_name = drink_info['strDrink'];
            drink_img = drink_info['strDrinkThumb'];

            $(review_container).append(build_drink_card(drink_id, drink_preference, drink_name, drink_img))
        }
    });

    function build_drink_card(drink_id, drink_preference, drink_name, drink_img){

        button_status_rlike = ''; //marks the button to show the user which preference the drink is already rated at
        button_status_like = '';
        button_status_dislike = '';
        if (drink_preference == '2'){
            button_status_rlike = marked_preference_class;
        } else if(drink_preference == '1'){
            button_status_like = marked_preference_class;
        } else if(drink_preference == '-1'){
            button_status_dislike = marked_preference_class;
        }

        console.log(`
            drink_preference = ${drink_preference}
            status rlike = ${button_status_rlike}
            status like = ${button_status_like}
            status dislike = ${button_status_dislike}
        `);

        var drink_card = `
                <div id='drinkid-${drink_id}'class='card mt-4 ml-4' style='width:250px;'>
                    <img src='${drink_img}' class='card-img-top' alt='${drink_name}'>
                    <div class='card-body'>
                        <h5 class='card-title'>${drink_name}</h5>
                        <p class='card-text'></p>
                        <div class='btn-group' role='group'>
                            <button type='button' class='btn btn-warning focus-cocktail-rating ${button_status_rlike}' value='Really like' ${button_status_rlike}>Really like</button>
                            <button type='button' class='btn btn-success focus-cocktail-rating ${button_status_like}' value='Like' ${button_status_like}>Like</button>
                            <button type='button' class='btn btn-danger focus-cocktail-rating ${button_status_dislike}' value='Dislike' ${button_status_dislike}>Dislike</button>
                        </div>
                    </div>
                </div>
            `;
        
        return drink_card;
    }
});