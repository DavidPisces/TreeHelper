# Tree Helper

# GPL V3

import random
import os,time
import GetInstance

from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from urllib import request
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

#from main import checkWindow, changeVideoQuality, fasterPlay, getCurrentTime, getTotalTime, nextVideo

url = "https://studyvideoh5.zhihuishu.com/stuStudy?recruitAndCourseId=4b5c5d5d445e4859454a58595f47594351"
browser = webdriver.Chrome()

# user config
username = "15314422050"
userpass = "Wd20030219"

# elements in browser
username_element = "/html/body/div[4]/div/form/div[1]/ul[1]/li[1]/input[4]"
password_element = "/html/body/div[4]/div/form/div[1]/ul[1]/li[2]/input"
loginbutton_element = "/html/body/div[4]/div/form/div[1]/span"


def logd(logn):
    print("[fuckzhihuishu.logd] " + logn)


def login(usernum, userpasswd, url):
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
    while True:
        try:
            image_back = browser.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute("src")
            image_in = browser.find_element(By.CLASS_NAME, "yidun_jigsaw").get_attribute("src")
            request.urlretrieve(image_back, "back.png")
            request.urlretrieve(image_in, "in.png")
            break
        except Exception:
            logd("auth failed")
    # get instance
    get_instance = GetInstance.identify_gap("back.png", "in.png", "out.png")
    print("[TreeHelper.logd] instance:", get_instance)
    # auth
    # 考虑到图片有透明边缘，设定偏移值为12
    slider = browser.find_element(By.CLASS_NAME, "yidun_slider")  # 实例化滑块
    # random int number
    randomnumber = random.randint(9, 14)
    ActionChains(browser) \
        .move_to_element(slider) \
        .click_and_hold() \
        .move_by_offset(get_instance + randomnumber, 0) \
        .release() \
        .perform()

"""
def enter_class(classarray):
    sleep(2)
    class_xpath = "/html/body/div[1]/section/div[2]/section[2]/section/div/div/div/div[2]/div[1]/div[2]/ul[" \
                  + classarray
    class_xpath = class_xpath + "]/div/dl/dt/div[1]/div[1]"
    try:
        browser.find_element(By.XPATH, class_xpath).click()
    except Exception:
        logd("enter_class failed")
    return 0

"""


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


def getUnitName():
    try:
        name = browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[1]/div[1]')
        return name.text
    except:
        return '暂未加载'


def checkWindow():
    print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在播放:' + getUnitName())
    close_warning()
    response()
    print('\n\n')


def changeVideoQuality():
    try:
        openControlsBar()
        videoQuality = browser.find_element(By.XPATH, ' //div[@class="definiBox"]/div/b[1]')
        definiBox = browser.find_element(By.XPATH, ' //div[@class="definiBox"]')
        time.sleep(5)
        openControlsBar()
        ActionChains(browser).move_to_element(definiBox).perform()
        videoQuality.click()
        print('成功切换到流畅画质\t√')
        checkWindow()
    except:
        print('切换到流畅画质失败，稍后将重试\t\t✘')



def openControlsBar():
    checkWindow()
    controlsBar = browser.find_element(By.XPATH,' //div[@id="container"]')
    ActionChains(browser).move_to_element(controlsBar).perform()

def response():
    try:
        # 检查是否有弹窗检验
        browser.find_element(By.XPATH, '//div[@id="app"]/div[1]/div[7]/div[@class="el-dialog"]')
        option = browser.find_elements(By.XPATH, '//ul[@class="topic-list"]/li')
        for i in range(len(option)):
            option[i].click()

        # 获取正确答案
        answer = browser.find_element(By.XPATH, "//p[@class='answer']/span").text.split(',')
        print('正确答案是：' + str(answer))

        # 点击正确答案

        for i in range(len(option)):
            print('选项' + str(i) + ':' + option[i].text)
            flag = False
            for j in range(len(answer)):
                if option[i].text.find(answer[j]) != -1:
                    flag = True
                    break
            if (flag == False):
                option[i].click()
        # 点击关闭
        close = browser.find_element(By.XPATH, '//div[@class="btn"]')
        close.click()
        print("答题成功！\t\t\t√")
        play()
        return True
    except:
        print("未找到弹窗测验\t\t✘")
        return False


