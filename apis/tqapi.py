import requests

class Tianqiapi():
    def __init__(self, appid, appsecret, Error_Message):
        self.appid = appid
        self.appsecret = appsecret
        self.Error_Message = Error_Message
        self.headers = {
            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
        }

    def get_weather(self, name):
        try:
            res = requests.get(
                f"https://www.tianqiapi.com/api/?version=v1&city={name}&appid={self.appid}&appsecret={self.appsecret}",
                headers=self.headers, timeout=5).json()
        except Exception as e:
            return 0
        cityname = res["city"].encode("unicode_escape").decode("unicode_escape")
        if cityname == name:
            return {"data": res["data"], "date": res["update_time"]}
        else:
            return 0

    def get_1d(self, name):
        res = self.get_weather(name)
        if res == 0: return self.Error_Message
        weather = res["data"][0]

        update_date = res["date"].encode("unicode_escape").decode("unicode_escape")
        air = weather["air"]
        air_level = weather["air_level"].encode("unicode_escape").decode("unicode_escape")
        weather_date = weather["date"].encode("unicode_escape").decode("unicode_escape")
        tem_now = weather["tem"].encode("unicode_escape").decode("unicode_escape")
        tem_low = weather["tem2"].encode("unicode_escape").decode("unicode_escape")
        tem_high = weather["tem1"].encode("unicode_escape").decode("unicode_escape")
        shidu = weather["humidity"]
        fengxiang = weather["win"][0].encode("unicode_escape").decode("unicode_escape")
        fengsu = weather["win_speed"].encode("unicode_escape").decode("unicode_escape")
        tianqi = weather["wea"].encode("unicode_escape").decode("unicode_escape")

        string = f"""更新时间：{update_date}，城市：{name}\n
    预报时间：{weather_date}
    {tianqi}；当前{tem_now}，最低{tem_low}，最高{tem_high}
    湿度：{shidu}%
    空气质量：{air}  {air_level}
    风向：{fengxiang}  风速：{fengsu}"""
        return string

    def get_7d(self, name):
        res = self.get_weather(name)
        if res == 0: return self.Error_Message
        update_date = res["date"].encode("unicode_escape").decode("unicode_escape")
        string = f"""更新时间：{update_date}，城市：{name}\n"""
        for i in range(len(res["data"])):
            weather = res["data"][i]
            try:
                air = weather["air"]
                air_level = weather["air_level"].encode("unicode_escape").decode("unicode_escape")
                shidu = str(weather["humidity"]) + '%'
            except Exception:
                air = "暂无空气质量信息"
                air_level = ""
                shidu = "暂无湿度信息"
            weather_date = weather["date"].encode("unicode_escape").decode("unicode_escape")
            tem_now = weather["tem"].encode("unicode_escape").decode("unicode_escape")
            tem_low = weather["tem2"].encode("unicode_escape").decode("unicode_escape")
            tem_high = weather["tem1"].encode("unicode_escape").decode("unicode_escape")
            fengxiang = weather["win"][0].encode("unicode_escape").decode("unicode_escape")
            fengsu = weather["win_speed"].encode("unicode_escape").decode("unicode_escape")
            tianqi = weather["wea"].encode("unicode_escape").decode("unicode_escape")

            string += f"""\n预报时间：{weather_date}
    {tianqi}；当前{tem_now}，最低{tem_low}，最高{tem_high}
    湿度：{shidu}
    空气质量：{air}  {air_level}
    风向：{fengxiang}  风速：{fengsu}\n"""
        return string
