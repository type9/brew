from recommender import Recommender
from pallete import Pallete
test_reviews = [
    {'drink_id': '11001', 'preference': '2'},
    {'drink_id': '11000', 'preference': '2'},
    {'drink_id': '11003', 'preference': '1'},
    {'drink_id': '11005', 'preference': '-1'}
]
num_drinks = 10
test_recommend = Recommender(test_reviews)


test_list = [
    ['Water', '1'],
    ['Bourbon', '2'],
    ['Sugar', '1'],
    ['Mint', '-1']
]
my_pallete = Pallete()
new_list = my_pallete.ignore_ingredients(test_list, my_pallete.ingredients_ignore)
print(new_list)

test_recommend.get_ingredients()
print(test_recommend.ingredient_scores)

# test_recommend.get_recommendations(num_drinks)
# print(test_recommend.recommendations)