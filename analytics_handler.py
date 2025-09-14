from twitchAPI.object.eventsub import ChatMessage

def message_analysis(msg: ChatMessage, words, emotes, emote_list):
    for fragment in msg.fragments:
        if fragment.type == 'text':
            message_split = fragment.text.split(' ')
            for word in message_split:
                if word in emote_list:
                    increment_values(emotes, word)
                    continue
                key = word.lower()
                if key.isalpha():
                    increment_values(words, key)
        elif fragment.type == 'emote':
            key = fragment.text
            increment_values(emotes, key)

def increment_values(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1