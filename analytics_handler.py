from twitchAPI.object.eventsub import ChatMessage

def message_analysis(msg: ChatMessage, words):
    for fragment in msg.fragments:
        if fragment.type == 'text':
            message_split = fragment.text.split(' ')
            for word in message_split:
                key = word.lower()
                if not key.isalpha():
                    continue
                if key in words:
                    words[key] += 1
                else:
                    words[key] = 1