import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def jump_to_detail(driver, search_keyword):
    print("jump_to_detail------search_keyword:",search_keyword)
    # 等待新页面加载
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "detailAuto")))
        print("成功跳转到详情页")
    
        # 假设 detail_page_html 是详情页的 HTML 源码
        detail_page_html = driver.page_source
        print("detail_page_html:",detail_page_html)

        detail_soup = BeautifulSoup(detail_page_html, "html.parser")
        print("detail_soup:",detail_soup)

        # 定位到 id="detailAuto" 的容器
        detail_auto = detail_soup.find("div", id="detailAuto")
        print("detail_auto:",detail_auto)

        if detail_auto:
            # 提取项目标题
            title_element = detail_auto.find("div", id="original_title").find("h3") if detail_auto.find("div", id="original_title") else None
            project_title = title_element.find("span").get_text(strip=True) if title_element and title_element.find("span") else "无标题"

            # 提取项目地址
            address_element = detail_auto.find("div", class_="address")
            project_address = address_element.get_text(strip=True) if address_element else "无地址"

            # 打印结果
            print(f"项目标题: {project_title}")
            print(f"项目地址: {project_address}")
        else:
            print("未找到 id='detailAuto' 的容器")
    except Exception as e:
        print(f"等待页面跳转或解析详情页时发生错误: {e}")
    time.sleep(20)