
import os, telegram
from dotenv import load_dotenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']
TG_GROUP = int(os.environ['TG_GROUP']) or None

class Bot():
  def __init__(self):
    try:
      self.driver = webdriver.Chrome(options=self.set_chrome_options())
    except:
      print("Chrome not found...")
    self.vars = {}
  
  def set_chrome_options(self) -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options
  
  def quit(self):
    self.driver.quit()
    sleep(3)
  
  def get_dates(self) -> list[str]:
    self.driver.get("https://hannover.premiumkino.de/film/avatar-the-way-of-water")
    self.driver.set_window_size(1206, 664)
    sleep(1)
    cookie_btn = self.driver.find_element(By.XPATH, "/html/body/modal/div/div[2]/div/div/div/div/div/div[4]/div/button[1]")
    ActionChains(self.driver).move_to_element(cookie_btn).perform()
    sleep(0.5)
    cookie_btn.click()
    sleep(0.5)
    self.driver.find_element(By.CSS_SELECTOR, ".none").click()
    sleep(0.5)
    i = 1
    dates:list[str] = []
    while True:
        try:
            dates.append(str(
              self.driver.find_element(
                By.XPATH, 
                f"/html/body/modal/div/div[2]/div/div/div[2]/div/div/div[2]/div[{i}]/h5"
              ).text
            ))
        except NoSuchElementException:
            break
        i += 1
    return dates


if __name__ == "__main__":
  last_date:str = ""
  tg = telegram.Bot(TG_TOKEN)

  tg.send_message(text='Bot läuft', chat_id=TG_GROUP)

  while True:
    bot = Bot()
    termine:list[str] = bot.get_dates()
    date = termine[-1]
    print(date)
    bot.quit()
    if last_date != date:
        tg.send_message(text="Neue Termine für Avatar 2:\n"+'\n'.join(termine), chat_id=TG_GROUP)
        last_date = date
    sleep(45*60)