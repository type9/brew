class Pallete(object):
    def __init__(self):
        self.ingredients_ignore = [
            'Water',
            'Sugar'
        ]
    
    def ignore_ingredients(self, ingredient_list, ignore_list):
        new_ingredient_list = ingredient_list
        ingredients_to_pop = list()
        for ingredient in ignore_list:
            for x in range(len(ingredient_list)):
                if ingredient == ingredient_list[x][0]:
                    ingredients_to_pop.append(ingredient_list[x])
        for ingredient in ingredients_to_pop:
            new_ingredient_list.remove(ingredient)

        return new_ingredient_list