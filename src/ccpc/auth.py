import os
import pickle
from selenium import webdriver
import time
from src.config import CPC_HOME_URL

class WebAuthenticator:
    def __init__(self, driver: webdriver.Chrome, cookies_file="cookies.pkl", local_storage_file="local_storage.pkl"):
        self.driver = driver
        self.cookies_file = os.path.join('data', cookies_file)
        self.local_storage_file = os.path.join('data', local_storage_file)

    def save_cookies_and_local_storage(self):
        """保存当前浏览器的 Cookies 和 Local Storage 到文件"""
        # 获取 cookies
        cookies = self.driver.get_cookies()

        # 获取 localStorage 数据
        local_storage_data = self.driver.execute_script("""
            let storage = {};
            for (let i = 0; i < localStorage.length; i++) {
                let key = localStorage.key(i);
                let value = localStorage.getItem(key);
                storage[key] = value;
            }
            return storage;
        """)

        # 保存 cookies
        with open(self.cookies_file, "wb") as cookies_file:
            pickle.dump(cookies, cookies_file)

        # 保存 Local Storage 数据
        with open(self.local_storage_file, "wb") as local_storage_file:
            pickle.dump(local_storage_data, local_storage_file)

        print("Cookies 和 Local Storage 已保存到文件中。")

    def load_cookies_and_local_storage(self):
        """加载存储的 Cookies 和 Local Storage 数据"""    
        # 检查 cookies 文件是否为空
        if os.path.exists(self.cookies_file):
            if os.path.getsize(self.cookies_file) > 0:  # 确保文件有内容
                with open(self.cookies_file, "rb") as cookies_file:
                    cookies = pickle.load(cookies_file)
                    # print(f"加载到的 Cookies 数据: {cookies}")
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                print("Cookies 已加载。")
            else:
                print(f"Cookies 文件为空 ({self.cookies_file})，无法加载 Cookies。")
        else:
            print(f"未找到 Cookies 文件 ({self.cookies_file})，无法加载 Cookies。")

        # 检查 localStorage 文件是否为空
        if os.path.exists(self.local_storage_file):
            if os.path.getsize(self.local_storage_file) > 0:  # 确保文件有内容
                with open(self.local_storage_file, "rb") as local_storage_file:
                    local_storage_data = pickle.load(local_storage_file)
                    # print(f"加载到的 Local Storage 数据: {local_storage_data}")
                    for key, value in local_storage_data.items():
                        self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
                print("Local Storage 已加载。")
            else:
                print(f"Local Storage 文件为空 ({self.local_storage_file})，无法加载 Local Storage。")
        else:
            print(f"未找到 Local Storage 文件 ({self.local_storage_file})，无法加载 Local Storage。")


    def check_if_logged_in(self, login_url):
        """检查当前页面 URL 是否是登录页面"""
        current_url = self.driver.current_url
        if login_url in current_url:
            return False  # 需要登录
        return True  # 已经登录

    def handle_authentication(self, url, login_url):
        """处理认证：加载 Cookies 和 Local Storage，如果失效则重新登录"""
        self.driver.get(url)  # 访问目标网站
        print(f"访问网站: {url}")

        # 加载之前存储的 Cookies 和 Local Storage
        self.load_cookies_and_local_storage()

        # 刷新页面以应用 Cookies 和 Local Storage
        self.driver.refresh()

        time.sleep(2)
        if (self.driver.current_url != CPC_HOME_URL):
            self.driver.get(CPC_HOME_URL)

        # 等待页面加载
        time.sleep(2)

        # 检查是否需要重新登录
        if not self.check_if_logged_in(login_url):
            print("认证信息已失效，重新登录...")
            return False  # 需要重新登录

        print("认证信息有效，继续访问网站...", self.driver.current_url)
        return True  # 认证有效