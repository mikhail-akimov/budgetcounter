from slackclient import SlackClient
from bot_tokens import oauth_access, bot_access
import slack_utility
from time import sleep
from db_utility import check_user, add_user


def main_loop():
    slack_api = slack_utility.connect()

    if slack_api.rtm_connect():
        print('BOT connected and ready to chat!')
        while True:
            data = slack_api.rtm_read()
            if slack_utility.parse_message(data):
                print(slack_utility.parse_message(data))
                userid = slack_utility.parse_message(data)['user_id']
                profile = slack_utility.get_user_profile(slack_api, userid)
                print(profile)
                if check_user(userid):
                    print('There is!')
                else:
                    print('There is no such user. Let`s add him!')
                    add_user(userid, profile['name'])
            else:
                sleep(1)


if __name__ == '__main__':
    main_loop()
