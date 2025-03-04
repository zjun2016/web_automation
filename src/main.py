from src.ccpc.ccpc_init import ccpy_login
from src.kimi.kimi_image import kimi_upload_and_send_message
from src.login_clcrc.login_clcrc import clcrc_login
from src.ocr.ocr import OCRHandler
from src.ocr.test import getTestImgPaths

def main():
    # 登录测试clcrc_ui
    # clcrc_login()


    # kimi的图片识别测试
    # 提示用户输入本地文件路径
    # file_path = input("请输入需要上传的本地文件路径（例如：/path/to/your/image.jpg）：")
    # # 检查文件路径是否存在（可选）
    # if not os.path.exists(file_path):
    #     print("文件路径不存在，请检查文件路径。")
    #     exit()
    # kimi_upload_and_send_message(file_path)



    # 使用while循环来接受有效的输入  /Users/zjun/Desktop/baoxian.jpeg
    # while True:
    #     search_keyword = input("请输入要搜索的关键词：")
    #     if not search_keyword.strip():  # 判断是否为空或仅包含空白字符
    #         print("关键词不能为空，请重新输入。")
    #     else:
    #         break  # 如果输入有效，跳出循环
    # ccpy_login(search_keyword)


    # 登录测试OCR
    imgIdx = input("请输入序号选择图片:")
    imgPath = getTestImgPaths()[int(imgIdx)]
    print('选择的图片路径为:', imgPath)
    ocrHandler = OCRHandler()
    ocrText = ocrHandler.get_text(imgPath)
    print(ocrText)

if __name__ == "__main__":
    main()
