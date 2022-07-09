import os
import time
import argparse
from utils.potato_service import PotatoService
from config import config, users

if __name__ == "__main__":
    # os.system("pkill -9 Google Chrome")

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="please input the user name in users.py", required=True)
    args = parser.parse_args()

    user_name = args.user
    user_post_page_url = f"{config.POTATO_HOST}/user/{users.info[user_name]['uuid']}/posts"

    PotatoService = PotatoService()
    PotatoService.login(users.info[user_name], config.LOGIN_URL)
    PotatoService.redirect_retry(user_post_page_url)

    while True:
        for i in range(5):
            try:
                PotatoService.create_new_draft(user_post_page_url)
                config.DRAFT_INFO["title"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                PotatoService.write_draft(config.DRAFT_INFO)
            except Exception as e:
                print(e)
        draft_uuid_list = PotatoService.get_latest_post_uuid_list(user_post_page_url, 3)
        draft_uuid_list = list(set(draft_uuid_list) - set(config.EX_UUID))
        print(draft_uuid_list)
        if draft_uuid_list:
            PotatoService.like_post(draft_uuid_list, True)
