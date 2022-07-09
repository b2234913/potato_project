import os
import time
from utils.potato_service import PotatoService
from config import config, users


# os.system("pkill -9 Google Chrome")


user_post_page_url = f"{config.potato_host}/user/{users.info['ShooterIsMe']['uuid']}/posts"

PotatoService = PotatoService()
PotatoService.login(users.info["ShooterIsMe"], config.login_url)
PotatoService.redirect_retry(user_post_page_url)

while True:
    for i in range(5):
        try:
            PotatoService.create_new_draft(user_post_page_url)
            title = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            config.draft_info["title"] = title
            PotatoService.write_draft(config.draft_info)
        except Exception as e:
            print(e)

    draft_uuid_list = PotatoService.get_latest_post_uuid_list(user_post_page_url, 3)
    draft_uuid_list = list(set(draft_uuid_list) - set(config.ex_uuid))
    print(draft_uuid_list)
    if draft_uuid_list:
        PotatoService.like_post(draft_uuid_list, True)

