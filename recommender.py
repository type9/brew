import requests
import json
from pallete import Pallete

cocktaildb_drinkurl = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
max_ingredients = 15

class Recommender(object):

    def __init__(self, reviews):
        self.reviews = list(reviews.items()) # converts from dict to tuple
        self.ingredient_scores = list()

    def get_recommendations(self, n):
        '''Method should return a list of n length of drinks ids in
        descending order of score
        '''
        pass

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
                if current_ingredient == None:
                    break
                ingredient_in_list = False
                for y in range(len(self.ingredient_scores)): # looks for the ingredient in the review list and increments by the review value if found
                    if self.ingredient_scores[y][0] == current_ingredient:
                        self.ingredient_scores[y][1] += int(self.reviews[i][1])
                        ingredient_in_list = True # marks that it found the ingredient
                if not ingredient_in_list: # elseif the ingredient needs to be added
                    self.ingredient_scores.append([current_ingredient, int(self.reviews[i][1])]) # gets appended with the review
    
    def apply_pallete(self):
        '''Method should manipulate ingredient scoring based off predetermined
        flavor groups. Utilize pallete class.
        '''
        pass