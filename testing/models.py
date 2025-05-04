from db import db
from datetime import datetime as dt, timedelta
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
    xp = db.mapped_column(db.Integer, nullable = False, default = 0)
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
            return self.time_until_waterable()
        
        self.is_watered = True
        self.add_xp()
        self.time_of_watering = dt.now()
        self.add_hp()
        self.time_until_waterable()
        db.session.commit()

        print(f"{self.name} has been watered. It looks very happy!")
        return self.time_until_waterable()
    
    # Reset is_watered status
    def reset_is_watered(self):
        self.is_watered = False
        db.session.commit()
        return f'{self.name} needs to be watered!'
    
 # return True or False whether the plant can be watered again
    def is_waterable_check(self):
         self.reset_is_watered()
         return not self.is_watered
    
# CALLED IN MAIN FUNCTIONS

    # add 20 XP to plant
    def add_xp(self):
        self.xp += 20
        if self.xp >= 100:
            self.xp = 0
        print(f"Plant XP: {self.xp}")

    def add_hp(self):
        self.hp += 20
        if self.hp > 100:
            self.hp = 100
        print(f"Plant XP: {self.xp}")
    
    # get the amount of time left until the next time the plant can be watered
    def time_until_waterable(self):
        if not self.is_watered or not self.time_of_watering:
            print('Plant is not watered, or does not have a time of watering')
            return None  # no cooldown needed bc plant is not planted or is not watered
 
        cooldown = timedelta(minutes=0.1)
        print(f'Cooldown Value: {cooldown}')
        elapsed = dt.now() - self.time_of_watering
        if elapsed > cooldown:
            self.reset_is_watered()
            return None
        print(type(elapsed))
        remaining = (cooldown - elapsed).total_seconds()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        return f'{minutes} minutes, {seconds} seconds'






