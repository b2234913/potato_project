import argparse
from utils.potato_service import PotatoService
from config import config, users

if __name__ == "__main__":
    # os.system("pkill -9 Google Chrome")

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="please input the user name in users.py", required=True)
    args = parser.parse_args()

    user_name = args.user

PotatoService = PotatoService()
PotatoService.login(users.info[user_name], config.LOGIN_URL)
uuid_list = PotatoService.get_latest_post_uuid_list(config.LATEST_POST_URL, 15)
PotatoService.comment_post(uuid_list, True)
