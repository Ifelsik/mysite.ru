class UserLogin():
    def fromDB(self, user): # какой в этом смысл?
        self.__user = user
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_username(self):
        return str(self.__user[1])
