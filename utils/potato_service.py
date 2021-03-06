import re
import time
import logging
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class PotatoService():
    def __init__(self):
        options = Options()
        options.add_extension("./extension/1.43.0_0.crx")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        self.driver.get('chrome://settings/')
        self.driver.execute_script("chrome.settingsPrivate.setDefaultZoom(0.5);")

    def redirect_retry(self, url: str) -> None:
        for try_time in range(10):
            try:
                logging.info("Try %s: Redirect.", try_time)
                self.driver.get(url)
                logging.info("Go to %s.", self.driver.current_url)
            except Exception as exc :
                logging.error(exc)
                continue
            break

    def login(self, user_info, login_url):
        for try_time in range(10):
            try:
                logging.info("Try %s: Account login.", try_time)
                self.redirect_retry(login_url)
                logging.info("Go to %s.", self.driver.current_url)
                #pylint: disable = line-too-long
                x_path = "//select[@class='forms-addon-text-select__Select--r6FsZ parts-shared__PhoneCountryAddon--oV3ov']//option[@value='"+ user_info["code"] +"']"
                self.driver.find_element(By.XPATH, x_path).click()
                self.driver.find_element(By.CLASS_NAME, "forms-form__FormInputInput--4ZfCG").send_keys(user_info["id"])
                self.driver.find_element(By.CLASS_NAME, "elements-text-button__TextButton--theme-filled--kI1ER").click()
                logging.info("Logined ID.")
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, "forms-form__FormInputInput--4ZfCG").send_keys(user_info["pw"])
                self.driver.find_element(By.CLASS_NAME, "elements-text-button__TextButton--theme-filled--kI1ER").click()
                logging.info("Logined PW.")
                time.sleep(5)
                self.check_score()
            except Exception as exc:
                logging.error(exc)
                continue
            break

    def check_score(self):
        score_block = self.driver.find_element(By.XPATH, "//a[@href='/i/score']").find_elements(By.XPATH, "//h4")
        level = score_block[1].text
        today_score = score_block[2].text
        total_score = score_block[3].text
        logging.info("Level is %s.", level)
        logging.info("Today score is %s.", today_score)
        logging.info("Total score is %s.", total_score)

    def create_new_draft(self, user_post_page_url: str) -> None:
        for try_time in range(3):
            try:
                logging.info("Try %s: Start to create_new_draft.", try_time)
                if self.driver.current_url != user_post_page_url:
                    self.redirect_retry(user_post_page_url)
                    time.sleep(2)
                #pylint: disable = line-too-long
                x_path = "//button[@class='elements-icon-button__Button--13DmG elements-icon-button__Button--shape-3--q3Gpt icon-nav-icon-nav__IconNavItemIconButton--GTzud']"
                self.driver.find_elements(By.XPATH, x_path)[1].click()
                self.driver.find_element(By.XPATH, "//a[text()='??????']").click()
                pop_up_window = self.driver.find_element(By.XPATH, "//div[@class='mixed-legal-terms-prompt-lightbox__ScrollableMiniCard--sz3e2']")
                for scole_time in range(10):
                    logging.debug("Scole down time %s", scole_time)
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up_window)
                    time.sleep(0.2)
                self.driver.find_element(By.XPATH, "//span[text()='?????????']").click()
                time.sleep(1)
                logging.info("Clicking new draft.")
            except Exception as exc:
                logging.error(exc)
                continue
            break

    def write_draft(self, draft_info: dict) -> None:
        for try_time in range(3):
            try:
                logging.info("Try %s: Write draft.", try_time)
                self.driver.find_element(By.XPATH, "//div[@data-placeholder='????????????... (??????)']").send_keys(draft_info["title"])
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//p[@data-placeholder='????????????...']").send_keys(draft_info["contents"])
                time.sleep(1)
                self.driver.find_element(By.XPATH, "//span[text()='?????????']").click()
                self.driver.find_element(By.XPATH, "//select[@class='forms-form__FormInputSelect--60nFw']//option[text()='???????????????']").click()
                self.driver.find_element(By.XPATH, "//textarea[@placeholder='????????????... (??????????????? 128 ???)']").send_keys("??????")
                x_path = "//span[@class='elements-text__Text--GtFnm elements-text__Style--typo-7--U36q4 elements-text-button__Text--VBmaO']"
                self.driver.find_elements(By.XPATH, x_path)[2].click()
                self.driver.find_element(By.XPATH, "//span[text()='????????????']").click()
                time.sleep(5)
                self.driver.find_element(By.XPATH, "//span[text()='??????']").click()
                logging.info("Done draft")
            except Exception as exc:
                logging.error(exc)
                continue
            break

    def get_latest_post_uuid_list(self, latest_post_url: str, scroll_times: int) -> list:
        self.redirect_retry(latest_post_url)
        post_uuid_list = []
        for try_time in range(scroll_times):
            try:
                logging.info("Try %s: Get latest post UUID list.", try_time)
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
            except Exception as exc:
                logging.error(exc)
                continue
        return_post_uuid_list =  list(set(post_uuid_list))
        logging.info("UUID list: %s", return_post_uuid_list)
        return return_post_uuid_list

    def like_post(self, post_uuid_list: list, and_delete: bool) -> None:
        for ind, post_uuid in enumerate(post_uuid_list):
            for i in range(10):
                try:
                    self.redirect_retry(f"https://www.potatomedia.co/post/{post_uuid}")
                    time.sleep(2)
                    action_bar = self.driver.find_element(By.CLASS_NAME, "article-action-bar-below__ActionList--ocd7B")
                    self.driver.execute_script(f"window.scrollTo(0, {action_bar.location['x']})")
                    action = action_bar.find_elements(By.CLASS_NAME, "elements-icon-button__Button--shape-3--q3Gpt")
                    action[0].click()
                    logging.info("Liked %s post.", ind)
                    if and_delete:
                        action[3].click()
                        self.driver.find_element(By.XPATH, "//span[text()='????????????']").click()
                        time.sleep(1)
                        self.driver.switch_to.alert.accept()
                        time.sleep(1)
                        self.driver.switch_to.alert.accept()
                        logging.info("Deleted post")
                except Exception as exc:
                    logging.error(exc)
                    continue
                break

    def comment_post(self, post_uuid_list: list, and_delete: bool) -> None:
        for ind, post_uuid in enumerate(post_uuid_list):
            for i in range(10):
                try:
                    self.redirect_retry(f"https://www.potatomedia.co/post/{post_uuid}")
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, "//textarea[@placeholder='??????...']").send_keys(":)")
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, "//span[text()='??????']").click()
                    time.sleep(2)
                    logging.info("Added %s comment.", ind)
                except Exception as exc:
                    logging.error(exc)
                    continue
                break
            if and_delete:
                for try_time in range(10):
                    try:
                        logging.info("Try %s: Delete Comment.", try_time)
                        x_path = "//div[@class='comment-block-comment-block__CommentItemActionButtonContainer--3T4Gl']"
                        self.driver.find_element(By.XPATH, x_path).click()
                        time.sleep(1)
                        self.driver.find_element(By.XPATH, "//div[@class='cards-card__CardItemContainer--2oLHT']").click()
                        time.sleep(2)
                        logging.info("Deleted comment.")
                    except Exception as exc:
                        logging.error(exc)
                        logging.error("Delete error: {post_uuid}")
                        continue
                    break
