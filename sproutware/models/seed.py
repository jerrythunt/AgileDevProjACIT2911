from sproutware.db import db
from datetime import datetime as dt, timedelta
from .time import Time

class Seed(db.Model):
    __tablename__ = "Seeds"
    
    id = db.mapped_column(db.Integer, primary_key = True)
    name = db.mapped_column(db.String, nullable = False)
    # image_id = db.mapped_column(db.Integer, db.ForeignKey("Images.id"), nullable=False)
    # image = db.relationship("Image", foreign_keys=[image_id])
    # phase_images = db.relationship("Image", back_populates="plant", foreign_keys=[Image.plant_id])
    category = db.mapped_column(db.String, nullable = False, default = "flower")
    hp = db.mapped_column(db.Integer, nullable = False, default = 100)
    xp = db.mapped_column(db.Integer, nullable = False, default = 0)
    is_watered = db.mapped_column(db.Boolean, default = False)
    time_of_watering = db.mapped_column(db.DateTime, nullable = True, default = None)
    is_planted = db.mapped_column(db.Boolean, nullable=False, default=False)    
    time_of_planting = db.mapped_column(db.DateTime, nullable = True, default = None)
    water_retention = db.mapped_column(db.Interval, nullable=False, default=timedelta(seconds=10))
    buffer_interval = db.mapped_column(db.Interval, nullable=False, default=timedelta(seconds=5))
    last_decay_time = db.mapped_column(db.DateTime, nullable=True, default=None)


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
        # if self.is_planted == False:
        #     print(f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?")
        #     return f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?"
        if self.is_watered:
            return self.time_until_waterable()
        
        if not self.is_waterable_check():
            time_left_to_water = self.time_until_waterable()
            seconds = int(time_left_to_water.total_seconds())
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{self.name} is already watered. Wait {minutes} min {seconds} sec."
        
        self.is_watered = True
        self.add_xp()
        self.time_of_watering = dt.now()
        self.add_hp()
        self.time_until_waterable()
        db.session.commit()

        return f"{self.name} has been watered. It looks very happy!"
        # return self.time_until_waterable()
    
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
            self.xp = 100
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
    
    # def decay_hp(self, current_time=None):
    #     if current_time is None:
    #         current_time = dt.now()
        
    #     if self.time_of_watering is None:
    #         return
        
    #     if self.last_decay_time is None:
    #         self.last_decay_time = self.time_of_watering + self.water_retention

    #     decay_time = (current_time - self.time_of_watering) - self.water_retention
    #     if decay_time.total_seconds() <= 0:
    #         return
        
    #     # time since it was last decayed
    #     time_since_last_decay = current_time - self.last_decay_time
    #     # number of intervals it has nto been watered
    #     num_of_decay_intervals = time_since_last_decay // self.buffer_interval

    #     if num_of_decay_intervals >= 1:
    #         decay_amount = num_of_decay_intervals * 5
    #         if self.hp >= decay_amount:
    #             self.hp -= decay_amount
    #         else:
    #             self.hp = 0

    #         # update time of last decay in database
    #         self.last_decay_time += num_of_decay_intervals * self.buffer_interval
    #         db.session.commit()
    
    def decay_hp(self, current_time=None):
        if current_time is None:
            current_time = dt.now()

        if self.time_of_watering is None:
            return

        # Set last_decay_time the *first* time decay runs
        if self.last_decay_time is None:
            self.last_decay_time = self.time_of_watering + self.water_retention
            db.session.commit()
            return  # don't decay now — start tracking after retention period

        # If we're still in the retention period, do nothing
        if current_time < self.last_decay_time:
            return

        # Calculate how many intervals have passed since last decay
        time_since_last_decay = current_time - self.last_decay_time
        interval_seconds = self.buffer_interval.total_seconds()
        intervals = int(time_since_last_decay.total_seconds() // interval_seconds)

        if intervals < 1:
            return  # not enough time passed yet for next decay

        # Decay once per interval
        decay_amount = intervals * 5
        self.hp = max(self.hp - decay_amount, 0)

        # Move forward the last_decay_time
        self.last_decay_time += timedelta(seconds=intervals * interval_seconds)

        db.session.commit()




    # def grab_image(self):
    #     images = db.session.execute(db.select(Image).where(Image.plant_id == self.id).order_by(Image.xp_amount)).scalars()

    #     for img in reversed(images):  
    #         if self.xp >= img.xp_amount:
    #             self.image_id = img.id
    #             db.session.commit()
    #             break
