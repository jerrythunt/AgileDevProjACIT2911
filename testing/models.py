from db import db
from datetime import datetime as dt
import time

class Time(db.Model):
    __tablename__ = "Time"

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

    def plant(self):
        self.is_planted = True
        self.time_of_planting = dt.now()
        db.session.commit()
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
        self.growth = self.growth + 20
        self.time_of_watering = dt.now()
        if self.hp > 80:
            self.hp = 100
        self.hp = self.hp + 20
        db.session.commit()
        print(f"{self.name} has been watered. It looks very happy!")
        return f'A user watered a {self.name} at {str(self.time_of_watering)}!'
    
    def reset_is_watered(self):
        self.is_watered = False
        db.session.commit()
        # while self.is_watered == False
        ## self.hp - 1 
        ## time.stop(30)
        return f'{self.name} needs to be watered!'
    
    def grow_stage(self):
        # if self.growth >= 40:, display new photo
            pass








