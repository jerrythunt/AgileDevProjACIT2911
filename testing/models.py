from db import db
from datetime import datetime as dt
import time

class Time(db.Model):
    __tablename__ = "Time"

    id = db.mapped_column(db.Integer, primary_key = True)
    current_time = db.mapped_column(db.DateTime, nullable = False, default = None)

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
        return f'A user planted a {self.name} on {self.time_of_planting}'
    
    def water_plant(self):
        if self.is_watered == True:
            return f"{self.name} is already watered!"
            pass
        
        self.is_watered = True
        self.growth = self.growth + 20
        self.time_of_watering = dt.now()
        if self.hp > 80:
            self.hp = 100
        self.hp = self.hp + 20
        db.session.commit()
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








