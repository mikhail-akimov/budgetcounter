from slackclient import SlackClient
from bot_tokens import oauth_access, bot_access
from db_utility import check_user, add_user


def bot_init():
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


class IncomingMessage:
    def __init__(self, data):
        self.data = data
        self.type = None
        self.user_id = None
        self.text = None
        self.client_msg_id = None
        self.team = None
        self.channel = None
        self.event_ts = None
        self.ts = None

    def parse_message(self):
        if self.data[0]['type'] == 'message':
            return Message(self.data)
        elif self.data[0]['type'] == 'hello':
            return HelloMessage(self.data)
        return self


class HelloMessage(IncomingMessage):
    def __init__(self, data):
        super().__init__(data)

    def __str__(self):
        return 'Hello!'


class Message(IncomingMessage):
    def __init__(self, data):
        super().__init__(data)
        self.type = self.data[0]['type']
        self.user_id = self.data[0]['user']
        self.text = self.data[0]['text']
        self.client_msg_id = self.data[0]['client_msg_id']
        self.team = self.data[0]['team']
        self.channel = self.data[0]['channel']
        self.event_ts = self.data[0]['event_ts']
        self.ts = self.data[0]['ts']

    def __str__(self):
        return '{} wrote {} in {}'.format(self.user_id, self.text, self.channel)


class UserTyping(IncomingMessage):
    def __init__(self, data):
        super().__init__(data)


class DesktopNotification(IncomingMessage):
    def __init__(self, data):
        super().__init__(data)


class OutgoingMessage:
    def __init__(self):
        pass


class User:
    def __init__(self, slack_api, user_id):
        self.slack_api = slack_api
        self.user_id = user_id

    def check_reg(self):
        if check_user(self.user_id):
            print('User found!')
            return RegisteredUser(self.slack_api, check_user(self.user_id)[0], check_user(self.user_id)[1])
        else:
            user_profile = self.get_user_profile()
            print('Registering user...')
            return RegisteredUser(self.slack_api, user_profile['id'], user_profile['username'])

    def get_user_profile(self):
        user_profile = {}
        profile = self.slack_api.api_call('users.info', user=self.user_id)['user']
        user_profile['id'] = profile['id']
        if profile['profile']['display_name'] != '':
            user_profile['username'] = profile['profile']['display_name']
        else:
            user_profile['username'] = profile['real_name']
        return user_profile

    def register_user(self):
        pass


class RegisteredUser(User):
    def __init__(self, slack_api, user_id, username):
        super().__init__(slack_api, user_id)
        self.username = username

    def __str__(self):
        return '{} {}'.format(self.user_id, self.username)


class NewUser(User):
    def __init__(self, slack_api, user_id):
        super().__init__(slack_api, user_id)
