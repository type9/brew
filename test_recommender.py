from recommender import Recommender
test_reviews = {
    '11001': '2',
    '11000': '2',
    '11003': '1',
    '11005': '-1'
}

test_recommend = Recommender(test_reviews)

test_recommend.get_ingredients()
print(test_recommend.ingredient_scores)