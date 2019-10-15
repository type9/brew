import flask_login

class User(flask_login.UserMixin):

    def __init__(self, is_authenticated=False, is_active=False, is_anonymous=True):
        self.id = str()
        self.reviews = list()
        
    def get_id(self):
        return self.id
    
    def add_review(self, drink_object):
        '''Needs to append a drink object along with string that states "like", "dislike", or "superlike"
        '''
        pass
    
    def change_review(self, drink_id, new_value):
        '''Loop through review list and find the review string and change it
        '''
        pass