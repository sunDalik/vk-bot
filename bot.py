import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from config import token, group_id

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def send_message(peer, msg, random):
    vk.messages.send(peer_id=peer, message=msg, random_id=random)


def msg_mode():
    while True:
        peer = input("Choose peer: ")
        print("You can start messaging!\nType /exit to exit mode or /change to change peer.")
        while True:
            msg = input()
            if msg == "/change":
                break
            elif msg == "/exit":
                return
            else:
                send_message(peer, msg, random.randint(1, 1000000000) )


def get_mode():
    print("You will now receive message events!\nUse Ctrl-C to exit mode.(ummm doesnt work actually)")
    try:
        while True:
            longpoll = VkBotLongPoll(vk_session, group_id)
            try:
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        e = event.object
                        print (e)
                        # print('New message: ' + e.text)
            except requests.exceptions.ReadTimeout as timeout:
                continue
    except KeyboardInterrupt:
        return


def main():
    while True:
        print("\n==Choose mode==")
        print("1. Message mode")
        print("2. Get mode")
        print("exit. Exit")
        option = input()
        if option == "1":
            msg_mode()
        elif option == "2":
            get_mode()
        elif option == "exit":
            return 0
        else:
            print("Invalid mode")

main()
