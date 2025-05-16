from sproutware.db import db
from datetime import datetime as dt, timedelta
from .time import Time

class Seed(db.Model):
    __tablename__ = "Seeds"
    
    id = db.mapped_column(db.Integer, primary_key = True)
    name = db.mapped_column(db.String, nullable = False)
    category = db.mapped_column(db.String, nullable = False, default = "flower")
    hp = db.mapped_column(db.Integer, nullable = False, default = 100)
    xp = db.mapped_column(db.Integer, nullable = False, default = 0)
    is_watered = db.mapped_column(db.Boolean, default = False)
    time_of_watering = db.mapped_column(db.DateTime, nullable = True, default = None)
    is_planted = db.mapped_column(db.Boolean, nullable=False, default=False)    
    time_of_planting = db.mapped_column(db.DateTime, nullable = True, default = None)
    water_retention = db.mapped_column(db.Interval, nullable=False, default=timedelta(seconds=5)) # change this for different plants
    is_selected = db.mapped_column(db.Boolean, nullable=False, default=False)
    decay_amount = db.mapped_column(db.Integer, nullable = False, default = 10) # change this for different plants
    decay_interval = db.mapped_column(db.Interval, nullable=False, default=timedelta(seconds=15)) # change this for different plants
    produced_seeds = db.mapped_column(db.Boolean, nullable = False, default = False)
    time_of_maturity = db.mapped_column(db.DateTime, nullable = True, default = None)

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
        print(f'Attempting to water {self.name}...')
        # if self.is_planted == False:
        #     print(f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?")
        #     return f"{self.name} hasn't been planted yet. How could you water it if it isn't planted?"
        if self.is_watered:
            print(f'{self.name} is already watered! (if self.is_watered = {self.is_watered})')
            return self.time_until_waterable()
        
        if not self.is_waterable_check():
            time_left_to_water = self.time_until_waterable()
            seconds = int(time_left_to_water.total_seconds())
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{self.name} is already watered. Wait {minutes} min {seconds} sec."
        
        self.is_watered = True
        self.add_xp()
        self.add_hp()
        self.decay_hp()
        # self.time_until_waterable()
        self.time_of_watering = dt.now()
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
    
    def matured_time(self):
        if self.xp == 100:
            self.time_of_maturity = dt.now()
            return self.time_of_maturity


# CALLED IN MAIN FUNCTIONS

    # add 20 XP to plant
    def add_xp(self):
        print(f"Plant XP before watering: {self.xp}")
        self.xp += 20
        if self.xp >= 100:
            self.xp = 100
        print(f"Plant XP after watering: {self.xp}")
        return self.xp

    def add_hp(self):
        print(f"Plant HP before watering: {self.hp}")
        self.hp += 20
        if self.hp > 100:
            self.hp = 100
        print(f"Plant HP after watering, but before decay: {self.hp}")
        return self.hp

    # get the amount of time left until the next time the plant can be watered
    def time_until_waterable(self):
        if not self.is_watered or not self.time_of_watering:
            print('Plant is not watered, or does not have a time of watering ...')
            return None  # no cooldown needed bc plant is not planted or is not watered
 
        cooldown = self.water_retention
        print(f'{self.name}\'s Cooldown/Water Retention Value: {cooldown}')
        elapsed = dt.now() - self.time_of_watering
        print(f'Current time - last time plant was watered = {elapsed}')
        if elapsed > cooldown:  
            dry = self.reset_is_watered()
            db.session.commit()
            print(f'{self.name} should no longer be watered. is_watered: {self.is_watered}')
            return dry
        remaining = (cooldown - elapsed).total_seconds()
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        return f'{minutes} minutes, {seconds} seconds'
    
    def decay_hp(self):
        if self.time_of_watering == None:
            return
        now = dt.now()
        elapsed = now - self.time_of_watering
        print(f' {elapsed} (time elapsed) is {now} (now) - {self.time_of_watering} (last time it was watered)')
        print(f'Elapsed type: {type(elapsed)}')

        decay_cycles = elapsed // self.decay_interval
        print(f'Decay cycles type:{decay_cycles} (from dividing elapsed and self.decay_interval)')

        if decay_cycles > 0:
            self.hp -= decay_cycles * self.decay_amount
            self.hp = max(self.hp, 0)
            if self.hp == 0:
                self.dead_plant()
        
        db.session.commit()

    def dead_plant(self):
        if self.hp <= 0:
            seed_to_delete = db.session.execute(db.select(Seed).where(self.name == Seed.name)).scalar()
            db.session.delete(seed_to_delete)
            db.session.commit()
            print(f'{self.name} has reached 0 HP and has died! Poor thing... Don\'t forget to water!')
        else:
            pass