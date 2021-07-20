from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import Constant
import AIRobot
import time

# Phone
desired_caps = {'platformName': 'Android',
                'platformVersion': '9.0',
                'deviceName': 'xxxxxxxxx',
                'appPackage': 'com.xxx.xxx',
                'appActivity': 'com.xxx.xxx.WelcomeActivity',
                'noReset': True,
                'newCommandTimeout': 10000}


class Message:

    #  初始化
    def __init__(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    # 进入消息列表
    def entryMessage(self):
        if WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id(Constant.MESSAGE_PAGE)):
            # 按钮显示了 执行点击事件
            self.driver.find_element_by_id(Constant.MESSAGE_PAGE).click()
            # Chat列表
            if WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id(Constant.CHAT_LIST)):
                # 轮询消息列表 接收新消息
                self.pollingMessage()
            else:
                print("消息列表显示失败！")
        else:
            print("打开消息列表页面失败！")

    # 轮询消息列表 接收新消息
    def pollingMessage(self):
        items = self.driver.find_elements_by_id(Constant.MESSAGE_NEW)
        # 元素组长度 如果为0则没有新消息
        if len(items) > 0:
            print("新消息来啦~~~")
            # 执行点击事件进入消息页面
            items[0].click()
            # 打开消息页面
            self.openMessage()
        else:
            print("没有新消息哦~")
            # 延迟
            time.sleep(1.5)
            # 轮询方法
            self.pollingMessage()

    # 打开消息页面
    def openMessage(self):
        if WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id(Constant.MESSAGE_LIST)):
            if self.news():
                print("对方的消息,交给机器人回复！")
                # 发送消息
                self.sendMessage()
            else:
                print("我的消息,则不处理！")
                # 返回消息列表页面
                self.backListActivity()
        else:
            print("打开消息页面失败！")
            # 返回消息列表页面
            self.backListActivity()

    # 发送消息
    def sendMessage(self):
        # 获取内容元素组
        contents = self.driver.find_elements_by_id(Constant.CHAT_CONTENT)
        # 获取内容
        content = contents[len(contents) - 1].text
        # 将内容提交给机器人
        result = AIRobot.requestRobot(content)
        # 机器人的回答赋值输入框
        self.driver.find_element_by_id(Constant.CHAT_INPUT).send_keys(result)
        # 发送
        if WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id(Constant.CHAT_SEND)):
            # 点击发送按钮
            self.driver.find_element_by_id(Constant.CHAT_SEND).click()
            # 计时等待新消息
            self.waitNewMessage()

    # 计时等待新消息
    def waitNewMessage(self):
        # 捕获没有找到按钮的异常
        countDown = Constant.CHAR_WAIT_TIME
        try:
            while True:
                if self.news():
                    print("新的对话消息来啦~~")
                    # 发送消息
                    self.sendMessage()
                    break
                elif countDown >= 0:
                    print("计时等待新消息 " + str(countDown))
                    # 自减计时
                    countDown = countDown - 1
                    # Sleep
                    time.sleep(1)
                else:
                    print("计时结束，返回列表页面~ ")
                    # 返回消息列表页面
                    self.backListActivity()
                    break

        except WebDriverException:
            print("消息等待异常 退出页面~~~ ")
            # 返回消息列表页面
            self.backListActivity()

    # 获取新消息
    def news(self):
        try:
            if WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id(Constant.CHAT_AVATARS)):
                # 获取头像元素组
                avatars = self.driver.find_elements_by_id(Constant.CHAT_AVATARS)
                # 内容验证
                if len(avatars) > 0:
                    # 最后一个头像的x坐标
                    avatarX = avatars[len(avatars) - 1].location['x']
                    # 获取屏幕宽度 ( 二分之一 )
                    screenX = (self.driver.get_window_size()['width'] / 2)
                    # 判断头像位置 True左 False右
                    return avatarX <= screenX
                else:
                    print("你们之间没有对话！")
                    return False
            else:
                return False
        except WebDriverException:
            print("头像元素异常 退出页面~~~ ")
            # 返回消息列表页面
            self.backListActivity()

    # 验证是否还在消息页面停留
    def isChatActivity(self):
        return self.driver.current_activity == Constant.CHAT_ACTIVITY

    # 返回消息列表页面
    def backListActivity(self):
        if self.isChatActivity():
            # 返回列表页面
            self.driver.back()
        # 轮询列表的消息
        self.pollingMessage()


# Run
if __name__ == '__main__':
    Message().entryMessage()
