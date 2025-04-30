from db import db
from datetime import datetime as dt
from datetime import timedelta
import time

# Classes are blueprints to create a real-world object
# Objects have attributes that define what they ARE (variable)
# Objects have methods that define what they DO (functions) 

# Create a table, inherit 'db.Model', otherwise it wont add to database!!
class Time(db.Model):
    # Declare the tablename
    __tablename__ = "Time"

    # Declare attributes that will populate database 
    # attribute = (db.mapped_column(db.DataType, options = insert_option))
    id = db.mapped_column(db.Integer, primary_key = True)
    name = db.mapped_column(db.String, nullable = False)
    current_time = db.mapped_column(db.DateTime, nullable = False, default = dt.now())

# class Image(db.Model):
#     __tablename__ = "Images"

#     id = db.mapped_column(db.Integer, primary_key = True)
#     path = db.mapped_column(db.String, nullable = False)
#     plant = db.mapped_column()

class Seed(db.Model):
    __tablename__ = "Seeds"
    
    id = db.mapped_column(db.Integer, primary_key = True)
    name = db.mapped_column(db.String, nullable = False)
    # image_id = db.mapped_column(db.Integer, nullable = False)
    category = db.mapped_column(db.String, nullable = False, default = "flower")
    hp = db.mapped_column(db.Integer, nullable = False, default = 100)
    growth = db.mapped_column(db.Integer, nullable = False, default = 0)
    is_watered = db.mapped_column(db.Boolean, default = False)
    time_of_watering = db.mapped_column(db.DateTime, nullable = True, default = None)
    is_planted = db.mapped_column(db.Boolean, nullable=False, default=False)    
    time_of_planting = db.mapped_column(db.DateTime, nullable = True, default = None)
    water_interval = db.mapped_column(db.DateTime)

    # Declare methods that we can call to update attributes
    # def function(self):
    # 'self' allows the object instance to call itself, so you don't have to hardcode
    def plant(self):
        # If seed object is planted, dont allow this method
        if self.is_planted == True:
            print(f'{self.name} has been planted already!')
            return f'{self.name} has been planted already!'
        # Else, run this logic 
        self.is_planted = True
        # dt.now() grabs the current time and stores it as an object
        self.time_of_planting = dt.now()
        # Update the database
        db.session.commit()
        # Debug check
        print(f'A user planted a {self.name} on {self.time_of_planting}')
        return self.is_planted
    
    def water_plant(self):
        if self.is_planted == False:
            print(f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?")
            return f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?"
        if self.is_watered == True:
            print(f"{self.name} is already watered! You have to wait 5 minutes before watering again")
            return f"{self.name} is already watered! You have to wait 5 minutes before watering again"
        
        self.is_watered = True
        self.time_of_watering = dt.now()

        self.add_xp()
        if self.hp > 100:
            self.hp = 100

        db.session.commit()

        print(f"{self.name} has been watered. It looks very happy!")
        return f'A user watered a {self.name} at {str(self.time_of_watering)}!'
    
    # Reset is_watered status
    def reset_is_watered(self):
        # Check if plant has been watered, otherwise do nothing
        if self.is_watered:
            elapsed = dt.now() - self.time_of_watering
            if elapsed >= timedelta(minutes=5):
                self.is_watered = False
                db.session.commit()
                
        return f'{self.name} needs to be watered!'  

    # return True or False whether the plant can be watered again
    def is_waterable_check(self):
        self.reset_is_watered()
        return not self.is_watered

    # get the amount of time left until the next time the plant can be watered
    def time_until_waterable(self):
        if not self.is_watered or not self.time_of_watering:
            return None  # no cooldown needed bc plant is not planted or is already watered

        cooldown = timedelta(minutes=5)
        elapsed = dt.now() - self.time_of_watering
        remaining = cooldown - elapsed

        if remaining.total_seconds() <= 0:
            return None
        return remaining

    # add 20 XP to growth
    def add_xp(self):
        self.growth += 20
        print(f"Plant XP: {self.growth}")

    def grow_stage(self):
        # if self.growth >= 40:, display new photo
            pass








