import flask_login
from flask import Flask, request

class User(flask_login.UserMixin):

    def __init__(self, id, password):
        super().__init__()
        self.id = id
        self.password = password
        self.reviews = list()
    
    def add_review(self, id, preference):
        '''Needs to append a drink object along with string that states "like", "dislike", or "superlike"
        '''
        review = [id, preference]
        self.reviews.append(review)
    
    def change_review(self, drink_id, new_value):
        '''Loop through review list and find the review string and change it
        '''
        for x in range(len(self.reviews)):
            if self.reviews[x][0] == drink_id:
                self.reviews[x][1] == new_value
                break
            return False