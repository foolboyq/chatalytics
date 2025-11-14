import os
from twitchAPI.object.eventsub import ChannelChatMessageEvent, ChannelSubscribeEvent, ChannelSubscriptionMessageEvent
from analytics_handler import message_analysis
from data_types.users import User

class EventHandler:
    def __init__(self, emote_list):
        """
        :param emote_list: dict of emotes {emote_name (str): Emote (class)}
        """
        self.emote_list = emote_list
        self.num_messages = 0     # Tracks number of messages
        self.chat_text = {}     # Dictionary counting words number {word (str): num_times_used (int)}
        self.chat_emotes = {}   # Dictionary counting emotes number {emote_name (str): num_times_used (int)}
        self.users = {}         # Dictionary containing user information
        self.save_data_file = os.path.abspath('./current_data.json')

    async def on_message(self, msg: ChannelChatMessageEvent):
        self.num_messages += 1
        chat_msg = msg.event.message
        user_name = msg.event.chatter_user_name
        user_id = msg.event.chatter_user_id
        message_analysis(chat_msg, self.chat_text, self.chat_emotes, self.emote_list)
        print(f'{user_name}: {chat_msg.text}')
        if user_id not in self.users:
            self.users[user_id] = User(user_id, user_name)
        self.users[user_id].messages += 1

    async def on_subscribe(self, sub: ChannelSubscribeEvent):
        user_id = sub.event.user_id
        if user_id not in self.users:
            self.users[user_id] = User(user_id, sub.event.user_name)
        self.users[user_id].add_subscription(sub.event.tier, sub.event.is_gift)

    async def on_resubscribe(self, sub: ChannelSubscriptionMessageEvent):
        user_id = sub.event.user_id
        if user_id not in self.users:
            self.users[user_id] = User(user_id, sub.event.user_name)
        self.users[user_id].add_subscription(sub.event.tier)
