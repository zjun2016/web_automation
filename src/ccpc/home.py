import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
from .detail import jump_to_detail

def safe_get_text(element, default="无内容"):
    """Safely get the text of an element."""
    if element:
        return element.get_text(strip=True)
    return default

def safe_get_split_text(element, delimiter="：", index=1, default="无内容"):
    """Safely get the split text."""
    if element:
        text = element.get_text(strip=True)
        if delimiter in text:
            return text.split(delimiter)[index] if len(text.split(delimiter)) > index else default
    return default

def search_info(driver, search_keyword, current_url):
    print("开始搜索信息....search_info:", current_url,search_keyword)
    # 定位到搜索框并输入内容
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.el-input__inner')))
    print("search_box:", search_box)
    search_box.clear()  # 清空搜索框（防止之前的搜索内容）
    search_box.send_keys(search_keyword)  # 输入传入的搜索关键词

    # 定位到搜索按钮并点击
    search_button = driver.find_element(By.ID, 'searchBtn')
    search_button.click()
    print("search_button:", search_button)

    # 等待页面加载
    time.sleep(3)

    # 获取页面的HTML源码
    html_content = driver.page_source
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")
            
    # 查找id为entryId的元素
    entry_element = soup.find(id="entryId")
    if not entry_element:
        print("未找到entryId元素")
        return

    # 查找包含所有checkbox_item的容器
    entry_main = entry_element.find("div", class_="entry_main")
    checkbox_group = entry_main.find("div", class_="el-checkbox-group")
    checkbox_items = checkbox_group.find_all("div", class_="checkbox_item")

    # 遍历所有条目提取信息
    for item in checkbox_items:
        # 提取标题
        title = safe_get_text(item.find("div", class_="one").find("span"))
        # 提取类型
        tag = safe_get_text(item.find("div", class_="item_tag").find("span"))
        # 提取投资额
        investment_amount = safe_get_text(item.find("div", class_="overClass").find("span", class_="red"))
        # 提取进展阶段、领域类型、地区、发布时间、甲方单位
        over_class_divs = item.find_all("div", class_="overClass")
        progress_stage = safe_get_split_text(over_class_divs[1], "：", 1) if len(over_class_divs) > 1 else "无进展阶段"
        field_type = safe_get_split_text(over_class_divs[2], "：", 1) if len(over_class_divs) > 2 else "无领域类型"
        region = safe_get_split_text(over_class_divs[3], "：", 1) if len(over_class_divs) > 3 else "无地区"
        publish_date = safe_get_split_text(over_class_divs[4], "：", 1) if len(over_class_divs) > 4 else "无发布时间"
        party_unit = safe_get_split_text(over_class_divs[5], "：", 1) if len(over_class_divs) > 5 else "无甲方单位"

        # 输出格式化信息
        print(f"标题: {title}")
        print(f"类型: {tag}")
        print(f"投资额(万元)：{investment_amount}")
        print(f"(发布时间) 进展阶段： {progress_stage}; 领域类型：{field_type}; 地区：{region}; 发布时间： {publish_date}; 甲方单位：{party_unit}")
        print("-" * 80)
        print('\n')
    
    # 获取用户需要点击的详情页序号，默认点击的是第一个，默认序号用0表示
    detail_index = input("请输入需要查看详情的序号(默认为1): ")
    detail_index = int(detail_index) if detail_index else 0
    
    # 使用XPath定位到指定的元素
    # xpath = f"//*[@id='entryId']//div[@class='entry_main']//div[@class='el-checkbox-group']/div[@class='checkbox_item'][{detail_index + 1}]//div[1]/span"
    xpath = f"//div[@class='el-checkbox-group']/div[@class='checkbox_item'][{detail_index + 1}]//div[@class='one']//span"
    print(f"定位到的XPath: {xpath}")

    # 通过XPath定位选中的 checkbox
    try:
        select_checkbox_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        print(f"选中的 checkbox: {select_checkbox_item}")
    except Exception as e:
        print(f"定位元素时发生错误: {e}")
        exit()

    # 点击详情页
    try:
        # 滚动到目标元素
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", select_checkbox_item)
        # 使用 JavaScript 直接点击
        driver.execute_script("arguments[0].click();", select_checkbox_item)
    except StaleElementReferenceException:
        print("元素已失效，忽略异常")
    except Exception as e:
        print(f"点击标题时发生错误: {e}")
    except Exception as e:
        print(f"点击标题时发生错误: {e}")
        return  # 终止函数，避免错误继续执行


    # 记录原来的窗口句柄
    original_window = driver.current_window_handle
    print(f"原始窗口: {original_window}")
    # 获取当前所有窗口
    all_windows_before_click = driver.window_handles
    print(f"所有窗口: {all_windows_before_click}")
    # 等待新的窗口打开
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > len(all_windows_before_click))
    print("新窗口已打开")
    # 获取新窗口句柄
    new_window = [window for window in driver.window_handles if window != original_window][0]
    print(f"新窗口: {new_window}")
    # 切换到新窗口
    driver.switch_to.window(new_window)
    print("切换到新窗口")
    time.sleep(3)
    jump_to_detail(driver, search_keyword)
