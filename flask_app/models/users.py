from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "ohana_rideshare_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_user(user):
        is_valid = True
        if not len(user['first_name']) >= 3 and str.isalpha(user['first_name']):
            flash(
                "First name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if not len(user['last_name']) >= 3 and str.isalpha(user['last_name']):
            flash(
                "Last name must be at least 2 characters and contain only letters.", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'register')
            is_valid = False
        if not len(user['password']) >= 9 and str.isalnum(user['password']):
            flash('Invalid password. Must contain at least 8 characters.', 'register')
            is_valid = False
        if not str.isalpha(user['password']) == False:
            flash('Password must contain at least 1 number', 'register')
            is_valid = False
        if not str.islower(user['password']) == False:
            flash("Password must contain at least 1 capital letter", 'register')
            is_valid = False
        if not user['password'] == user['confirm_password']:
            flash('Passwords must match', 'register')
            is_valid = False

        return is_valid


#Create:
    @classmethod
    def save(cls, data):
        query = '''INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)


#Read:
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for a_user in results:
            users.append(cls(a_user))
        return users
    

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        
        return cls(result[0])
        #If JOINING tables, and adding attributes to user object, use the following method to add new table attributs.
        # user_data = result[0]
        # user = cls(user_data)
        # user.new_attribute = user_data['new_attribute']
        # return user

        #If JOINING tables for many:many and adding objects related to user, use the following method to add objects to user.
        # data = {
        #     "author_id": id
        # }
        # results = connectToMySQL("books_schema").query_db(query, data)
        # if len(results)>0:
        #     author = cls(results[0])
        #     for row_from_db in results:
        #             book_data = {
        #                 "id": row_from_db["books.id"],
        #                 "title": row_from_db["title"],
        #                 "num_of_pages": row_from_db["num_of_pages"],
        #                 "created_at": row_from_db["books.created_at"],
        #                 "updated_at": row_from_db["books.updated_at"]
        #             }
        #             author.books.append(book.Book(book_data))
        #     return author
        # else:
        #     author = Author.author_select_one(id)
        #     return author

#Update:
    @classmethod
    def update_user_info(cls,data):
        query = '''UPDATE users SET
                    first_name = %(first_name)s,
                    last_name = %(last_name)s,
                    email = %(email)s,
                    password = %(password)s
                    WHERE id = %(id)s;'''
        
        return connectToMySQL(cls.DB).query_db(query,data)


#Delete:
    @classmethod
    def delete_user(cls, id):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        
        return connectToMySQL(cls.DB).query_db(query, {"id": id}) 