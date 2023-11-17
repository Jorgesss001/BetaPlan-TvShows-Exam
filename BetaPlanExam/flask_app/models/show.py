from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
# create a regular expression object that we'll use later   
class Show:
    db_name = 'TvShows'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.releaseDate = ['releaseDate']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database


    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (name, description, network, release_date, user_id) VALUES (%(name)s, %(description)s, %(network)s, %(release_date)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        return results[0] 

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET name=%(name)s, description =  %(description)s, network=%(network)s, release_date =%(release_date)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM shows;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_shows= []
        for row in results:
            all_shows.append(row)
        return all_shows
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['name'])<3:
            flash('Name of the show must be at least 3 characters', "show")
            is_valid=False
        if len(show['network'])<3:
            flash('network must be at least 3 characters', "show")
            is_valid=False
        if len(show['description'])<3:
            flash('Description must be at least 3 characters', "show")
            is_valid=False
        if show['release_date'] == "":
            flash('Please enter a date', "show")
            is_valid=False
        return is_valid
    
    