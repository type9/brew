from flask import Flask, request

class Review():
    def __init__(self, drink_id, preference):
        self.drink_id = str(drink_id)
        self.preference = int(preference)

class User():
    def __init__(self, username):
        self.username = username
        # self.reviews = list()
    
    def add_review(self, id, preference):
        '''Needs to append a drink object along with string that states "like", "dislike", or "superlike"
        '''
        review = Review(id, preference)
        self.reviews.append(review)
    
    def change_review(self, drink_id, new_value):
        '''Loop through review list and find the review string and change it
        '''
        for x in range(len(self.reviews)):
            if self.reviews[x][0] == drink_id:
                self.reviews[x][1] == new_value
                break
            return False