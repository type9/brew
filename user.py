class User(object):

    def __init__(self, id, first_name, last_name):
        self._id = id
        self.first_name = first_name
        self.last_name = last_name
        self.login_key = int()
        self.reviews = list()
    
    def add_review(self, drink_object):
        '''Needs to append a drink object along with string that states "like", "dislike", or "superlike"
        '''
        pass
    
    def change_review(self, drink_id, new_value):
        '''Loop through review list and find the review string and change it
        '''
        pass