from slackclient import SlackClient
from bot_tokens import oauth_access, bot_access


def connect():
    slack_api_client = SlackClient(bot_access)
    return slack_api_client


def send_test_msg(slack_api_client):
    response = slack_api_client.api_call(
                    'chat.postMessage',
                    channel="general",
                    text="Writing some code!"
                )
    return response


def parse_message(msg):
    if msg:
        result = {}
        for line in msg:
            if line['type'] == 'message':
                result['user_id'] = line['user']
                result['message_text'] = line['text']
                result['message_id'] = line['client_msg_id']
                result['channel'] = line['channel']
    else:
        result = None
    return result


def get_user_profile(client, userid):
    user_profile = {}
    user = client.api_call('users.info', user=userid)['user']
    user_profile['id'] = user['id']
    if user['profile']['display_name'] != '':
        user_profile['name'] = user['profile']['display_name']
    else:
        user_profile['name'] = user['real_name']
    return user_profile

