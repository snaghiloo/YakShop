class Herd(object):
    def __init__(self, yaks_list=[]):
        self.yaks_list = yaks_list

    def total_milk(self, elapsed_time):
        total_milk = 0.0
        for yak in self.yaks_list:
            total_milk += yak.amount_of_milk(elapsed_time)
        return total_milk

    def total_skins(self, elapsed_time):
        total_skins = 0
        for yak in self.yaks_list:
            total_skins += yak.skins(elapsed_time)
        return total_skins

    def get_yaks_list(self):
        return self.yaks_list

    def set_yak_list(self, yak_list):
        self.yaks_list = yak_list


global_herd = Herd()

