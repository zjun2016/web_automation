import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.ccpc.auth import WebAuthenticator
from src.ccpc.home import search_info
from src.config import CPC_HOME_URL, CPC_LOGIN_URL
from .solva_captcha import solve_captcha_with_easyocr
from src.utils.utils import get_initialize_driver_with_profile, human_typing_with_backspace,human_click_random_delay

def ccpy_login(search_keyword: str):
    try:
        # 初始化浏览器
        driver = get_initialize_driver_with_profile()
        driver.get(CPC_HOME_URL)

        # 执行JavaScript代码，隐藏WebDriver检测
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        #  隐藏WebDriver检测
        driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: function() { return ['en-US', 'en']; }
            });
        """)

        # 创建认证处理对象
        print("创建认证处理对象")
        authenticator = WebAuthenticator(driver)
        print("创建认证处理对象----结束")
        # time.sleep()
        # 判断是否跳转到 SSO 登录页面
        if not authenticator.handle_authentication(CPC_HOME_URL, login_url=CPC_LOGIN_URL):
            print('当前处于项目登录页面，执行项目登录操作。')
            # 输入用户名
            username_input = driver.find_element(By.NAME, "username")
            username_input.clear()
            human_typing_with_backspace(driver, username_input, USERNAME)

            # 输入密码
            password_input = driver.find_element(By.NAME, "password")
            password_input.clear()
            human_typing_with_backspace(driver, password_input, PASSWORD)

            # 勾选同意协议的复选框
            label_element = driver.find_element(By.XPATH, "//div[contains(@class, 'agreeInfo')]//label")
            label_class = label_element.get_attribute('class') # 判断 label 元素的 class 是否包含 'is-checked'
            if 'is-checked' not in label_class:
                # 如果 label 中没有 is-checked，模拟点击 label 元素，选中协议复选框
                checkbox_element = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                human_click_random_delay(driver, checkbox_element)

            # 获取验证码并输入
            captcha_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='请输入右侧校验码']")

            retry_count = 0
            max_retries = 5  # 最大重试次数为5次

            while retry_count < max_retries:
                # 获取并识别验证码
                captcha_text = solve_captcha_with_easyocr(driver)
                print(f"识别的验证码是: {captcha_text}")

                # 判断验证码格式，确保是四位数字（根据实际情况修改验证规则）
                if captcha_text and captcha_text.isdigit() and len(captcha_text) == 4:
                    print(f"验证码格式正确：{captcha_text}")
                    break
                else:
                    retry_count += 1
                    print(f"验证码格式不正确，重新获取验证码... (第 {retry_count} 次重试)")

                    if retry_count >= max_retries:
                        print("重试次数超过最大限制，停止重新获取验证码。")
                        return  # 结束函数，停止登录流程

                    # 点击刷新验证码按钮
                    # captcha_image_element = driver.find_element(By.CSS_SELECTOR, "div.el-input-group__append img")
                    # captcha_image_element.click()

                    refresh_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.el-input-group__append img"))
                    )
                    # 尝试使用 JavaScript 进行点击（规避不可交互问题）
                    driver.execute_script("arguments[0].click();", refresh_button)

            # 输入验证码
            captcha_input.clear()
            human_typing_with_backspace(driver, captcha_input, captcha_text)

            # 等待二次确认框弹出并点击同意
            # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")))
            # agree_button = driver.find_element(By.CSS_SELECTOR, ".el-message-box__btns .el-button--primary")
            # human_click_random_delay(driver, agree_button)

            # 点击登录按钮
            print("正在点击登录按钮...----")
            time.sleep(1)
            print("正在点击登录按钮...++++")
            login_button = driver.find_element(By.CLASS_NAME, "login-btn")
            login_button.click()
            
            # 等待登录操作完成，判断是否跳转到主页
            WebDriverWait(driver, 10).until(EC.url_changes(HOME_URL))
            time.sleep(2)
            print(f"当前页面URL: {driver.current_url}")

            # 登录后保存新的 Cookies 和 Local Storage 数据
            authenticator.save_cookies_and_local_storage()
            
            # 修改当前的url地址
            driver.get(HOME_URL)
            current_url = driver.current_url
            print(f"当前页面URL保存之后的: {driver.current_url}")
            time.sleep(3)
            # 搜索信息
            print("开始搜索信息....1", current_url)
            search_info(driver, search_keyword, current_url)
        else:
            # 搜索信息
            print("开始搜索信息....2", driver.current_url)
            search_info(driver, search_keyword, CPC_HOME_URL)

    except Exception as e:
        print(f"发生异常: {e}")
    finally:
        driver.quit()
