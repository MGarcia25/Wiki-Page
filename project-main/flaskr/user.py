class User(user_info):
    name = user_info[0]
    pass_word = user_info[1]

    def to_json(self):
        return {"name": self.name, "email": self.pass_word}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