def play():
    start_status = browser.find_element(By.XPATH, '//div[@id="playButton"]').get_attribute('class')
    start_button = browser.find_element(By.XPATH, '//div[@id="playButton"]')
    time.sleep(10)
    if start_status.find('playButton') != -1:
        print('当前静止')
        openControlsBar()
        time.sleep(1)
        start_button.click()
        print('点击播放成功\t\t√')


# 点击静音
def noVoice():
    try:
        voice_status = browser.find_element(By.XPATH, '//div[@id="vjs_container"]/div[10]/div[6]').get_attribute(
            'class')
        voice_buttton = browser.find_element(By.XPATH, '//div[@id="vjs_container"]/div[10]/div[6]/div[1]')
        print(voice_status)
        if voice_status.find('volumeNone') == -1:
            print('此时非静音')
            time.sleep(5)
            openControlsBar()
            voice_buttton.click()
            print('静音成功\t\t\t√')
    except:
        print('静音失败，稍后将重试\t\t✘')


def fasterPlay():
    try:
        openControlsBar()
        speed = browser.find_element(By.XPATH, ' //div[@class="speedBox"]/div/div[1]')
        speedbox = browser.find_element(By.XPATH, '//div[@class="speedBox"]')
        time.sleep(5)
        openControlsBar()
        ActionChains(browser).move_to_element(speedbox).perform()
        speed.click()
        print('成功切换成' + speed.text + '倍速\t√')
    except:
        print('切换成' + speed.text + '倍速失败，稍后将重试\t✘')


def getCurrentTime():
    openControlsBar()
    time = browser.find_element(By.XPATH, '//div[@class="nPlayTime"]/span[1]').text
    print('当前播放时间为：' + time)
    return time


def getTotalTime():
    openControlsBar()
    time = browser.find_element(By.XPATH, '//div[@class="nPlayTime"]/span[2]').text
    print('本集视频时间为：' + time)
    return time


def nextVideo():
    openControlsBar()
    nextBtn = browser.find_element(By.XPATH, '//div[@id="nextBtn"]')
    nextBtn.click()
    print('\n切换下一个视频\n')


if __name__ == '__main__':
    login(username, userpass ,url)
    close_warning()
    playvideo()
    while (True):
        # 有时进入视频会直接弹出窗口，且窗口显示顺序不定，故检测三次，保证再开始播放之前关闭
        print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n' + '正在在执行视频播放前检查')
        for i in range(3):
            print('\n第' + str(i) + '检测')
            checkWindow()
            time.sleep(2)

        print(time.strftime('%Y-%m-%d  %H:%M:%S') + '\n检查完毕\n\n\n开始优化播放\n')
        # 避免在前三次中未检测出窗口，开始操作前全部检查一次
        checkWindow()
        play()
        print('正在修改画质')
        time.sleep(2)
        checkWindow()
        changeVideoQuality()
        print('画质修改成功\t\t\t√')
        print('正在修该播放速度')
        checkWindow()
        fasterPlay()
        print('播放速度修改成功\t\t\t√')
        print('正在修改静音')
        checkWindow()
        noVoice()
        print('静音修改成功\t\t√\n\n')

        # 每隔5秒检测是否有我知道了，学前必读，是否播放完
        while (True):
            print(time.strftime('%Y-%m-%d  %H:%M:%S'))
            # 播放完毕，下一集
            if getCurrentTime() == getTotalTime():
                print('\n\n')
                checkWindow()
                nextVideo()
                break

            print('\n\n')
            checkWindow()
            print('\n\n')
            time.sleep(5)
