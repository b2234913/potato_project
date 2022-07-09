import re
import time
import logging
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class PotatoService():
    def __init__(self):
        options = Options()
        options.add_extension("/Users/victor_wu/Library/Application Support/Google/Chrome/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.43.0_0.crx")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        # self.driver.minimize_window()
        self.driver.get('chrome://settings/')
        self.driver.execute_script("chrome.settingsPrivate.setDefaultZoom(0.5);")

    def redirect_retry(self, url):
        for i in range(10):
            try:
                self.driver.get(url)
                logging.info("Go to %s.", self.driver.current_url)
            except Exception as e :
                logging.error("try %s and get something error", i)
                logging.error(e)
                continue
            break

    def login(self, user_info, login_url):
        for i in range(10):
            try:
                self.redirect_retry(login_url)
                logging.info("Go to %s.", self.driver.current_url)
                self.driver.find_element(By.XPATH, "//select[@class='forms-addon-text-select__Select--r6FsZ parts-shared__PhoneCountryAddon--oV3ov']//option[@value='" + user_info["code"] + "']").click()
                self.driver.find_element(By.CLASS_NAME, "forms-form__FormInputInput--4ZfCG").send_keys(user_info["id"])
                self.driver.find_element(By.CLASS_NAME, "elements-text-button__TextButton--theme-filled--kI1ER").click()
                logging.info("Login ID.")
            except Exception as e:
                logging.error(e)
                continue
            break
        time.sleep(1)
        for i in range(10):
            try:
                self.driver.find_element(By.CLASS_NAME, "forms-form__FormInputInput--4ZfCG").send_keys(user_info["pw"])
                self.driver.find_element(By.CLASS_NAME, "elements-text-button__TextButton--theme-filled--kI1ER").click()
                logging.info("Login PW.")
            except Exception as e:
                logging.error(e)
                continue
            break
        time.sleep(2)

    def create_new_draft(self, user_post_page_url):
        for i in range(3):
            try:
                if self.driver.current_url != user_post_page_url:
                    self.redirect_retry(user_post_page_url)
                    time.sleep(2)
                self.driver.find_elements(By.XPATH, "//button[@class='elements-icon-button__Button--13DmG elements-icon-button__Button--shape-3--q3Gpt icon-nav-icon-nav__IconNavItemIconButton--GTzud']")[1].click()

                self.driver.find_element(By.XPATH, "//a[text()='文章']").click()
                pop_up_window = self.driver.find_element(By.XPATH, "//div[@class='mixed-legal-terms-prompt-lightbox__ScrollableMiniCard--sz3e2']")
                for i in range(10):
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up_window)
                    time.sleep(1)
                self.driver.find_element(By.XPATH, "//span[text()='我同意']").click()
                time.sleep(1)
                logging.info("Clicking new draft.")
            except Exception as e:
                logging.error(e)
                continue
            break

    def write_draft(self, draft_info):
        for i in range(3):
            try:
                self.driver.find_element(By.XPATH, "//div[@data-placeholder='文章標題... (必填)']").send_keys(draft_info["title"])
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//p[@data-placeholder='空白段落...']").send_keys(draft_info["contents"])
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//span[text()='下一步']").click()
                self.driver.find_element(By.XPATH, "//select[@class='forms-form__FormInputSelect--60nFw']//option[text()='✦議題討論']").click()
                self.driver.find_element(By.XPATH, "//textarea[@placeholder='文章簡介... (必填，最多 128 字)']").send_keys("廢文")
                self.driver.find_elements(By.XPATH, "//span[@class='elements-text__Text--GtFnm elements-text__Style--typo-7--U36q4 elements-text-button__Text--VBmaO']")[2].click()
                self.driver.find_element(By.XPATH, "//span[text()='上傳草稿']").click()
                time.sleep(5)
                self.driver.find_element(By.XPATH, "//span[text()='確認']").click()
                logging.info("Done draft")
            except Exception as e:
                logging.error(e)
                continue
            break

    def get_latest_post_uuid_list(self, latest_post_url, scroll_times):
        self.redirect_retry(latest_post_url)
        post_uuid_list = []
        for i in range(scroll_times):
            try:
                post_list = self.driver.find_elements(By.CLASS_NAME, "elements-icon-button__Button--shape-3--q3Gpt")
                reg = "https://www.potatomedia.co/post/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
                for post in post_list:
                    url = str(post.get_attribute("href"))
                    re_result = re.match(reg, url)
                    if re_result:
                        post_uuid_list.append(re_result.group(1))

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                self.driver.execute_script("return document.body.scrollHeight")
                time.sleep(2)
            except Exception as e:
                logging.error(e)
                continue
        return_post_uuid_list =  list(set(post_uuid_list))
        logging.info("UUID list: %s", return_post_uuid_list)
        return return_post_uuid_list

    def like_post(self, post_uuid_list, and_delete):
        for post_uuid in post_uuid_list:
            for i in range(10):
                try:
                    self.redirect_retry(f"https://www.potatomedia.co/post/{post_uuid}")
                    time.sleep(2)
                    action_bar = self.driver.find_element(By.CLASS_NAME, "article-action-bar-below__ActionList--ocd7B")
                    self.driver.execute_script(f"window.scrollTo(0, {action_bar.location['x']})")
                    action = action_bar.find_elements(By.CLASS_NAME, "elements-icon-button__Button--shape-3--q3Gpt")
                    action[0].click()
                    logging.info("Liked post.")
                    if and_delete:
                        action[3].click()
                        self.driver.find_element(By.XPATH, "//span[text()='刪除貼文']").click()
                        time.sleep(1)
                        self.driver.switch_to.alert.accept()
                        time.sleep(1)
                        self.driver.switch_to.alert.accept()
                        logging.info("Deleted post")
                except Exception as e:
                    logging.error(e)
                    continue
                break

    def comment_post(self, post_uuid_list, and_delete):
        for post_uuid in post_uuid_list:
            for i in range(10):
                try:
                    self.redirect_retry(f"https://www.potatomedia.co/post/{post_uuid}")
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, "//textarea[@placeholder='留言...']").send_keys(":)")
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, "//span[text()='留言']").click()
                    time.sleep(2)
                    logging.info("Added new comment.")
                except Exception as e:
                    logging.error(e)
                    continue
                break
            if and_delete:
                for i in range(10):
                    try:
                        self.driver.find_element(By.XPATH, "//div[@class='comment-block-comment-block__CommentItemActionButtonContainer--3T4Gl']").click()
                        time.sleep(1)
                        self.driver.find_element(By.XPATH, "//div[@class='cards-card__CardItemContainer--2oLHT']").click()
                        time.sleep(2)
                        logging.info("Deleted comment.")
                    except Exception as e:
                        logging.error(e)
                        logging.error("Delete error: {post_uuid}")
                        continue
                    break
