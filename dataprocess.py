from apis.hefengapi import Hefengapi
from apis.caiyunapi import Caiyunapi
from file_loading import decoding_password
import time

Pending_Message = "请稍后，程序正在获取信息...\n这将最多花费5秒钟"
Error_Message = """系统错误，请重新输入内容！\n
可能原因：
1.请在搜索时，不要在城市名里加上“市”或“区”！
2.本API不支持除中国以外的国家和地区
3.网络连接出现问题
4.API每日调用超出限额(可在开发者模式下看到)"""
Not_Available_Message = "抱歉，本功能由于API暂未支持，或开发者在编程时禁用了该功能，所以您才会看到此提示信息。\n唯一解决方案：请静候更新！"
TestList = decoding_password("password.json")


def is_debug(test):
    global TestList
    if str(test).lower() in TestList:
        return 0
    else:
        return 1


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class Hefeng:
    def __init__(self, editcity, debugging, weather_info, query_time, token):
        self.hefeng_editcity = editcity
        self.debugging = debugging
        self.weather_info = weather_info
        self.weather = Hefengapi(token, Error_Message)
        self.query_time = query_time

    def set_realtime(self):
        if self.hefeng_editcity.text():
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.realtime(self.hefeng_editcity.text())
                self.weather_info.setText(str(res))
            else:
                self.weather_info.setText(self.weather.debugging(self.hefeng_editcity.text(), 1))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_forecast(self):
        if self.hefeng_editcity.text():
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.forecast(self.hefeng_editcity.text())
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(self.hefeng_editcity.text(), 3))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_houly(self):
        if self.hefeng_editcity.text():
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.hourly(self.hefeng_editcity.text())
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(self.hefeng_editcity.text(), 2))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_air_realtime(self):
        if self.hefeng_editcity.text():
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.air_now(self.hefeng_editcity.text())
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(self.hefeng_editcity.text(), 4))
            self.query_time.setText("信息查询时间戳：" + get_time())


class Caiyun:
    def __init__(self, editcity, debugging, weather_info, query_time, token):
        self.editcity = editcity
        self.debugging = debugging
        self.weather_info = weather_info
        self.weather = Caiyunapi(Error_Message, token)
        self.query_time = query_time
        # TAkhjf8d1nlSlspN 彩云公开测试用key

    def set_realtime(self):
        if self.editcity.text():
            pos = self.trans_pos(self.editcity.text())
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.realtime(pos)
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(pos, 1))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_2hour(self):
        if self.editcity.text():
            pos = self.trans_pos(self.editcity.text())
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.forecast_2hour(pos)
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(pos, 2))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_houly(self):
        if self.editcity.text():
            pos = self.trans_pos(self.editcity.text())
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.forecast_hourly(pos)
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(pos, 2))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def set_daily(self):
        if self.editcity.text():
            pos = self.trans_pos(self.editcity.text())
            if is_debug(self.debugging.text()) == 1:
                self.weather_info.setText(Pending_Message)
                res = self.weather.forecast_daily(pos)
                self.weather_info.setText(res)
            else:
                self.weather_info.setText(self.weather.debugging(pos, 2))
            self.query_time.setText("信息查询时间戳：" + get_time())

    def trans_pos(self, pos):
        temp = str(pos)
        try:
            temp2 = temp.split(",")
        except Exception as e:
            print(e)
            return self.weather_info.setText(Error_Message)
        else:
            return temp2
