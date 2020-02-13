from enum import Enum


class Sex(Enum):
    MALE = 1
    FEMALE = 2


class Yak(object):
    def __init__(self, name='', age=0, sex=Sex.FEMALE):
        self.name = name
        self.age = age
        self.sex = sex

    def amount_of_milk(self, elapsed_time):
        amount_of_milk = 0
        if self.sex == Sex.FEMALE:
            for d in range(elapsed_time):
                amount_of_milk += 50 - ((self.age + d) * 0.03)
        return amount_of_milk

    def skins(self, elapsed_time):
        skins = 0
        shave_day = (8 + self.age * 0.01) + 1
        for d in range(elapsed_time):
            if d % shave_day == 0 and d < elapsed_time:
                skins += 1
        return skins