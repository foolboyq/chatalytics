from twitchAPI.object.eventsub import ChannelChatMessageEvent
from analytics_handler import message_analysis

class EventHandler:
    def __init__(self):
        self.num_events = 0
        self.chat_text = {}
        self.chat_emotes = {}

    async def on_message(self, msg: ChannelChatMessageEvent):
        chat_msg = msg.event.message
        msg_user = msg.event.chatter_user_name
        message_analysis(chat_msg, self.chat_text)
        print(f'{msg_user}: {chat_msg.text}')
