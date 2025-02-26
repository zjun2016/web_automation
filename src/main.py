import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from src.config import HOME_URL, LOGIN_URL, SSOUSERNAME, SSSOPASSWORD, USERNAME, PASSWORD
from src.captcha_solver.captcha_solver import extract_base64_data, reconizeOCR

def main():
    # 配置Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 无头模式
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化控制提示
    service = Service("/usr/local/bin/chromedriver")  # 替换为你的chromedriver路径
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # 直接打开首页
        driver.get(HOME_URL)
        time.sleep(2)  # 等待页面加载

        # 获取当前页面的 URL
        current_url = driver.current_url
        print(f"当前页面URL: {current_url}")

        # 判断是否跳转到 SSO 登录页面
        if "authcenter/ActionAuthChain" in current_url:
            print("当前处于SSO登录页面，执行SSO登录操作。")
            
            # 输入SSO登录的用户名和密码
            username_input = driver.find_element(By.ID, "j_username")
            username_input.send_keys(SSOUSERNAME)
            password_input = driver.find_element(By.ID, "j_password")
            password_input.send_keys(SSSOPASSWORD)

            # 点击SSO登录按钮
            login_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(@class, 'loginBt')]")
            login_button.click()
            time.sleep(2)  # 等待登录完成

            # 获取新页面的 URL
            new_url = driver.current_url
            print(f"新的页面URL: {new_url}")

            if "/index" in new_url:
                print("SSO登录成功，页面URL已跳转至主页。")
            else:
                print("SSO登录失败，请检查用户名、密码是否正确。")
        
        # 判断是否跳转到项目的登录页面
        elif "/login" in current_url:
            print("当前处于项目登录页面，执行项目登录操作。")

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
            print('USERNAME', USERNAME, 'PASSWORD', PASSWORD, 'captcha_answer----', captcha_answer)

            # 点击登录按钮
            login_button = driver.find_element(By.XPATH, "//button/span[text()='登录']/..")
            login_button.click()
            time.sleep(2)  # 等待登录完成

            # 获取新页面的 URL
            new_url = driver.current_url
            print(f"新的页面URL: {new_url}")

            # 判断是否登录成功
            if new_url != current_url and "/index" in new_url:
                print("登录成功！页面URL已跳转至主页。")
            else:
                print("登录失败，请检查账号、密码或验证码解析是否正确。")
        
        else:
            print("当前页面已登录，无需重新登录。")
            time.sleep(4)  # 等待主页加载完成

    finally:
        driver.quit()
        if os.path.exists("captcha.png"):
            os.remove("captcha.png")

if __name__ == "__main__":
    main()
