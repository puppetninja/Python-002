#!/usr/bin/env python3
import time
import random

from selenium import webdriver

SHIMO_HOME_PAGE = "https://shimo.im"

USER_LOGIN_XPATH = '/html/body/div[1]/div[1]/header/nav/div[3]/a[2]/button'
USER_NAME_INPUT_XPATH = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div/input'
USER_PW_XPATH = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/div[2]/div/input'

SHIMO_MAIL = # 石墨邮箱或手机号
SHIMO_PW = # 石墨密码

LOGIN_BUTTON_XPATH = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button'


def random_stay(stay_min=5, stay_max=15):
    time.sleep(random.randrange(stay_min, stay_max))


def login_shimo():
    with webdriver.Chrome() as driver:
        driver.get(SHIMO_HOME_PAGE)
        random_stay()

        # Login into Shimo home page
        driver.find_element_by_xpath(USER_LOGIN_XPATH).click()

        # Input USER NAME & PW then click login button
        random_stay()
        driver.find_element_by_xpath(USER_NAME_INPUT_XPATH).send_keys(SHIMO_MAIL)

        random_stay()
        driver.find_element_by_xpath(USER_PW_XPATH).send_keys(SHIMO_PW)

        random_stay()
        driver.find_element_by_xpath(LOGIN_BUTTON_XPATH).click()

        # Check around shimo docs then close the browser
        random_stay(20, 30)


if __name__ == "__main__":
    login_shimo()
