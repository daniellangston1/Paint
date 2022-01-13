from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Painting:
    db = 'belt2_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # self.votes = []

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO paintings (title, description, price, creator_id) VALUES (%(title)s, %(description)s, %(price)s, %(creator_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_paintings(cls):
        query = 'SELECT * FROM paintings'
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM paintings WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_all_paintings_with_users(cls):
        query = 'SELECT * FROM paintings LEFT JOIN users ON paintings.creator_id = users.id;'
        paintings = connectToMySQL(cls.db).query_db(query)
        results=[]
        for painting in paintings:
            data = {
                'id' : painting['creator_id'],
                'first_name' : painting['first_name'],
                'last_name' : painting['last_name'],
                'email' : painting['email'],
                'password' : painting['password'],
                'created_at' : painting['users.created_at'],
                'updated_at' : painting['users.updated_at']
            }
            one_painting = cls(painting)
            one_painting.creator = User(data)
            results.append(one_painting)
        return results

    @classmethod 
    def get_one_painting_with_users(cls, data):
        query = 'SELECT * FROM paintings LEFT JOIN users ON paintings.creator_id = users.id WHERE paintings.id = %(id)s;'
        painting = connectToMySQL(cls.db).query_db(query, data)
        data = {
            'id' : painting[0]['users.id'],
            'first_name' : painting[0]['first_name'],
            'last_name' : painting[0]['last_name'],
            'email' : painting[0]['email'],
            'password' : painting[0]['password'],
            'created_at' : painting[0]['users.created_at'],
            'updated_at' : painting[0]['users.updated_at']
        }
        one_painting = cls(painting[0])
        one_painting.creator = User(data)
        return one_painting

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            flash('Title must have a value greater than 2 characters!')
            is_valid = False
        if len(painting['description']) < 10:
            flash('Description must have a value greater than 10 characters!')
            is_valid = False
        if len(painting['price']) < 1:
            flash('Price must have a value greater than zero!')
            is_valid = False
        return is_valid








    # @classmethod
    # def get_all_paintings_with_votes(cls):
    #     query = 'SELECT * FROM paintings LEFT JOIN users ON paintings.creator_id = users.id LEFT JOIN votes ON paintings.id = votes.painting_id ORDER BY paintings.created_at DESC;'
    #     paintings = connectToMySQL(cls.db).query_db(query)
    #     results=[]
    #     for painting in paintings:
    #             data = {
    #                 'id' : painting['users.id'],
    #                 'first_name' : painting['first_name'],
    #                 'last_name' : painting['last_name'],
    #                 'email' : painting['email'],
    #                 'password' : painting['password'],
    #                 'created_at' : painting['users.created_at'],
    #                 'updated_at' : painting['users.updated_at']
    #             }
    #             one_painting = cls(painting)
    #             one_painting.creator = User(data)
    #             results.append(one_painting)
    #     return results
