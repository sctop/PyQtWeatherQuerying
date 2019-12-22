import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon, QFont
import json
from dataprocess import Hefeng, Caiyun, is_debug
import time
import random

with open("config.json", encoding="UTF-8", mode="r") as file:
    content = json.load(file)
    DefaultCity = content["Default"]["city"]
    DefaultAddress = content["Default"]["latlon"]

# 针对1920*1080 16:9屏幕设计
__size__ = (730,800)
# WAAAAAAAAAAAAAAAAAAAAAAAAAARFRAAAAAAAAAAAAAAAAAAAME!
with open("something.json", encoding="UTF-8", mode='r') as file:
    introduction = json.load(file)

class App:
    def __init__(self):
        global DefaultCity, DefaultAddress
        self.font_21 = QFont("微软雅黑", 21)
        self.font_13 = QFont("微软雅黑", 13)
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setGeometry(100, 100, __size__[0], __size__[1])
        self.window.setWindowTitle("PyQt天气查询系统")
        self.window.setWindowIcon(QIcon("favicon.ico"))
        self.main()
        self.hefeng = Hefeng(self.hefeng_editcity, self.debugging, self.weather_info, self.query_time, "Your key here")
        self.caiyun = Caiyun(self.caiyun_editcity, self.debugging, self.weather_info, self.query_time, "Your key here")
        self.run()
        self.window.show()
        self.defalt()
        self.app.exec_()

    def main(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        self.window.setLayout(self.layout)

        self.lb_search = QLabel("天气查询系统", self.window)
        self.lb_search.setAlignment(Qt.AlignCenter)
        self.lb_search.setFont(self.font_21)
        self.layout.addWidget(self.lb_search, 0, 0, 1, 12)

        self.copyright = QLabel("Powered by Python - Developed by sctop")
        self.copyright.setAlignment(Qt.AlignCenter)
        self.copyright.setFont(QFont("微软雅黑", 9))
        self.layout.addWidget(self.copyright, 1, 0, 1, 12)

        self.hefeng_add()
        self.caiyun_add()

        # debug专用
        self.debugging = QLineEdit()
        self.debugging.setFont(self.font_13)
        self.debugging.setPlaceholderText("DEBUGGING_PARAM")
        self.layout.addWidget(self.debugging, 2, 8, 1, 4)

        # 显示数据
        self.weather_info = QTextBrowser()
        self.weather_info.setText("此处显示天气信息")
        self.weather_info.setFont(self.font_13)
        self.layout.addWidget(self.weather_info, 6, 0, 1, 12)

        # 显示查询时间
        self.query_time = QLineEdit()
        self.query_time.setFont(self.font_13)
        self.query_time.setText("此处显示查询时间")
        self.query_time.setAlignment(Qt.AlignCenter)
        self.query_time.setReadOnly(True)
        self.layout.addWidget(self.query_time, 7, 0, 1, 12)

        # 关于按钮
        self.btn_about = QPushButton("关于本程序")
        self.btn_about.setFont(self.font_13)
        self.layout.addWidget(self.btn_about,8,0,1,6)

        # 帮助按钮
        self.btn_help = QPushButton("使用说明")
        self.btn_help.setFont(self.font_13)
        self.layout.addWidget(self.btn_help, 8, 6, 1, 6)

    def run(self):
        self.btn_hefeng_realtime.clicked.connect(self.hefeng.set_realtime)
        self.btn_hefeng_7d.clicked.connect(self.hefeng.set_forecast)
        self.btn_hefeng_hourly.clicked.connect(self.hefeng.set_houly)
        self.btn_hefeng_air_realtime.clicked.connect(self.hefeng.set_air_realtime)
        self.btn_caiyun_2hour.clicked.connect(self.caiyun.set_2hour)
        self.btn_caiyun_realtime.clicked.connect(self.caiyun.set_realtime)
        self.btn_caiyun_daily.clicked.connect(self.caiyun.set_daily)
        self.btn_caiyun_hourly.clicked.connect(self.caiyun.set_houly)
        self.btn_about.clicked.connect(self.about)
        self.btn_help.clicked.connect(self.help)

    def hefeng_add(self):
        self.lb_city = QLabel("欲查询的城市名/ID/经纬度/auto_ip：")
        self.lb_city.setAlignment(Qt.AlignCenter)
        self.lb_city.setFont(self.font_13)
        self.layout.addWidget(self.lb_city, 2, 0, 1, 4)

        self.hefeng_editcity = QLineEdit()
        self.hefeng_editcity.setFont(self.font_13)
        self.hefeng_editcity.setPlaceholderText("在这里键入...")
        self.layout.addWidget(self.hefeng_editcity, 2, 4, 1, 4)

        self.btn_hefeng_realtime = QPushButton("当前实况天气")
        self.btn_hefeng_realtime.setFont(self.font_13)
        self.layout.addWidget(self.btn_hefeng_realtime, 3, 0, 1, 3)

        self.btn_hefeng_7d = QPushButton("七日天气预报")
        self.btn_hefeng_7d.setFont(self.font_13)
        self.layout.addWidget(self.btn_hefeng_7d, 3, 3, 1, 3)

        self.btn_hefeng_hourly = QPushButton("未来1天逐三小时预报")
        self.btn_hefeng_hourly.setFont(self.font_13)
        self.layout.addWidget(self.btn_hefeng_hourly, 3, 6, 1, 3)

        self.btn_hefeng_air_realtime = QPushButton("当前实况空气质量")
        self.btn_hefeng_air_realtime.setFont(self.font_13)
        self.layout.addWidget(self.btn_hefeng_air_realtime, 3, 9, 1, 3)

    def caiyun_add(self):
        self.lb_jingwei = QLabel("欲查询的经纬度(使用逗号隔开经度和纬度)：")
        self.lb_jingwei.setAlignment(Qt.AlignCenter)
        self.lb_jingwei.setFont(self.font_13)
        self.layout.addWidget(self.lb_jingwei, 4, 0, 1, 6)

        self.caiyun_editcity = QLineEdit()
        self.caiyun_editcity.setFont(self.font_13)
        self.caiyun_editcity.setPlaceholderText("在这里键入...")
        self.layout.addWidget(self.caiyun_editcity, 4, 6, 1, 6)

        self.btn_caiyun_realtime = QPushButton("当前实况天气")
        self.btn_caiyun_realtime.setFont(self.font_13)
        self.layout.addWidget(self.btn_caiyun_realtime, 5, 0, 1, 3)

        self.btn_caiyun_2hour = QPushButton("两小时降雨概率")
        self.btn_caiyun_2hour.setFont(self.font_13)
        self.layout.addWidget(self.btn_caiyun_2hour, 5, 3, 1, 3)

        self.btn_caiyun_hourly = QPushButton("未来三天逐小时预报")
        self.btn_caiyun_hourly.setFont(self.font_13)
        self.layout.addWidget(self.btn_caiyun_hourly, 5, 6, 1, 3)

        self.btn_caiyun_daily = QPushButton("未来五天预报")
        self.btn_caiyun_daily.setFont(self.font_13)
        self.layout.addWidget(self.btn_caiyun_daily, 5, 9, 1, 3)

    def defalt(self):
        self.hefeng_editcity.setText(DefaultCity)
        self.caiyun_editcity.setText(DefaultAddress)
        self.weather_info.setText("""嗨！这里是开发者，非常开心你能够使用本程序！""")

    def about(self):
        if is_debug(self.debugging.text()) != 1:
            keys = [self.hefeng.weather.key,self.caiyun.weather.token]
        else:
            keys=["[key]","[key]"]
        self.weather_info.setText(f"""本程序使用了PyQt、requests等库对程序的主体部分进行开发
本程序使用了 和风天气(www.heweather.com) 与 彩云天气(caiyunapp.com) 的API进行数据的提供\n
和风天气API地址：\n1. 天气查询：https://free-api.heweather.net/s6/weather/[request_mode]?location=[name]&key={keys[0]}
2. 空气查询：https://free-api.heweather.net/s6/air/[request_mode]?location=[name]&key=[key]
彩云天气API地址：\n1. 实况天气：https://api.caiyunapp.com/v2/{keys[1]}/[pos]/realtime.json?lang=zh_CN&unit=metric&tzshift=28800
2. 预报天气：https://api.caiyunapp.com/v2/[token]/[pos]/forecast.json?lang=zh_CN&unit=metric&tzshift=28800
(注：彩云天气的API使用的是公共API key，不保障7×24小时全天候的服务可用性)\n
关注开发者的最新动态：
QQ：2094880085
GitHub：https://github.com/sctop 
Bilibili：https://space.bilibili.com/93650528
Warframe中文维基：https://warframe.huijiwiki.com/wiki/用户:Sctop
邮箱：2094880085@qq.com / sctopzhang@gmail.com / sctopzhang@outlook.com\n
Powered by Python - Designed and developed by Sctop
本项目开源地址：https://github.com/PythonQtWeatherQuerying\n\n
-----------------------一些小秘密-----------------------\n"""+random.choice(introduction))
        self.query_time.setText("信息查询时间戳："+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    def help(self):
        self.weather_info.setText("""本程序最上面的输入框使用和风天气API，其用于输入查询的地址。该地址可以是以下格式中的其中任意一种：
1. 城市ID。城市ID列表见：https://dev.heweather.com/docs/refer/city
2. 经纬度格式：“经度,纬度”（经度在前纬度在后，英文,分隔，十进制格式，北纬东经为正，南纬西经为负）
3. 城市名称，支持中英文和汉语拼音
4. 城市名称，上级城市 或 省 或 国家，英文,分隔，此方式可以在重名的情况下只获取想要的地区的天气数据，例如 西安,陕西
5. IP地址(xxx.xxx.xxx.xxx)
6. 根据请求自动判断，根据用户的请求获取IP，通过 IP 定位并获取城市数据\n
该地址输出框的右侧为开发者Debug专用，需要输入对应的Debug字段才能进入开发者的专用模式。
该模式将显示请求的原内容，信息量较大，建议使用Chrome + Devtools -> Network -> Preview来查看JSON关系图。
Debug字段已公布在程序中可供预览的部分中，不需要查看源代码即可获取到专属字段。\n
第三个输入框使用彩云天气API，其用于输入查询的经纬度。
经纬度格式见以上内容。\n
------------------------------------------------------------
由于未知原因，目前该程序的配置文件“config.json”不能通过记事本进行编辑，否则会导致程序无法运行。
若需要，请使用诸如Notepad++(https://notepad-plus-plus.org/downloads/)的工具进行修改！""")
        self.query_time.setText("信息查询时间戳：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


main = App()
