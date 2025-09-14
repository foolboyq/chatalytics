from twitchAPI.object.eventsub import ChatMessage

def message_analysis(msg: ChatMessage, words: dict, emotes: dict, emote_list: dict):
    """
    :param msg: full chat message
    :param words: dict counting words times used {word (str): num_times_used (int)}
    :param emotes: dict counting emotes times used {emote_name (str): num_times_used (int)}
    :param emote_list: dict of emotes {emote_name (str): Emote (class)}
    """
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
    """
    :param dictionary: dictionary with labels as keys and number of times used as values
    :param key: name of key to increment value on
    """
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1