import os
import asyncio

from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope

from events_handler import EventHandler
from emotes import EmoteList

# DoggieLogger App Credentials saved in local environment variables
APP_ID = os.getenv("TWITCH_APP_ID")
APP_SECRET = os.getenv("TWITCH_APP_SECRET")
TARGET_SCOPES = [AuthScope.USER_READ_CHAT]
BROADCASTER = 'wendilunar'
LISTENER = 'deepsdoggie'

async def run():
    # create the api instance and get user auth either from storage or website
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    # get the specified users
    list_user = await first(twitch.get_users(logins=LISTENER))
    broad_user = await first(twitch.get_users(logins=BROADCASTER))

    # Get broadcast channel emotes
    provider_list = ['BTTV', 'FFZ', '7TV']
    emote_list = EmoteList(provider_list, broad_user.id)
    twitch_channel_emotes = await twitch.get_channel_emotes(broad_user.id)
    twitch_global_emotes = await twitch.get_global_emotes()
    emote_list.add_twitch_emotes(twitch_channel_emotes)
    emote_list.add_twitch_emotes(twitch_global_emotes)

    # get class to handle events
    handler = EventHandler(emote_list.emote_list)

    # Create eventsub websocket instance and start the client.
    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    # We have to subscribe to the first topic within 10 seconds of eventsub.start() to not be disconnected.
    # Event subscription documentation:
    # https://pytwitchapi.dev/en/stable/modules/twitchAPI.eventsub.websocket.html
    # Listen to chat messages (broadcast_user_id, user_id, callback)
    await eventsub.listen_channel_chat_message(broad_user.id, list_user.id, handler.on_message)

    # Wait for input to match exit criteria before quitting
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

    # sort data dicts by value
    sorted_dict_text = dict(sorted(handler.chat_text.items(), key=lambda item: item[1], reverse=True))
    sorted_dict_emotes = dict(sorted(handler.chat_emotes.items(), key=lambda item: item[1], reverse=True))

    common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'you', 'was', 'for', 'on',
                    'are', 'as', 'with', 'so', 'did', 'he', 'she', 'is', 'were', 'your']
    for key in common_words:
        sorted_dict_text.pop(key, None)

    # print out top results
    print('\n\nTop words:')
    for idx, word in enumerate(sorted_dict_text):
        print(f'{word} - {sorted_dict_text[word]}')
        if idx > 4:
            break

    print('\n\nTop emotes:')
    for idx, emote in enumerate(sorted_dict_emotes):
        print(f'{emote} - {sorted_dict_emotes[emote]}')
        if idx > 4:
            break

    print(f'\n\nTotal messages captured: {handler.num_events}')


if __name__ == '__main__':
    asyncio.run(run())
