from datetime import date


class User:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.messages = 0
        self.subscriptions = []

    def add_subscription(self, tier:str):
        self.subscriptions.append(Subscription(tier))

class Subscription:
    def __init__(self, tier:str, gifted:bool=False):
        self.tier = int(tier[0])
        self.date = date.today()
        self.gifted = gifted