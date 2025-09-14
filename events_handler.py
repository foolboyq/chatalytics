import os
from twitchAPI.object.eventsub import ChannelChatMessageEvent
from analytics_handler import message_analysis

class EventHandler:
    def __init__(self, emote_list):
        """
        :param emote_list: dict of emotes {emote_name (str): Emote (class)}
        """
        self.emote_list = emote_list
        self.num_events = 0     # Tracks number of events
        self.chat_text = {}     # Dictionary counting words number {word (str): num_times_used (int)}
        self.chat_emotes = {}   # Dictionary counting emotes number {emote_name (str): num_times_used (int)}
        self.save_data_file = os.path.abspath('./current_data.json')

    async def on_message(self, msg: ChannelChatMessageEvent):
        self.num_events += 1
        chat_msg = msg.event.message
        msg_user = msg.event.chatter_user_name
        message_analysis(chat_msg, self.chat_text, self.chat_emotes, self.emote_list)
        print(f'{msg_user}: {chat_msg.text}')
