import requests
import json
from pallete import Pallete

cocktaildb_drinkurl = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
cocktaildb_searchbyingredient = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
max_ingredients = 15

class Recommender(object):

    def __init__(self, reviews):
        self.reviews = self.convert_to_list(reviews) # converts from db dict format to iterable list format [drink_id][score]
        self.ingredient_scores = list() # FORMAT: [drink_id][score]
        self.recommendations = list() # FORMAT: [drink_id][total_score]
        self.pallete = Pallete()

    def convert_to_list(self, reviews):
        list_reviews = list()
        for x in range(len(reviews)):
            this_review = [reviews[x]['drink_id'], reviews[x]['preference']]
            list_reviews.append(this_review)
        return list_reviews

    def get_recommendations(self, n):
        '''Method should return a list of n length of drinks ids in
        descending order of score
        '''
        self.get_ingredients()
        for x in range(len(self.ingredient_scores)): # for ea. ingredient scored
            r = requests.get(cocktaildb_searchbyingredient + self.ingredient_scores[x][0]) # searching db by ingredient
            ingredient_drinks = json.loads(r.content)

            for y in range(len(ingredient_drinks['drinks'])): # for ea. drink in the by-ingredient search
                drink_id = ingredient_drinks['drinks'][y]['idDrink']
                already_recommended = False

                for recommended_drink in range(len(self.recommendations)): # for each drink in already recommended
                    if drink_id == self.recommendations[recommended_drink][0]: # checks if the ID already has been recommended
                        already_recommended = True
                        break
                for reviewed_drink in range(len(self.reviews)): # checks if the drink is a drink reviewed already
                    if drink_id == self.reviews[reviewed_drink][0]:
                        already_recommended = True
                        break
                if already_recommended: # breaks if already has been scored and on the recommended list
                    break
                r_1 = requests.get(cocktaildb_drinkurl + drink_id)
                drink =  json.loads(r_1.content) # gets drink object from API call
                drink_score = 0
                for z in range(max_ingredients): # for ea. ingredient in the drink objcet
                    current_ingredient = drink['drinks'][0]['strIngredient' + str(z + 1)] # get ingredient by z value
                    for i in range(len(self.ingredient_scores)): # loop through ingredient scores and check if it matches current ingredient
                        if current_ingredient == self.ingredient_scores[i][0]:
                            drink_score += int(self.ingredient_scores[i][1]) # adds the scoring for that ingredient onto the total score of the drink
                
                self.recommendations.append([drink_id, drink_score]) # appends th drink_id with the associated total score
        sorted_drinks = sorted(self.recommendations, key=lambda x: x[1], reverse=True) # sorts in descending order by score
        self.recommendations = sorted_drinks[:n] # only keeps the first n drinks

    def get_ingredients(self):
        '''Method should return a 2D list of ingredients from the user's preferences
        and additive score. Where a like is +1, dislike is -1, and a super like is +2.
        Format should look like [ingredient_name, score]
        '''
        for i in range(len(self.reviews)):
            r = requests.get(cocktaildb_drinkurl + self.reviews[i][0]) # gets the drink object
            drinks = json.loads(r.content)

            for x in range(max_ingredients): # checks all 15 possible ingredient strings in the object
                current_ingredient = drinks['drinks'][0]['strIngredient' + str(x + 1)]
                if current_ingredient == None: # stop looking for ingredients when a null value
                    break
                ingredient_in_list = False
                for y in range(len(self.ingredient_scores)): # looks for the ingredient in the review list and increments by the review value if found
                    if self.ingredient_scores[y][0] == current_ingredient:
                        self.ingredient_scores[y][1] += int(self.reviews[i][1])
                        ingredient_in_list = True # marks that it found the ingredient
                if not ingredient_in_list: # elseif the ingredient needs to be added
                    self.ingredient_scores.append([current_ingredient, int(self.reviews[i][1])]) # gets appended with the review
        self.apply_pallete()
    
    def apply_pallete(self):
        '''Method should manipulate ingredient scoring based off predetermined
        flavor groups. Utilize pallete class.
        '''
        new_scores = self.pallete.ignore_ingredients(self.ingredient_scores, self.pallete.ingredients_ignore)
        self.ingredient_scores = new_scores