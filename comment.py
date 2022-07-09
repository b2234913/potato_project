from utils.potato_service import PotatoService
from config import config, users
# os.system("pkill -9 Google Chrome")

PotatoService = PotatoService()
PotatoService.login(users.info['ShooterIsMe'], config.login_url)
uuid_list = PotatoService.get_latest_post_uuid_list(config.latest_post_url, 30)
PotatoService.comment_post(uuid_list, True)
