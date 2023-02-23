from flask_app.config.pymysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, BCRYPT
from flask import flash
import re

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
        
    # Class method to create a user in the database
    @classmethod
    def create(cls, form):
        
        
        hashed_pw = BCRYPT.generate_password_hash(form['password'])
        
        
        data = {
            **form,
            'password' : hashed_pw
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    # Class method to find a user by email in the database
    @classmethod
    def get_one_by_email(cls, email):
        data = {
            'email' : email
        }
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            return cls(results[0])
        else:
            return False
        
        
    # Class method to find a user by id
    @classmethod
    def get_one(cls, id):
        
        data = {
            'id' : id
        }
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        result = results[0]
        
        return cls(result)



    # Checks if there is registered user in our database
    @classmethod
    def validate_login(cls, form):
        is_valid = True
        found_user = cls.get_one_by_email(form['email'])
        if not found_user:
            flash("Invalid Login", 'log_In_Error')
            return False
        else:
            if not BCRYPT.check_password_hash(found_user.password, form['password']):
                flash("Invalid Login", 'log_In_Error')
                return False
        
        return found_user
    
    
    @staticmethod
    def validate(data):
        # letters variable is set to check characters are only letters 
        letters = re.compile(r'^[a-zA-Z]+$')
        # is_valid variable is a placeholder for the validations below returning False and returns True if all validations pass
        is_valid = True
        
        # Checks if anything is entered in input fields
        if not data['first_name']:
            flash("First Name is required", 'reg_error')
            is_valid = False
        else:
            is_valid = True
            
        if not data['last_name']:
            flash("Last Name is required", 'reg_error')
            is_valid = False
        else:
            is_valid = True
            
        if not data['email']:
            flash("Email is required", 'reg_error')
            is_valid = False
        else:
            is_valid = True
            
        if not data['password']:
            flash("Password is required", 'reg_error')
            is_valid = False
        else:
            is_valid = True


        
        # Checks if input fields contain a specific length of characters
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters", 'reg_error')
            is_valid = False
        
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters", 'reg_error')
            is_valid = False
            
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", 'reg_error')
            is_valid = False


        # Checks if input fields contain only letters 
        if letters.match(data['first_name']):
            is_valid = True
        else: 
            flash("First Name must only be letters ex. John", 'reg_error')
            is_valid = False

        if letters.match(data['last_name']):
            is_valid = True
        else: 
            flash("Last Name must only be letters ex. John", 'reg_error')
            is_valid = False

        # Checks if email is in a valid format
        if not EMAIL_REGEX.match(data['email']):
            flash("invalid email, try again ex.User@mail.com", 'reg_error')
            is_valid = False
        
        # checks if email is already registered
        if User.get_one_by_email(data['email']):
            flash("Email already registered", 'reg_error')
            is_valid = False
        
        # Checks if password and confirm password match
        if data['password'] != data['confirm_password']:
            flash("Passwords don't match!", 'reg_error')
            is_valid = False
        
        return is_valid
