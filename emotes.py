import requests

class Emote:
    def __init__(self, code, provider):
        self.code = code
        self.provider = provider
        self.urls = {}

    def to_dict(self):
        return dict(
            code=self.code,
            provider=self.provider,
            urls=[u.to_dict() for u in self.urls]
        )

class EmoteList:
    def __init__(self, provider_list, channel_id):
        self.emote_list = {}

        for provider in provider_list:
            if provider == 'BTTV':
                self.get_bttv_channel_emotes(channel_id)
            elif provider == 'FFZ':
                self.get_ffz_channel_emotes(channel_id)
            elif provider == '7TV':
                self.get_7tv_channel_emotes(channel_id)

    def add_twitch_emotes(self, twitch_emotes):
        for e in twitch_emotes:
            emote = Emote(code=e.name, provider='TWITCH')
            for scale in e.scale:
                values = {
                    'id': e.id,
                    'format': 'default',
                    'theme_mode': e.theme_mode[0],
                    'scale': scale,
                }
                url = twitch_emotes.template.replace('{{', '{').replace('}}', '}').format(**values)
                size = f"{int(float(scale))}x"
                emote.urls[size] = url
            self.emote_list[emote.code] = emote

    def get_bttv_channel_emotes(self, channel_id):
        emotes = []

        url = f"https://api.betterttv.net/3/cached/users/twitch/{channel_id}"
        data = run_request(url)
        emotes.extend(data['channelEmotes'])
        emotes.extend(data['sharedEmotes'])

        global_url = 'https://api.betterttv.net/3/cached/emotes/global'
        emotes.extend(run_request(global_url))

        for e in emotes:
            emote = Emote(code=e['code'], provider='BTTV')
            for size in ['1x', '2x', '3x']:
                url = f"https://cdn.betterttv.net/emote/{e['id']}/{size}"
                emote.urls[size] = url
            self.emote_list[emote.code] = emote

    def get_ffz_channel_emotes(self, channel_id):
        emotes = []

        url = f"https://api.frankerfacez.com/v1/room/id/{channel_id}"
        data = run_request(url)
        emotes.extend(data['sets'][str(data['room']['set'])]['emoticons'])

        global_url = 'https://api.frankerfacez.com/v1/set/global'
        global_data = run_request(global_url)
        for set_id in global_data['default_sets']:
            emotes.extend(global_data['sets'][str(set_id)]['emoticons'])

        for e in emotes:
            emote = Emote(code=e['name'], provider='FFZ')
            for u in (e.get('animated') or e['urls']).items():
                size = f'{u[0]}x'
                url = u[1]
                emote.urls[size] = url
            self.emote_list[emote.code] = emote

    def get_7tv_channel_emotes(self, channel_id):
        emotes = []
        url = f"https://7tv.io/v3/users/twitch/{channel_id}"
        data = run_request(url)
        emotes.extend(data['emote_set']['emotes'])

        global_url = 'https://7tv.io/v3/emote-sets/global'
        data_global = run_request(global_url)
        emotes.extend(data_global['emotes'])

        for e in emotes:
            emote = Emote(code=e['name'], provider='7TV')
            host = e['data']['host']
            template = 'https:' + host['url']
            for file in host['files']:
                if file['format'] != 'WEBP':
                    continue
                size = file['name'].replace('.webp', '')
                url = f"{template}/{file['name']}"
                emote.urls[size] = url
            self.emote_list[emote.code] = emote

def run_request(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()