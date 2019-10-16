import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import re
import sys
import os
import json
from config import token, group_id
import requests
import img2msg
import memgen

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


def send_message(peer, msg="", random=random.randint(-2147483648, 2147483647), attachment=None):
    if attachment is not None:
        vk.messages.send(peer_id=peer, message=msg, random_id=random, attachment=attachment)
    elif msg.strip() != "":
        vk.messages.send(peer_id=peer, message=msg, random_id=random)


def upload_photo(photo_path):
    img = {'photo': open(photo_path,"rb")}
    upload_resp = json.loads(requests.post(vk.photos.getMessagesUploadServer()['upload_url'], files=img).text)
    photo_id = upload_resp['photo']
    if photo_id is not 'null':
        photo_id = vk.photos.saveMessagesPhoto(photo=upload_resp['photo'], server=upload_resp['server'], hash=upload_resp['hash'])[0]['id']
        attachment = str('photo-'+str(group_id)+'_'+str(photo_id))
        return attachment
    else:
        return None

joker_images = ["joker/" + img for img in os.listdir("joker")]

def rndmsg_mode(msg_list, mentions):
    if not mentions:
        mentions = ['rndmsg']
    joker = ['джокер', 'joker', 'джокера', 'джокеру', 'джокером', 'джокере']
    mentions_re = re.compile(r"\b(" + "|".join(mentions) + r")\b")
    joker_re = re.compile(r"\b(" + "|".join(joker) + r")\b")
    while True:
        longpoll = VkBotLongPoll(vk_session, group_id)
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    e = event.object
                    attachments = list(filter(lambda a: a.get("type") =="photo", e.attachments))
                    # on joker command send joker meme
                    if joker_re.search(e.text.lower()):
                        memgen.make_meme(random.choice(joker_images), "temp.jpg", msg_list)
                        photo = upload_photo("temp.jpg")
                        try:
                            send_message(e.peer_id, attachment=photo)
                        except Exception as e:
                            print(e)
                    # on mention + photo reply to photo
                    elif (mentions_re.search(e.text.lower()) or (e.reply_message and e.reply_message.get("from_id") == -group_id)) and len(attachments) != 0:
                        img_resp = vk_session.http.get(attachments[0].get("photo").get("sizes")[-1].get("url"), allow_redirects=True)
                        open('temp', 'wb').write(img_resp.content)
                        try:
                            send_message(e.peer_id, img2msg.get_msg(msg_list, "temp"))
                        except Exception as e:
                            print(e)
                    # on mention or reply send random message
                    elif mentions_re.search(e.text.lower()) or (e.reply_message and e.reply_message.get("from_id") == -group_id):
                        try:
                            send_message(e.peer_id, random.choice(msg_list))
                        except Exception as e:
                            print(e)
                    # on photo with no mentions has a chance to reply to it
                    elif len(attachments) != 0 and random.randint(1,10) == 1:
                        img_resp = vk_session.http.get(attachments[0].get("photo").get("sizes")[-1].get("url"), allow_redirects=True)
                        open('temp', 'wb').write(img_resp.content)
                        try:
                            send_message(e.peer_id, img2msg.get_msg(msg_list, "temp"))
                        except Exception as e:
                            print(e)
                    # has a chance to reply to any message
                    elif random.randint(1, 100) == 1:
                        try:
                            send_message(e.peer_id, random.choice(msg_list))
                        except Exception as e:
                            print(e)
        except requests.exceptions.ReadTimeout as timeout:
            continue




def main():
    if len(sys.argv) == 2:
        cf = open(sys.argv[1], "r")
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
            print("(First line - filename; second line - delimiter; then mentions, each on a new line)")
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
