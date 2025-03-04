import easyocr
from PIL import Image,ImageEnhance
from io import BytesIO
import base64
import numpy as np
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def solve_captcha_with_easyocr(driver):
    # 等待验证码图片加载
    captcha_image_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-input-group__append img"))
    )

    # 确保图片可见
    WebDriverWait(driver, 2).until(EC.visibility_of(captcha_image_element))
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.el-input-group__append img")))
    
    # 获取图片的src属性（Blob URL）
    captcha_image_src = captcha_image_element.get_attribute("src")
    
    # 如果是Blob URL，使用JavaScript获取实际的图片内容
    if captcha_image_src.startswith('blob:'):
        image_data = driver.execute_script("""
            var img = document.querySelector('img[src^="blob:"]');
            if (img) {
                var canvas = document.createElement('canvas');
                var context = canvas.getContext('2d');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                context.drawImage(img, 0, 0);
                return canvas.toDataURL('image/png').split(',')[1];  // 只获取Base64部分
            }
            return null;
        """)

        if image_data:
            # 将Base64字符串解码为二进制数据
            image_data = base64.b64decode(image_data)
            
            # 打开图像文件
            captcha_image = Image.open(BytesIO(image_data))
        else:
            print("无法获取验证码图片数据")
            return None
    else:
        # 如果是普通的URL，直接下载
        response = requests.get(captcha_image_src)
        captcha_image = Image.open(BytesIO(response.content))

    # 1. 转换为灰度图像
    captcha_image = captcha_image.convert('L')

    # 2. 增强对比度：提升文本的对比度，使得文本更突出
    enhancer = ImageEnhance.Contrast(captcha_image)
    captcha_image = enhancer.enhance(3.0)

    # threshold = 150  # 阈值可以根据实际情况调整
    # captcha_image = captcha_image.point(lambda p: 255 if p > threshold else 0)

    # 显示处理后的图像（可选）
    captcha_image.show()

    # 4. 将 PIL 图像转换为 NumPy 数组
    captcha_image_np = np.array(captcha_image)

    # 4. 使用 easyocr 进行 OCR 识别
    reader = easyocr.Reader(['en'])  # 识别英文数字
    result = reader.readtext(captcha_image_np)

    # 输出识别结果
    if result:
        captcha_text = result[0][1]  # 取识别的第一个文本结果
        print(f"识别的验证码是: {captcha_text}")
        return captcha_text
    else:
        print("无法识别验证码")
        return None
