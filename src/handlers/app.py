from flask import Flask
from flask import make_response
from flask import request
from slack_sdk.webhook import WebhookClient

from src.auth.slackauth import validate_token
from src.kubeutils.kube import Kube
from src.slackUtils.slackUtil import parse_body, slack_message, slack_upload, getChList


app = Flask(__name__)
kubecl = Kube()


@app.route('/', methods=['POST'])
@validate_token
def sl():
    try:
        user, cmd, cmd_fnc, ns, pod = (parse_body(request.get_data().decode('utf8')))
        if cmd == "get" and cmd_fnc == "pods" and ns != "":
            slack_message(f"{user} requested: {cmd} {cmd_fnc} {ns}")
            slack_message(kubecl.pods(ns))
            return f"{cmd} {cmd_fnc} {ns}"
        if cmd == "get" and cmd_fnc == "logs" and ns != "" and pod != "":
            slack_message(f"{user} requested: {cmd} {cmd_fnc} {ns} {pod}")
            slack_upload(kubecl.writeLogs(ns, pod))
            return f"{cmd} {cmd_fnc} {ns} {pod}"
        else: return "Invalid Command"
    except Exception as e:
        return "Invalid Command"


@app.route('/get-channels', methods=['GET'])
def getcl():
    return getChList()

@app.route("/slack/events", methods=["POST"])
@validate_token
def slack_app():
    # Handle a slash command invocation
    if "command" in request.form \
            and request.form["command"] == "/kube":
        response_url = request.form["response_url"]
        text = request.form["text"]
        webhook = WebhookClient(response_url)
        # Send a reply in the channel
        response = webhook.send(text=f"You said '{text}'")
        print("acknowledgeeEEEE")
        # Acknowledge this request
        return make_response("", 200)

    return make_response("", 404)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
