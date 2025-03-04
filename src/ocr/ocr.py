import easyocr
import base64
from src.captcha_solver.captcha_solver import identifyImgWithAI

class OCRHandler:
    def __init__(self):
        # 初始化 OCR 读取器，支持中文和英文
        self.reader = easyocr.Reader(['ch_sim', 'en'])

    # 使用easyocr识别图片
    def get_text(self, image_path: str):
        results = self.reader.readtext(image_path)
        for bbox, text, prob in results:
            print(f"文本: {text}, 置信度: {prob:.4f}")
        if results:
            return results[0][1]
    
    # 读取图片并转换为 Base64
    def _image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            base64_str = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_str

    # 使用AI识别图片
    def get_text_ai(self, image_path: str):
        base64Str = self._image_to_base64(image_path)
        identifyImgWithAI(base64Str)
