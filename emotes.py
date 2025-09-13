import requests


class EmoteUrl:
    def __init__(self, size, url):
        self.size = size
        self.url = url

    def to_dict(self):
       return dict(size=self.size, url=self.url)

class Emote:
    def __init__(self, code, provider):
        self.code = code
        self.provider = provider
        self.urls = []

    def to_dict(self):
        return dict(
            code=self.code,
            provider=self.provider,
            urls=[u.to_dict() for u in self.urls]
        )

    def add_url(self, size, url):
        self.urls.append(EmoteUrl(size, url))

class EmoteList:
    def __init__(self, provider_list, channel_id):
        self.emote_list = []

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
                emote.add_url(size, url)
            self.emote_list.append(emote)

    def get_bttv_channel_emotes(self, channel_id):
        url = f"https://api.betterttv.net/3/cached/users/twitch/{channel_id}"
        data = run_request(url)

        for e in data['channelEmotes'] + data['sharedEmotes']:
            emote = Emote(code=e['code'], provider='BTTV')
            for size in ['1x', '2x', '3x']:
                url = f"https://cdn.betterttv.net/emote/{e['id']}/{size}"
                emote.add_url(size, url)
            self.emote_list.append(emote)

    def get_ffz_channel_emotes(self, channel_id):
        url = f"https://api.frankerfacez.com/v1/room/id/{channel_id}"
        data = run_request(url)
        set_id = data['room']['set']

        for e in data['sets'][str(set_id)]['emoticons']:
            emote = Emote(code=e['name'], provider='FFZ')
            for u in (e.get('animated') or e['urls']).items():
                size = f'{u[0]}x'
                url = u[1]
                emote.add_url(size, url)
            self.emote_list.append(emote)

    def get_7tv_channel_emotes(self, channel_id):
        url = f"https://7tv.io/v3/users/twitch/{channel_id}"
        data = run_request(url)

        for e in data['emote_set']['emotes']:
            emote = Emote(code=e['name'], provider='7TV')
            host = e['data']['host']
            template = 'https:' + host['url']
            for file in host['files']:
                if file['format'] != 'WEBP':
                    continue
                size = file['name'].replace('.webp', '')
                url = f"{template}/{file['name']}"
                emote.add_url(size, url)
            self.emote_list.append(emote)

def run_request(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()