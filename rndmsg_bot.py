import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from config import token, group_id

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

def send_message(peer, msg, random):
    if msg.strip() != "":
        vk.messages.send(peer_id=peer, message=msg, random_id=random)


def rndmsg_mode(msg_list, mentions):
    if not mentions:
        mentions = ['rndmsg']
    while True:
        longpoll = VkBotLongPoll(vk_session, group_id)
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    e = event.object
                    if any(mention in e.text.lower() for mention in mentions):
                        try:
                            send_message(e.peer_id, random.choice(msg_list), random.randint(1, 1000000000))
                        except Exception as e:
                            print(e)
        except requests.exceptions.ReadTimeout as timeout:
            continue


def main():
    print("Choose how would you like to set up a bot:")
    print("1. From stdin:")
    print("2. From file: ")
    option = input()
    if option == "1":
        print("Enter file with messages:")
        msgs_file = input()
        print("Enter messages delimiter:")
        delimiter = input()
        print("Enter mentions(words that will trigger the bot). Stop input with Ctrl-D")
        mentions = []
        while True:
            try:
                mentions.append(input())
            except EOFError:
                break

    elif option == "2":
        print("Enter config file:")
        print("(First line - filename; second line - delimiter; then delimiters, each on a new line)")
        configfile = input()
        cf = open(configfile, "r")
        mentions = []
        for i, line in enumerate(cf):
            line = line.rstrip("\n")
            if i == 0:
                msgs_file = line
            elif i  == 1:
                delimiter = line
            else:
                mentions.append(line)
    
    else:
        print("Unknown option")
        exit(1)

    f = open(msgs_file, "r")
    msgs = f.read()
    msg_list = msgs.split(delimiter)
    f.close()
    print("You are all set! Bot is working...")
    rndmsg_mode(msg_list, mentions)


main()
