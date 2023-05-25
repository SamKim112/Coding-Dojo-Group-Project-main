from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

#DONE

class Event:
    db = "project_db"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.event_name = db_data['event_name']
        self.location = db_data['location']
        self.participants = db_data['participants']
        self.date = db_data['date']
        self.messages = db_data['messages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_id = db_data['users_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM events
                JOIN users on events.users_id = users.id;
                """
        results = connectToMySQL(cls.db).query_db(query)
        events = []
        for row in results:
            this_event = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_event.creator = user.User(user_data)
            events.append(this_event)
        return events
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM events
                JOIN users on events.users_id = users.id
                WHERE events.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_event = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_event.creator = user.User(user_data)
        return this_event

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO events (event_name, location, participants, date, messages, users_id)
                VALUES (%(event_name)s,%(location)s,%(participants)s, %(date)s, %(messages)s, %(users_id)s);
                """
        return connectToMySQL(cls.db).query_db(query,form_data)
    
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE events SET event_name = %(event_name)s, location = %(location)s, participants = %(participants)s, date = %(date)s, messages = %(messages)s   WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM events WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_event(form_data):
        is_valid = True

        if len(form_data['event_name']) < 1:
            flash("Please provide an event name.")
            is_valid = False
        elif len(form_data['event_name']) < 3:
            flash("Event name must be more than 3 characters.")
            is_valid = False
        if len(form_data['location']) < 1:
            flash("Please provide a location.")
            is_valid = False
        elif len(form_data['location']) < 3:
            flash("Location name must be more than 3 characters.")
            is_valid = False
        if form_data['participants'] == '':
            flash("Please include participants.")
            is_valid = False
        if form_data['date'] == '':
            flash("Please input a date.")
            is_valid = False  
        if form_data['messages'] == '':
            flash("Please provide a message.")
            is_valid = False  
        return is_valid


