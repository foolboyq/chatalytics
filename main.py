import os
import asyncio

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChatMessage
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope

# DoggieLogger App Credentials saved in local environment variables
APP_ID = os.getenv("TWITCH_APP_ID")
APP_SECRET = os.getenv("TWITCH_APP_SECRET")
TARGET_SCOPES = [AuthScope.USER_READ_CHAT]
BROADCASTER = 'wendilunar'
BROADCASTER = 'TheBurntPeanut'
LISTENER = 'deepsdoggie'

async def on_message(msg: ChatMessage):
    message_info = msg.event.message
    print(f'{msg.event.chatter_user_name}: {msg.event.message.text}')

async def run():
    # create the api instance and get user auth either from storage or website
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    # get the specified users
    list_user = await first(twitch.get_users(logins=LISTENER))
    broad_user = await first(twitch.get_users(logins=BROADCASTER))

    # create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # subscribing to the desired eventsub hook for our user
    # the given function (in this example on_follow) will be called every time this event is triggered
    # the broadcaster is a moderator in their own channel by default so specifying both as the same works in this example
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.

    # Listen to chat messages (broadcast_user_id, user_id, callback)
    await eventsub.listen_channel_chat_message(broad_user.id, list_user.id, on_message)

    # eventsub will run in its own process
    # so lets just wait for user input before shutting it all down again

    while True:
        try:
            print('Type "exit" to quit')
            user_in = input()
            if 'exit' in user_in:
                break
        except KeyboardInterrupt:
            break

    await eventsub.stop()
    await twitch.close()

if __name__ == '__main__':
    asyncio.run(run())
