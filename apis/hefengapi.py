import requests
import json


class Hefengapi(object):
    def __init__(self, key, error_msg):
        self.key = key
        self.error_meg = error_msg
        self.headers = {
            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
        }

    def get_weather(self, mode, cityname):
        """
        获取天气数据。

        :param mode: mode=1，实况天气；mode=2，逐小时预报；mode=3，3-10天预报
        """
        if mode == 1 or mode == 4:
            request_mode = "now"
        elif mode == 2:
            request_mode = "hourly"
        elif mode == 3:
            request_mode = "forecast"
        else:
            return 1
        try:
            if mode != 4:
                r = requests.get(f"https://free-api.heweather.net/s6/weather/{request_mode}?location={cityname}&key={self.key}",
                                 headers=self.headers, timeout=5)
            else:
                r = requests.get(f"https://free-api.heweather.net/s6/air/{request_mode}?location={cityname}&key={self.key}",
                    headers=self.headers, timeout=5)
        except Exception as e:
            print(e)
            return 1
        r.encoding = "UTF-8"
        content = r.json()["HeWeather6"][0]
        if content["status"] == "ok":
            return content
        else:
            return 1

    def realtime(self, name):
        res = self.get_weather(1, name)
        if res == 1:
            return self.error_meg
        location = f'{res["basic"]["cnty"]} {res["basic"]["admin_area"]} {res["basic"]["parent_city"]} {res["basic"]["location"]}'
        update_time = res["update"]["loc"]  # 更新时间
        zhuangkuang = res["now"]["cond_txt"]  # 天气状况
        wendu = res["now"]["tmp"]  # 温度
        feeling = res["now"]["fl"]  # 体感温度
        shidu = res["now"]["hum"]  # 湿度
        jiangshui = res["now"]["pcpn"]  # 降水量
        qiya = res["now"]["pres"]  # 大气压力
        nengjiandu = res["now"]["vis"]  # 能见度
        yunliang = res["now"]["cloud"]  # 云量
        fengxiang = res["now"]["wind_dir"]  # 风向
        fengli = res["now"]["wind_sc"]  # 风力等级
        fengsu = res["now"]["wind_spd"]  # 风速

        string = f"""更新时间：{update_time}
您所查询的地点位于{location}\n
实时温度：{wendu}℃，体感温度为{feeling}℃；当前湿度为{shidu}%；
天气状况：{zhuangkuang}，能见度：{nengjiandu}公里，云量：{yunliang}；
风速：{fengsu}公里/小时(风力{fengli}级)，风向为{fengxiang}；
当前降水量：{jiangshui}，气压：{qiya}毫安。"""
        return string

    def forecast(self, name):
        res = self.get_weather(3, name)
        if res == 1:
            return self.error_meg
        update_time = res["update"]["loc"]
        location = f'{res["basic"]["cnty"]} {res["basic"]["admin_area"]} {res["basic"]["parent_city"]} {res["basic"]["location"]}'
        string = f"""更新时间：{update_time}\n您所查询的地点位于{location}\n\n"""
        for daily in res["daily_forecast"]:
            date = daily["date"]  # 预报时间
            day_zhuangkuang = daily["cond_txt_d"]  # 白天天气状况
            night_zhuangkuang = daily["cond_txt_n"]  # 夜间天气状况
            sunrise = daily["sr"]  # 日升时间
            sunshut = daily["ss"]  # 日落时间
            moonrise = daily["mr"]  # 月升时间
            moonshut = daily["ms"]  # 月落时间
            shidu = daily["hum"]  # 湿度
            jiangshui = daily["pcpn"]  # 降水量
            jiangshuigailv = daily["pop"]  # 降水概率
            qiya = daily["pres"]  # 大气压力
            tmp_min = daily["tmp_min"]  # 最低温度
            tmp_max = daily["tmp_max"]  # 最高温度
            uv = daily["uv_index"]  # 紫外线强度指数
            nengjiandu = daily["vis"]  # 能见度
            fengxiang = daily["wind_dir"]  # 风向
            fengsu = daily["wind_spd"]  # 风速
            fengli = daily["wind_sc"]  # 风力

            string += f"""预报日期：{date}
日间天气状况：{day_zhuangkuang}  夜间天气状况：{night_zhuangkuang}；
日出时间：{sunrise}，日落时间：{sunshut}；月升时间：{moonrise}，月落时间：{moonshut}；
最高温度：{tmp_max}℃，最低温度：{tmp_min}℃，湿度：{shidu}%；
能见度：{nengjiandu}公里，紫外线强度指数为{uv}级；
风速：{fengsu}公里/小时(风力{fengli}级)，风向：{fengxiang}；
当前降水量：{jiangshui}(降水概率：{jiangshuigailv}%)，气压：{qiya}毫安。\n\n"""

        # 删除末尾多出来的两行换行符
        string = "".join(list(string)[:len(string) - 2])
        return string

    def hourly(self, name):
        res = self.get_weather(2, name)
        if res == 1:
            return self.error_meg
        update_time = res["update"]["loc"]
        location = f'{res["basic"]["cnty"]} {res["basic"]["admin_area"]} {res["basic"]["parent_city"]} {res["basic"]["location"]}'
        string = f"""更新时间：{update_time}\n您所查询的地点位于{location}\n\n"""
        for hourly in res["hourly"]:
            time = hourly["time"]  # 预报时间
            tmp = hourly["tmp"]  # 预报气温
            ludian = hourly["dew"]  # 露点温度
            zhuangkuang = hourly["cond_txt"]  # 天气状况
            jiangshuigailv = hourly["pop"]  # 降水概率
            qiya = hourly["pres"]  # 气压
            shidu = hourly["hum"]  # 湿度
            yunliang = hourly["cloud"]  # 云量
            fengxiang = hourly["wind_dir"]  # 风向
            fengsu = hourly["wind_spd"]  # 风速
            fengli = hourly["wind_sc"]  # 风力

            string += f"""预报时间：{time}
预报天气状况：{zhuangkuang}，云量：{yunliang}；
预测温度：{tmp}℃，露点温度：{ludian}℃，湿度：{shidu}%；
风速：{fengsu}公里/小时(风力{fengli}级)，风向：{fengxiang}；
降水概率：{jiangshuigailv}%，气压：{qiya}毫安。\n\n"""

        # 删除末尾多出来的两行换行符
        string = "".join(list(string)[:len(string) - 2])
        return string

    def air_now(self, name):
        res = self.get_weather(4, name)
        if res == 1:
            try:
                res = requests.get(f"https://free-api.heweather.net/s6/weather/now?location={name}&key={self.key}",
                                   headers=self.headers, timeout=5).json()["HeWeather6"][0]
                res = self.get_weather(4, res["basic"]["parent_city"])
                if res == 1:
                    return self.error_meg
            except Exception:
                return self.error_meg
        update_time = res["update"]["loc"]
        location = f'{res["basic"]["cnty"]} {res["basic"]["admin_area"]} {res["basic"]["parent_city"]} {res["basic"]["location"]}'
        string = f"""更新时间：{update_time}\n您所查询的地点位于{location}\n\n"""

        city_now = {}
        city_now["aqi"] = res["air_now_city"]["aqi"]
        city_now["desc"] = res["air_now_city"]["qlty"]
        city_now["pm25"] = res["air_now_city"]["pm25"]
        city_now["pm10"] =res["air_now_city"]["pm10"]
        city_now["no2"] = res["air_now_city"]["no2"]
        city_now["so2"] = res["air_now_city"]["so2"]
        city_now["co"] = res["air_now_city"]["co"]
        city_now["o3"] = res["air_now_city"]["o3"]
        city_now["main"] = "无主要污染物" if res["air_now_city"]["main"]=="-" else res["air_now_city"]["main"]
        city_now["time"] = res["air_now_city"]["pub_time"]

        station = {}
        for info in res["air_now_station"]:
            main = "无主要污染物" if info["main"]=="-" else info["main"]
            station[info["air_sta"]] = {"aqi": info["aqi"], "no2": info["no2"], "o3": info["o3"], "pm10": info["pm10"],
                                        "pm25": info["pm25"], "so2": info["so2"], "desc": info["qlty"],"co": info["co"],
                                        "time": info["pub_time"], "main": main}

        string += f"""当前城市概况（发布时间{city_now['time']}）：
空气质量指数：{city_now['aqi']}({city_now['desc']})，{city_now['main']}
PM2.5浓度为{city_now['pm25']}μg/m3，PM10浓度为{city_now['pm10']}μg/m3
NO2浓度为{city_now['no2']}μg/m3，so2浓度为{city_now['so2']}μg/m3，co浓度为{city_now['co']}μg/m3，o3浓度为{city_now['o3']}μg/m3\n\n"""

        for info in station:
            string += f"""站点“{info}”信息（发布时间{station[info]['time']}）：
空气质量指数：{station[info]['aqi']}({station[info]['desc']})，主要污染物：{station[info]['main']}
PM2.5浓度为{station[info]['pm25']}μg/m3，PM10浓度为{station[info]['pm10']}μg/m3
NO2浓度为{station[info]['no2']}μg/m3，so2浓度为{station[info]['so2']}μg/m3，co浓度为{station[info]['co']}μg/m3，o3浓度为{station[info]['o3']}μg/m3\n\n"""

        # 删除末尾多出来的两行换行符
        string = "".join(list(string)[:len(string) - 2])
        return string

    def debugging(self, name, mode):
        if mode == 1 or mode == 4:
            request_mode = "now"
        elif mode == 2:
            request_mode = "hourly"
        elif mode == 3:
            request_mode = "forecast"
        else:
            return self.error_meg

        if mode != 4:
            url = f"https://free-api.heweather.net/s6/weather/{request_mode}?location={name}&key={self.key}"
        else:
            url = f"https://free-api.heweather.net/s6/air/{request_mode}?location={name}&key={self.key}"
        try:
            res = requests.get(url, headers=self.headers, timeout=5).json()
        except Exception as e:
            res = e
        status = res["HeWeather6"][0]["status"]
        headers = str(self.headers)

        string = f"""请求URL：{url}
请求头：{headers}
请求状态：{status}

响应：{res}"""

        return string