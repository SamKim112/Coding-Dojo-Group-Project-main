from flask_app.config.mysqlconnection import connectToMySQL
from flask import app 
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 



class User:
    db= "project_db"
    def __init__(self, data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]


    @classmethod
    def register_user(cls, data):
        query = """
        INSERT into users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_by_id(cls, data):
        query = """SELECT * from users WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results)==0:
            return None 
        else:
            return cls(results[0])
        
    @classmethod
    def get_one_by_email(cls, data):
        query = """SELECT * from users WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results)==0:
            return None 
        else:
            return cls(results[0])
        
    @staticmethod
    def validate_registration(form_data):
        is_valid= True
        if len (form_data['first_name'])<2:
            is_valid= False
            flash("First Name must be at least 2 characters.")
        if len (form_data['last_name'])<2:
            is_valid= False
            flash("Last Name must be at least 2 characters.")
        if not EMAIL_REGEX.match(form_data['email']): 
            is_valid = False
            flash("Invalid email address!")
        if len (form_data['password'])<8:
            is_valid= False
            flash("Password must be at least 8 characters.")
        if form_data['password'] !=form_data['confirm_password']:
            is_valid= False
            flash("Passwords must agree.")
        found_user_or_none= User.get_one_by_email({"email": form_data['email']})
        if found_user_or_none != None:
            is_valid = False
            flash ("User already registered with that email")
        return is_valid
    
    @staticmethod
    def validate_login(form_data):
        is_valid = True
        found_user_or_none= User.get_one_by_email({"email": form_data['email']})
        if found_user_or_none == None:
            is_valid = False
            flash ("invalid login")
            return False 
        if bcrypt.check_password_hash(found_user_or_none.password, form_data["password"]):
            flash("invalid login ")
            return is_valid
