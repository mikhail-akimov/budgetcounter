from slackclient import SlackClient
from project.bot_tokens import oauth_access, bot_access


def send_test_msg():
    client = SlackClient(token='{}'.format(oauth_access))
    return client.api_call(
                    'chat.postMessage',
                    channel="general",
                    text="Writing some code!"
                )


if __name__ == '__main__':
    print(send_test_msg())

