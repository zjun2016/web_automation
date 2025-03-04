from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def initialize_driver_with_profile():
    chrome_driver_path = '/usr/local/bin/chromedriver'  # 替换为你本地的 chromedriver 路径
    chrome_user_data_dir = '/Users/zjun/Library/Application Support/Google/Chrome/Profile 4/'  # 使用你找到的路径
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 如果不需要显示浏览器界面可以启用无头模式
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # 设置自定义浏览器指纹
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")  # 使用已存在的用户数据目录
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # 自定义User-Agent
    options.add_argument("accept-language=zh-CN,zh;q=0.9,en;q=0.8")  # 设置语言
    options.add_argument("window-size=1920x1080")  # 设置浏览器窗口大小
    # options.add_argument("--proxy-server=http://your.proxy.server:port") # 可以通过 --proxy-server 参数来设置自定义代理，从而隐藏真实 IP 地址。
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def kimi_upload_and_send_message(file_path, max_retries=3):
    retry_count = 0
    
    while retry_count < max_retries:
        # 初始化浏览器
        driver = initialize_driver_with_profile()

        # 打开目标网页 http://10.25.114.122:8080/  https://kimi.moonshot.cn/ /Users/zjun/Desktop/baoxian.jpeg
        driver.get("https://kimi.moonshot.cn/")

        # 等待页面加载
        time.sleep(2)

        try:
            # 找到文件上传的 input 元素
            file_input = driver.find_element(By.XPATH, '//label[contains(@class, "attachment-button")]/input[@type="file"]')
            file_input.send_keys(file_path)  # 上传用户指定的本地文件
            time.sleep(5)

            # 找到输入框并通过 JavaScript 输入“请帮我识别附件图片内容”
            input_box = driver.find_element(By.XPATH, '//div[contains(@class, "chat-input-editor")]')
            # 使用 JavaScript 插入文本内容到 <span> 标签中
            driver.execute_script("arguments[0].innerHTML = '<p><span data-lexical-text=\"true\">请帮我识别附件图片内容</span></p>';", input_box)

            # 选择发送按钮所在的 div 元素
            send_button = driver.find_element(By.XPATH, '//div[contains(@class, "send-button-container")]//div[@class="send-button"]')


            time.sleep(1)

            # 点击发送按钮
            send_button.click()

            # 等待 2 秒钟，等待服务端返回数据
            time.sleep(32)

            # 获取所有的聊天记录
            all_text = get_all_text(driver)
            print("获取到的全部聊天记录：", all_text)
            time.sleep(2)

            if all_text:
                print("聊天记录返回结果：", all_text)
                driver.quit()  # 关闭浏览器
                return all_text
            else:
                print("未获取到聊天记录，正在刷新页面并重试...")
                driver.refresh()  # 刷新页面
                retry_count += 1
                time.sleep(2)
        except Exception as e:
            print(f"执行过程中发生错误: {e}")
            driver.quit()
            break

    # 超过最大重试次数
    print("尝试超过最大次数，未能成功获取聊天记录。")
    return None


def get_all_text(driver):
    try:
        # 获取所有聊天记录
        messages = driver.find_elements(By.CLASS_NAME, "markdown")
        print(f"获取到 {len(messages)} 条聊天记录。messages:{messages}")
        
        all_texts = []
        for message in messages:
            paragraphs = message.find_elements(By.CLASS_NAME, "paragraph")
            for paragraph in paragraphs:
                all_texts.append(paragraph.text.strip())
        
        # 返回所有文本的合并结果
        return "\n".join(all_texts)
    except Exception as e:
        print(f"获取所有聊天记录时出错: {e}")
        return None
