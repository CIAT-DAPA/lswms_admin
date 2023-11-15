from flask_login import UserMixin
import os
user=os.getenv('WP_ADMIN_USER')
password=os.getenv('WP_ADMIN_PASSWORD')
users = {user: {'password': password}}

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get(username):
        user_data = users.get(username)
        if user_data:
            return User(username, user_data['password'])
        return None

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return self.username
