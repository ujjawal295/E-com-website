import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password')
        self.name = user_data.get('name')
        self.role = user_data.get('role', 'user')
        self.created_at = user_data.get('created_at')
        self.orders = user_data.get('orders', [])

    def check_password(self, password):
        if self.password_hash.startswith('pbkdf2:'):
            return check_password_hash(self.password_hash, password)
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password_hash,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at,
            'orders': self.orders
        }

    @staticmethod
    def get_user_by_id(user_id):
        try:
            with open('app/data/users.json', 'r') as f:
                data = json.load(f)
                for user in data['users']:
                    if user['id'] == str(user_id):
                        return User(user)
        except Exception as e:
            print(f"Error loading user: {e}")
        return None

    @staticmethod
    def get_user_by_email(email):
        try:
            with open('app/data/users.json', 'r') as f:
                data = json.load(f)
                for user in data['users']:
                    if user['email'] == email:
                        return User(user)
        except Exception as e:
            print(f"Error loading user: {e}")
        return None

    @staticmethod
    def create_user(email, password, name):
        try:
            with open('app/data/users.json', 'r') as f:
                data = json.load(f)
            
            # Check if user already exists
            if any(user['email'] == email for user in data['users']):
                return None

            # Create new user
            new_user = {
                'id': str(len(data['users']) + 1),
                'email': email,
                'password': generate_password_hash(password),
                'name': name,
                'role': 'user',
                'created_at': datetime.now().isoformat(),
                'orders': []
            }
            
            data['users'].append(new_user)
            
            # Save updated user data
            with open('app/data/users.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            return User(new_user)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def save(self):
        try:
            with open('app/data/users.json', 'r') as f:
                data = json.load(f)
            
            # Update user data
            for i, user in enumerate(data['users']):
                if user['id'] == self.id:
                    data['users'][i] = self.to_dict()
                    break
            
            # Save updated user data
            with open('app/data/users.json', 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False 