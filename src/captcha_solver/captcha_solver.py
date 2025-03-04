import base64
import io
from PIL import Image
import re
from openai import OpenAI
from src.config import OPENAIKEY

# 创建 OpenAI 客户端
client = OpenAI(
    api_key=OPENAIKEY, # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1",
)

def identifyVerificationCodeWithAI(img_base):
    resultStr = identifyImgWithAI(img_base)
    number = extract_number_after_equal(resultStr)
    print(number)
    return number

def identifyImgWithAI(img_base):
    img_base = f"data:image/png;base64,{img_base}"
    completion = client.chat.completions.create(
    model="moonshot-v1-8k-vision-preview",
    messages=[
        {"role": "system", "content": "你是 AA"},
        {
            "role": "user",
            # 注意这里，content 由原来的 str 类型变更为一个 list，这个 list 中包含多个部分的内容，图片（image_url）是一个部分（part），
            # 文字（text）是一个部分（part）
            "content": [
                {
                    "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                    "image_url": {
                        "url": img_base,
                    },
                },
                {
                    "type": "text",
                    "text": "请描述图片的内容，并给出这个验证码图片计算后的结果", # <-- 使用 text 类型来提供文字指令，例如“描述图片内容”
                },
                ],
            },
        ],
    )
    resultStr = completion.choices[0].message.content
    print(resultStr)
    return resultStr


def extract_number_after_equal(s):
    # 使用正则表达式匹配等号后面的数字
    match = re.search(r'=\s*(\d+)', s)
    if match:
        return match.group(1)  # 返回匹配的数字部分
    else:
        return None  # 如果没有匹配到数字，返回None



#/ 验证码图片路径
# 配置 Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# def preprocess_image(image_path):
#     # 打开图片文件
#     img = Image.open(image_path)
    
#     # 转换为灰度图像
#     gray_img = img.convert('L')

#     # 提高对比度
#     enhancer = ImageEnhance.Contrast(gray_img)
#     enhanced_img = enhancer.enhance(2.0)
#     enhanced_img.show()

#     # 使用中值滤波去噪
#     filtered_img = enhanced_img.filter(ImageFilter.MedianFilter(size=3))
#     filtered_img.show()

#     # 将滤波后的图像转换为 numpy 数组
#     np_image = np.array(filtered_img)

#     # 使用 Canny 边缘检测
#     edges = cv2.Canny(np_image, 100, 200)

#     # 将边缘图像转换为 PIL 图像
#     edges_img = Image.fromarray(edges)
#     edges_img.show()  # 显示边缘检测结果

#     # 二值化处理
#     _, binary_img = cv2.threshold(np_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#     # 返回处理后的图像
#     binary_img = Image.fromarray(binary_img)
#     binary_img.show()

#     return binary_img

# def solve_captcha(image_path):
#     # 预处理图片
#     processed_image = preprocess_image(image_path)
    
#     # 使用 OCR 解析图片
#     custom_config = r'--oem 3 --psm 6'  # 调整 OCR 配置
#     captcha_text = pytesseract.image_to_string(processed_image, lang="eng", config=custom_config)
#     captcha_text = captcha_text.strip()
    
#     if not captcha_text:
#         raise ValueError("无法识别验证码文字，请检查图片质量")

#     print(f"OCR 解析结果：{captcha_text}")

#     # 解析并计算结果
#     # 匹配数字、加减乘除运算符、等于号和问号
#     expression = re.findall(r"\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\?", captcha_text)
#     if not expression:
#         raise ValueError("无法解析验证码表达式")

#     # 提取表达式并计算结果
#     expression = expression[0].replace("=", "").strip()  # 去掉等号
#     result = eval(expression)
#     return str(result)



def extract_base64_data(page_source):
    # 使用正则表达式匹配 Base64 数据
    pattern = r'src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"'
    match = re.search(pattern, page_source)
    # print('extract_base64_data----', match)
    if match:
        return match.group(1)  # 返回匹配到的 Base64 数据
    else:
        raise ValueError("无法找到 Base64 数据")

def save_base64_image(base64_data, output_path):
    # 去掉 Base64 数据的前缀（如 data:image/jpeg;base64,）
    base64_data = base64_data.split(",")[-1]
    
    # 将 Base64 数据解码为二进制数据
    image_data = base64.b64decode(base64_data)
    
    # 使用 PIL 打开图片并保存
    image = Image.open(io.BytesIO(image_data))
    image.save(output_path, format="PNG")  # 保存为 PNG 格式
    print(f"图片已保存到 {output_path}")