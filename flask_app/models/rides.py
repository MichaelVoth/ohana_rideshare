from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.users import User


class Ride:
    DB = "ohana_rideshare_schema"

    def __init__(self, data):
        self.id = data['id']
        self.rider_id = data['rider_id']
        self.driver_id = data['driver_id']
        self.destination = data['destination']
        self.pick_up_location = data['pick_up_location']
        self.rideshare_date = data['rideshare_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.driver = None
        self.rider = None
    

#Create:
    @classmethod
    def save(cls, data):
        query = '''INSERT INTO rides (rider_id, destination, pick_up_location, rideshare_date, details)
                VALUES (%(rider_id)s, %(destination)s, %(pick_up_location)s, %(rideshare_date)s, %(details)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)
    

    @classmethod
    def save_driver(cls, data):
        query = '''
            UPDATE rides
            SET driver_id = %(id)s
            WHERE rides.id = %(ride_id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)
    

#Read:
    @classmethod
    def get_all_driverless_rides(cls):
        query = '''SELECT * FROM rides
                    JOIN users ON users.id = rider_id
                    WHERE driver_id IS NULL;'''
        results = connectToMySQL(cls.DB).query_db(query)
        driverless_rides = []
        for ride in results:
            ride_obj = cls(ride)
            user_data = {
                "id": ride["rider_id"],
                "first_name": ride["first_name"],
                "last_name": ride["last_name"],
                "email": ride["email"],
                "password": ride["password"],
                "created_at": ride["users.created_at"],
                "updated_at": ride["users.updated_at"]
            }
            ride_obj.rider = User(user_data)
            driverless_rides.append(ride_obj)

        return driverless_rides
    


    @classmethod
    def get_all_rides(cls):
        query = '''SELECT rides.id, rides.rider_id, rides.driver_id, rides.destination, rides.pick_up_location, rides.rideshare_date, rides.details, rides.created_at, rides.updated_at,
        rider.id AS rider_id, rider.first_name AS rider_first_name, rider.last_name AS rider_last_name, rider.email AS rider_email, rider.password AS rider_password, rider.created_at AS rider_created_at, rider.updated_at AS rider_updated_at,
        driver.id AS driver_id, driver.first_name AS driver_first_name, driver.last_name AS driver_last_name, driver.email AS driver_email, driver.password AS driver_password, driver. created_at AS driver_created_at, driver.updated_at AS driver_updated_at
        FROM rides
        JOIN users AS rider ON rider.id = rides.rider_id
        JOIN users AS driver ON driver.id = rides.driver_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        rides = []
        for ride in results:
            rider_data = {
                "id": ride["rider_id"],
                "first_name": ride["rider_first_name"],
                "last_name": ride["rider_last_name"],
                "email": ride["rider_email"],
                "password": ride["rider_password"],
                "created_at": ride['rider_created_at'],
                "updated_at": ride['rider_updated_at'],
            }

            driver_data = {
                "id": ride["driver_id"],
                "first_name": ride["driver_first_name"],
                "last_name": ride["driver_last_name"],
                "email": ride["driver_email"],
                "password": ride['driver_password'],
                'created_at': ride['driver_created_at'],
                "updated_at": ride['driver_created_at'],
                }
            ride_obj = cls(ride)
            ride_obj.rider = User(rider_data)
            ride_obj.driver= User(driver_data)
            rides.append(ride_obj)
        return rides


    @classmethod
    def get_ride_by_id(cls, id):
        query = '''SELECT rides.id, rides.rider_id, rides.driver_id, rides.destination, rides.pick_up_location, rides.rideshare_date, rides.details, rides.created_at, rides.updated_at,
        rider.id AS rider_id, rider.first_name AS rider_first_name, rider.last_name AS rider_last_name, rider.email AS rider_email, rider.password AS rider_password, rider.created_at AS rider_created_at, rider.updated_at AS rider_updated_at,
        driver.id AS driver_id, driver.first_name AS driver_first_name, driver.last_name AS driver_last_name, driver.email AS driver_email, driver.password AS driver_password, driver. created_at AS driver_created_at, driver.updated_at AS driver_updated_at
        FROM rides
        JOIN users AS rider ON rider.id = rides.rider_id
        JOIN users AS driver ON driver.id = rides.driver_id
        WHERE rides.id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        for ride in results:
            rider_data = {
                "id": ride["rider_id"],
                "first_name": ride["rider_first_name"],
                "last_name": ride["rider_last_name"],
                "email": ride["rider_email"],
                "password": ride["rider_password"],
                "created_at": ride['rider_created_at'],
                "updated_at": ride['rider_updated_at'],
            }

            driver_data = {
                "id": ride["driver_id"],
                "first_name": ride["driver_first_name"],
                "last_name": ride["driver_last_name"],
                "email": ride["driver_email"],
                "password": ride['driver_password'],
                'created_at': ride['driver_created_at'],
                "updated_at": ride['driver_created_at'],
                }
            ride_obj = cls(ride)
            ride_obj.rider = User(rider_data)
            ride_obj.driver= User(driver_data)
            print(vars(ride_obj))

        return ride_obj



#Update:
    @classmethod
    def update_ride_info(cls,data):
        query = '''UPDATE rides SET
                    
                    pick_up_location = %(pick_up_location)s,
                    
                    details = %(details)s
                    WHERE id = %(id)s;'''
        
        return connectToMySQL(cls.DB).query_db(query,data)


#Delete
    @classmethod
    def delete_ride(cls, id):
        query  = "DELETE FROM rides WHERE id = %(id)s;"
        
        return connectToMySQL(cls.DB).query_db(query, {"id": id}) 
    

    @classmethod
    def remove_driver(cls,id):
        query = '''UPDATE rides SET driver_id = NULL
                    WHERE rides.id = %(id)s;'''
        
        return connectToMySQL(cls.DB).query_db(query, {"id": id}) 
    

#Static
    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if not len(ride['destination']) > 3:
            flash("* Destination must be at least 3 characters.", 'create')
            is_valid = False
        if not len(ride['pick_up_location']) > 3:
            flash("* Location must be at least 2 characters.", 'create')
            is_valid = False
        if not len(ride['details']) > 10:
            flash("* Details must be at least 3 characters.", 'create')
            is_valid = False
        if not ride['rideshare_date']:
            flash("* Date is required.", 'create')
            is_valid = False


        return is_valid