import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

@app.command("/webhook")
def hello_command(ack, body):
    print('Receiving event')
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")

@app.message("hello")
def message_hello(message, say):
    print('Receiving hello')
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# All the magic happens here
@app.message("bug")
def fix_bug(message, say):
    print('receiving bug message')
    say(text="I will fix it!")

@app.event("app_mention")
def event_test(body, say):
    say(text="Hi there!", channel=body['event']['channel'])

@app.event("message")
def handle_message_events(body, say):
    print('received message event')
    say(text="Hi, how are you?", channel=body['event']['channel'])

if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()


# web_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

# def message(channel_id: str, text: str):
#     try:
#         # Post a message to a channel
#         response = web_client.chat_postMessage(channel=channel_id, text=text)
#     except SlackApiError as e:
#         assert e.response["ok"] is False
#         assert e.response["error"]
#         print(f"Got an error: {e.response['error']}")

# def handle_app_mention(socket_mode_request: SocketModeRequest, web_client: WebClient):
#     payload = socket_mode_request.payload
#     event = payload.get("event", {})
#     channel_id = event.get("channel")
#     text = event.get("text")
#     if not channel_id or not text:
#         return
#     message(channel_id, "Hello, I am your bot!")

# if __name__ == "__main__":
#     client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=web_client)
#     client.socket_mode_request_listeners.append(handle_app_mention)
#     client.connect()
#     client.start()
