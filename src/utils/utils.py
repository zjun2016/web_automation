from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

def get_initialize_driver_with_profile():
    chrome_driver_path = '/usr/local/bin/chromedriver'  # 替换为你本地的 chromedriver 路径
    chrome_user_data_dir = '/Users/zjun/Library/Application Support/Google/Chrome/Profile 4/'  # 使用你找到的路径
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 如果不需要显示浏览器界面可以启用无头模式
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    # 设置自定义浏览器指纹
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")  # 使用已存在的用户数据目录
    options.add_argument(f"user-agent={get_random_user_agent()}")
    options.add_argument("accept-language=zh-CN,zh;q=0.9,en;q=0.8")  # 设置语言
    options.add_argument("window-size=1920x1080")  # 设置浏览器窗口大小
    # options.add_argument(f'--proxy-server={get_proxy()}')
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver



# 模拟人类输入
def human_typing_with_backspace(driver, element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # 模拟打字速度
    time.sleep(random.uniform(1, 2))  # 完成输入后增加随机停顿

# 调整页面元素交互延迟
def human_click_random_delay(driver, element):
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(random.uniform(1, 2))  # 增加随机延迟

# 获取代理信息
def get_proxy():
    proxy_list = ['http://proxy1.com', 'http://proxy2.com', 'http://proxy3.com']  # 示例代理池
    return random.choice(proxy_list)
# 增加浏览器指纹的多样性
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
    return random.choice(user_agents)


# 随机鼠标移动
def move_mouse_randomly(driver):
    width = driver.execute_script("return document.body.scrollWidth")
    height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(random.randint(3, 5)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        ActionChains(driver).move_by_offset(x, y).perform()
        time.sleep(random.uniform(0.5, 1.5))


# CAPTCHA 识别优化-将图片转为灰度图-图像二值化
def enhance_captcha_image(captcha_image):
    # 将图片转为灰度图
    captcha_image = captcha_image.convert("L")
    # 图像二值化
    captcha_image = captcha_image.point(lambda p: p > 128 and 255)
    return captcha_image