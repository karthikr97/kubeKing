import os
import sys

from slack_sdk import WebClient


client = WebClient(token=os.environ.get('SLACK_TOKEN'))
channel = os.environ.get('CHANNEL_ID')

def parse_body(body):
    token = ""
    user_name = ""
    try:
        body = body.split("&")
        for parameter in body:
            parameter = parameter.split("=")
            if parameter[0] == "user_name":
                user_name = parameter[1]
            if parameter[0] == "token":
                token = parameter[1]
            if "text" in parameter[0]:
                text = parameter[1]
                text = text.split("+")
                command = ""
                command_func = ""
                namespace = ""
                pod_name = ""
                if len((text)) < 3:
                    raise Exception("invalid arguments")
                if len(text) >= 3:
                    command = text[0]
                    command_func = text[1]
                    namespace = text[2]
                if len(text) == 4:
                    pod_name = text[3]
                print(user_name + "::" + token)
                print("command: %s %s , namespace: %s , pod: %s, parameter: %s  " %
                      (command, command_func, namespace, pod_name, parameter), file=sys.stderr)  # Debug
                return (user_name,command, command_func, namespace, pod_name)
    except (IndexError, ValueError) as e:
        # print(e, file=sys.stderr)
        raise Exception("invalid arguments")


def slack_message(text):
    response = client.chat_postMessage(
        channel=channel,
        text=text,
    )
    assert response["ok"]
    assert response["message"]["text"]
    return


def slack_upload(pod):
    response = client.files_upload(
        channels=channel,
        file="tmp/%s.txt" % pod)
    assert response["ok"]
    os.system("rm -rf tmp/%s.txt" % pod)
    return "Processing...", 200


def getChList():
    chlist = {}
    for result in client.conversations_list():
        for channel in result["channels"]:
            chname = channel["name"]
            chid = channel["id"]
            chlist.update({chname: chid})
            print(f"Found ch name: {chname}  ID: {chid}")
    return chlist