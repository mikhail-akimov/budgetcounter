from slack_utility import bot_init, IncomingMessage, User
from time import sleep
from db_utility import check_user, add_user


def main_loop():
    slack_api = bot_init()

    if slack_api.rtm_connect():
        print('BOT connected and ready to chat!')
        while True:
            data = IncomingMessage(slack_api.rtm_read())
            if data.data:
                message = data.parse_message()
                print(message)
                if message.user_id:
                    user = User(slack_api, message.user_id)
                    print(user.check_reg())
                else:
                    pass
            else:
                sleep(1)


if __name__ == '__main__':
    main_loop()
