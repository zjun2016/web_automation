# main.py
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from src.config import LOGIN_URL, USERNAME, PASSWORD
from src.captcha_solver.captcha_solver import extract_base64_data, reconizeOCR


def main():
    # 配置Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无头模式
    service = Service("/usr/local/bin/chromedriver")  # 替换为你的chromedriver路径
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 打开登录页面
        driver.get(LOGIN_URL)
        original_url = driver.current_url
        time.sleep(2)  # 等待页面加载

        # 获取页面源码
        page_source = driver.page_source

        # 提取 Base64 数据
        base64_data = extract_base64_data(page_source)
        captcha_answer = reconizeOCR(base64_data)

        # 输入账号、密码和验证码
        username_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='用户名']")
        username_input.send_keys(USERNAME)
        password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='密码']")
        password_input.send_keys(PASSWORD)
        captcha_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='请输入计算结果']")
        captcha_input.send_keys(captcha_answer)
        print('USERNAME', USERNAME,'PASSWORD',PASSWORD,'captcha_answer----', captcha_answer)

        # 点击登录按钮
        # 使用XPath定位器通过按钮内的文本定位登录按钮并点击
        login_button = driver.find_element(By.XPATH, "//button/span[text()='登录']/..")
        login_button.click()
        time.sleep(2)  # 等待登录完成

        new_url = driver.current_url
        print(f"新的页面URL: {new_url}")

        # 判断是否登录成功
        if new_url != original_url and "/index" in new_url:
            print("登录成功！页面URL已跳转至主页。")
        else:
            print("登录失败，请检查账号、密码或验证码解析是否正确。")

    finally:
        driver.quit()
        if os.path.exists("captcha.png"):
            os.remove("captcha.png")

if __name__ == "__main__":
    main()

