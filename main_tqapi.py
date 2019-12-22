import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon, QFont
import json
from apis.tqapi import Tianqiapi

Pending_Message = "请稍后，程序正在获取信息...\n这将最多花费5秒钟"
Error_Message = "系统错误，请重新输入内容！\n\n可能原因：\n1.请在搜索时，不要在城市名里加上“市”或“区”！\n2.本API不支持除中国以外的国家和地区\n3.网络连接出现问题"

with open("config.json", encoding="UTF-8", mode="r") as file:
    content = json.load(file)
    DefaultCity = content["DefaultCity"]
    LoadingBeforeShowing = content["LoadingBeforeShowing"]

class App:
    def __init__(self):
        global LoadingBeforeShowing, DefaultCity
        self.weather = Tianqiapi(str(35445442), str("DBa3xzEd"), Error_Message)
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setGeometry(100, 100, 500, 700)
        self.window.setWindowTitle("Qt天气查询系统 © sctop")
        self.main()
        self.run()
        self.window.show()
        self.app.exec_()

    def main(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(10)
        self.window.setLayout(self.layout)

        font_21 = QFont("微软雅黑", 21)
        font_13 = QFont("微软雅黑", 13)

        self.lb_search = QLabel("天气查询", self.window)
        self.lb_search.setAlignment(Qt.AlignCenter)
        self.lb_search.setFont(font_21)
        self.layout.addWidget(self.lb_search, 0, 0, 1, 2)

        self.lb_city = QLabel("城市：")
        self.lb_city.setAlignment(Qt.AlignCenter)
        self.lb_city.setFont(font_13)
        self.layout.addWidget(self.lb_city, 1, 0, 1, 1)

        self.edit_city = QLineEdit()
        self.edit_city.setFont(font_13)
        self.layout.addWidget(self.edit_city, 1, 1, 1, 1)

        self.btn_1d = QPushButton("今日天气")
        self.btn_1d.setFont(font_13)
        self.layout.addWidget(self.btn_1d, 2, 0, 1, 1)

        self.btn_7d = QPushButton("七日天气")
        self.btn_7d.setFont(font_13)
        self.layout.addWidget(self.btn_7d, 2, 1, 1, 1)

        self.weather_info = QTextBrowser()
        self.weather_info.setText("此处显示天气信息")
        self.weather_info.setFont(font_13)
        self.layout.addWidget(self.weather_info, 3, 0, 1, 2)

        self.defalt()

    def run(self):
        self.btn_1d.clicked.connect(self.set_1d)
        self.btn_7d.clicked.connect(self.set_7d)

    def set_1d(self):
        if self.edit_city.text():
            self.weather_info.setText(Pending_Message)
            res = self.weather.get_1d(self.edit_city.text())
            self.weather_info.setText(res)

    def set_7d(self):
        if self.edit_city.text():
            self.weather_info.setText(Pending_Message)
            res = self.weather.get_7d(self.edit_city.text())
            self.weather_info.setText(res)

    def defalt(self):
        if LoadingBeforeShowing:
            res = self.weather.get_7d(DefaultCity)
            self.weather_info.setText("程序默认载入数据（地区："+DefaultCity+"）\n"+res)
            self.edit_city.setText(DefaultCity)
        else:
            self.weather_info.setText("欢迎使用天气查询系统！")


main = App()
