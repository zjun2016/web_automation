# web_automation

接入大模型的OCR识别和使用selenium实现页面自动化操作
Integrating Large Model OCR Recognition and Implementing Page Automation Using Selenium

# 项目需要使用虚拟环境

1.1 创建虚拟环境
python3 -m venv venv
1.2 激活虚拟环境
在 macOS/Linux 上，运行：
source venv/bin/activate
在 Windows 上，运行：
venv\Scripts\activate

# 安装依赖包

pip3 install selenium webdriver-manager
pip3 install --upgrade 'openai>=1.0' #使用的是moonshot的接口
pip3 install Pillow

# 创建 requirements.txt 文件
pip3 freeze > requirements.txt

# 如果需要根据requirements.txt安装依赖包
pip3 install -r requirements.txt

# 运行项目 - 首先需要激活虚拟环境
python3 run.py
或者
python3 -m src.main