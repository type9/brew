from user import User
from pallete import Pallete

class Recommender(object):

    def __init__(self, user, drink_object_list):
        self.user = user
        self.ingredient_scores = list()
    
    def get_recommendations(self):
        '''Method should return a list of n length of drinks in
        descending order of score
        '''
        pass

    def get_ingredients(self):
        '''Method should return a 2D list of ingredients from the user's preferences
        and additive score. Where a like is +1, dislike is -1, and a super like is +2.
        Format should look like [ingredient_name, score]
        '''
        pass
    
    def apply_pallete(self):
        '''Method should manipulate ingredient scoring based off predetermined
        flavor groups. Utilize pallete class.
        '''
        pass