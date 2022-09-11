# Tree Helper

# GPL V3

import random
import os
import GetInstance

from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib import request
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


url = "https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin"
browser = webdriver.Chrome()

# user config
username = ""
userpass = ""

# elements in browser
username_element = "/html/body/div[4]/div/form/div[1]/ul[1]/li[1]/input[4]"
password_element = "/html/body/div[4]/div/form/div[1]/ul[1]/li[2]/input"
loginbutton_element = "/html/body/div[4]/div/form/div[1]/span"


def logd(logn):
    print("[fuckzhihuishu.logd] " + logn)


def login(usernum, userpasswd):
    # start
    browser.get(url)
    browser.fullscreen_window()
    logd("Open Chrome Successfully")
    print(browser.window_handles)
    # set implicitly wait for the elements be found.
    browser.implicitly_wait(10)
    print("[fuckzhihuishu.login] User:", usernum, "loginng")
    # simulate input username and password
    browser.find_element(By.XPATH, username_element).send_keys(usernum)
    logd("Input username")
    browser.find_element(By.XPATH, password_element).send_keys(userpasswd)
    logd("input password")
    browser.find_element(By.XPATH, loginbutton_element).click()

    # waitting for imagination loading
    logd("waiting for image authentication")
    sleep(4)
    # get authentication imagination
    image_back = browser.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute("src")
    image_in = browser.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute("src")
    request.urlretrieve(image_back, "back.png")
    request.urlretrieve(image_in, "in.png")
    # get instance
    get_instance = GetInstance.identify_gap("back.png", "in.png", "out.png")
    print("[fuckzhihuishu.logd] instance:", get_instance)
    # auth
    # 考虑到图片有透明边缘，设定偏移值为12
    slider = browser.find_element(By.CLASS_NAME, "yidun_slider")  # 实例化滑块
    # random int number
    randomnumber = random.randint(9, 12)
    ActionChains(browser) \
        .move_to_element(slider) \
        .click_and_hold() \
        .move_by_offset(get_instance + randomnumber, 0) \
        .release() \
        .perform()


def enter_class(classarray):
    sleep(2)
    class_xpath = "/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul[" \
                  + classarray
    class_xpath = class_xpath + "]/div/dl/dt/div[1]/div[1]"
    browser.find_element(By.XPATH, class_xpath).click()
    return 0


def close_warning():
    try:
        button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[6]/div/div[3]/span/button")
        button.click()
        logd("Warning Close successfully")
        button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[7]/div[2]/div[1]/i")
        button.click()
        logd("学前必读 close successfully")
    except Exception:
        logd("Close failed,check browser")


def playvideo():
    browser.fullscreen_window()
    while True:
        try:
            browser.switch_to.window(browser.window_handles[-1])
            video=browser.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[8]")
            ActionChains(browser).move_to_element(video)
            playbutton = browser.find_element(By.XPATH,
                                              "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div/div[10]/div[2]")
            # point stay on video
            ActionChains(browser)\
                .move_to_element(playbutton)\
                .pause(1).click(playbutton).perform()
            logd("playing....")
            break
        except Exception:
            logd("play failed")
    return 0


if __name__ == '__main__':
    login(username, userpass)
    enter_class("1")
    close_warning()
    playvideo()
