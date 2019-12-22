import requests
import time


class Caiyunapi:
    def __init__(self, error_msg, token):
        self.error_meg = error_msg
        self.headers = {
            "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
        }
        self.skycon = {
            'CLEAR_DAY': "晴（白天）",
            'CLEAR_NIGHT': "晴（夜间）",
            'PARTLY_CLOUDY_DAY': '多云（白天）',
            'PARTLY_CLOUDY_NIGHT': '多云（夜间）',
            'CLOUDY': '阴',
            'WIND': '大风',
            'HAZE': '雾霾',
            'RAIN': '雨',
            'SNOW': '雪',
            'Unknown': '其它'
        }
        self.comfort = {
            -1: '未知',
            0: '闷热',
            1: '酷热',
            2: '很热',
            3: '热',
            4: '温暖',
            5: '舒适',
            6: '凉爽',
            7: '冷',
            8: '很冷',
            9: '寒冷',
            10: '极冷',
            11: '刺骨的冷',
            12: '湿冷',
            13: '干冷',
        }
        self.token = token

    def get_weather(self, mode, pos):
        if mode == 1:
            request_mode = "realtime"
        elif mode == 2:
            request_mode = "forecast"
        else:
            return 1
        try:
            r = requests.get(
                f"https://api.caiyunapp.com/v2/{self.token}/{pos[0]},{pos[1]}/{request_mode}.json?lang=zh_CN&unit=metric&tzshift=28800")
        except Exception as e:
            print(e)
            return 1
        r.encoding = "UTF-8"
        if r.status_code != 200:
            return 1
        content = r.json()
        if content["status"] == "ok" and content["api_status"] == "active":
            return content
        else:
            return 1

    def realtime(self, pos):
        if type(pos) != list:
            return self.error_meg
        r = self.get_weather(1, pos)
        if r == 1:
            return self.error_meg
        servertime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(r["server_time"])))
        location = r["location"]

        r = r["result"]
        tmp = r["temperature"]
        shidu = int(r["humidity"]) * 100
        yunliang = r["cloudrate"] * 100
        zhuangkuang = self.skycon[r["skycon"]]
        nengjiandu = r["visibility"]
        fengsu = r["wind"]["speed"]
        fengxiang = r["wind"]["direction"]
        qiya = r["pres"] / 100
        tigan = r["apparent_temperature"]
        local_jiangshuiliang = r["precipitation"]["local"]["intensity"]
        nearest_distance = r["precipitation"]["nearest"]["distance"]
        nearest_jiangshuiliang = r["precipitation"]["nearest"]["intensity"]
        ul_level = r["ultraviolet"]["index"]
        comfort = self.comfort[r["comfort"]["index"]]

        aqi = r["aqi"]
        pm25 = r["pm25"]
        pm10 = r["pm10"]
        o3 = r["o3"]
        so2 = r["so2"]
        no2 = r["no2"]
        co = r["co"]

        string = f"""更新时间：{servertime}
查询的经纬度：{location[0]},{location[1]}\n
实时温度：{tmp}℃，体感温度为{tigan}℃，感觉{comfort}；当前湿度为{shidu}
天气状况：{zhuangkuang}，能见度：{nengjiandu}公里，云量：{yunliang}
紫外线强度指数为{ul_level}级
风速：{fengsu}公里/小时，风向{fengxiang}°
本地降水量：{local_jiangshuiliang:0.2f}，气压：{qiya:0.2f}
最近的降雨团距离：{nearest_distance:0.2f}公里，降水量：{nearest_jiangshuiliang:0.2f}
空气质量：{aqi}；PM2.5浓度为{pm25}μg/m3，PM10浓度为{pm10}μg/m3，o3浓度为{o3}μg/m3，so2浓度为{so2}μg/m3，no2浓度为{no2}μg/m3，co浓度为{co}μg/m3
"""
        return string

    def forecast_2hour(self, pos):
        if type(pos) != list:
            return self.error_meg
        r = self.get_weather(2, pos)
        if r == 1:
            return self.error_meg
        servertime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(r["server_time"])))
        location = r["location"]

        # 两小时内下雨概率
        minutely = r["result"]["minutely"]
        minutely_string = f"""更新时间：{servertime}
查询的经纬度：{location[0]}, {location[1]}\n
两小时降雨预报：
总体概况：{minutely['description']}
未来0.5小时概率：{minutely['probability'][0]}；未来1小时概率：{minutely['probability'][1]}；未来1.5小时概率：{minutely['probability'][2]}；未来2小时概率：{minutely['probability'][3]}"""
        return minutely_string

    def forecast_hourly(self, pos):
        if type(pos) != list:
            return self.error_meg
        r = self.get_weather(2, pos)
        if r == 1:
            return self.error_meg
        servertime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(r["server_time"])))
        location = r["location"]
        # 逐小时预报
        hourly = r["result"]["hourly"]
        total_24 = hourly["description"]
        string = f"更新时间：{servertime}\n查询的经纬度：{location[0]}, {location[1]}\n大致情况：{total_24}\n\n"
        data = {}
        for jiangshuiliang in hourly["precipitation"]:  # 降水量
            if jiangshuiliang["datetime"] not in data.keys():
                data[jiangshuiliang["datetime"]] = {"jiangshuiliang": jiangshuiliang["value"]}
            else:
                data[jiangshuiliang["datetime"]]["jiangshuiliang"] = jiangshuiliang["value"]
        for tmp in hourly["temperature"]:  # 温度
            data[tmp["datetime"]]["tmp"] = tmp["value"]
        for wind in hourly["wind"]:  # 风速风向
            data[wind["datetime"]]["wind_speed"] = wind["speed"]
            data[wind["datetime"]]["wind_direction"] = wind["direction"]
        for shidu in hourly["humidity"]:
            data[shidu["datetime"]]["shidu"] = shidu["value"] * 100
        for yunliang in hourly["cloudrate"]:
            data[yunliang["datetime"]]["yunliang"] = yunliang["value"] * 100
        for zhuangkuang in hourly["skycon"]:
            data[zhuangkuang["datetime"]]["zhuangkuang"] = self.skycon[zhuangkuang["value"]]
        for qiya in hourly["pres"]:
            data[qiya["datetime"]]["qiya"] = qiya["value"] / 100
        for nengjiandu in hourly["visibility"]:
            data[nengjiandu["datetime"]]["nengjiandu"] = nengjiandu["value"]
        for aqi in hourly["aqi"]:
            data[aqi["datetime"]]["aqi"] = aqi["value"]
        for pm25 in hourly["pm25"]:
            data[pm25["datetime"]]["pm25"] = pm25["value"]
        for info in data:
            string += f"""预报天气：{info}
预报天气状况：{data[info]["zhuangkuang"]}，云量：{data[info]["yunliang"]:0.2f}
温度：{data[info]["tmp"]}℃，湿度：{data[info]["shidu"]:0.2f}%
能见度：{data[info]["nengjiandu"]}公里；空气质量：{data[info]["aqi"]}，PM2.5浓度为{data[info]["pm25"]}μg/m3
风速：{data[info]["wind_speed"]}公里/小时，风向：{data[info]["wind_direction"]}°
降水量：{data[info]["jiangshuiliang"]}，气压：{data[info]["qiya"]:0.2f}\n\n"""

        # 删除末尾多出来的两行换行符
        string = "".join(list(string)[:len(string) - 2])
        return string

    def forecast_daily(self, pos):
        if type(pos) != list:
            return self.error_meg
        r = self.get_weather(2, pos)
        if r == 1:
            return self.error_meg
        servertime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(r["server_time"])))
        location = r["location"]
        string = f"更新时间：{servertime}\n查询的经纬度：{location[0]}, {location[1]}\n\n"
        data = {}

        r = r["result"]["daily"]
        for suninfo in r["astro"]:
            if suninfo["date"] not in data.keys():
                data[suninfo["date"]] = {"sunrise": suninfo["sunrise"]["time"], "sunset": suninfo["sunset"]["time"]}
            else:
                data[suninfo["date"]]["sunrise"] = suninfo["sunrise"]["time"]
                data[suninfo["date"]]["sunset"] = suninfo["sunset"]["time"]
        for jiangshuiliang in r["precipitation"]:
            data[jiangshuiliang["date"]]["jiangshui_max"] = jiangshuiliang["max"]
            data[jiangshuiliang["date"]]["jiangshui_min"] = jiangshuiliang["min"]
            data[jiangshuiliang["date"]]["jiangshui_avg"] = jiangshuiliang["avg"]
        for tmp in r["temperature"]:
            data[tmp["date"]]["tmp_max"] = tmp["max"]
            data[tmp["date"]]["tmp_min"] = tmp["min"]
            data[tmp["date"]]["tmp_avg"] = tmp["avg"]
        for wind in r["wind"]:
            data[wind["date"]]["wind_max_spd"] = wind["max"]["speed"]
            data[wind["date"]]["wind_max_dir"] = wind["max"]["direction"]
            data[wind["date"]]["wind_min_spd"] = wind["min"]["speed"]
            data[wind["date"]]["wind_min_dir"] = wind["min"]["direction"]
        for shidu in r["humidity"]:
            data[shidu["date"]]["hum_max"] = shidu["max"] * 100
            data[shidu["date"]]["hum_min"] = shidu["min"] * 100
            data[shidu["date"]]["hum_avg"] = shidu["avg"] * 100
        for cloudrate in r["cloudrate"]:
            data[cloudrate["date"]]["cloud_max"] = cloudrate["max"] * 100
            data[cloudrate["date"]]["cloud_min"] = cloudrate["min"] * 100
            data[cloudrate["date"]]["cloud_avg"] = cloudrate["avg"] * 100
        for pres in r["pres"]:
            data[pres["date"]]["pres_max"] = pres["max"] / 100
            data[pres["date"]]["pres_min"] = pres["min"] / 100
            data[pres["date"]]["pres_avg"] = pres["avg"] / 100
        for nengjiandu in r["visibility"]:
            data[nengjiandu["date"]]["vis_max"] = nengjiandu["max"]
            data[nengjiandu["date"]]["vis_min"] = nengjiandu["min"]
            data[nengjiandu["date"]]["vis_avg"] = nengjiandu["avg"]
        for aqi in r["aqi"]:
            data[aqi["date"]]["aqi_max"] = aqi["max"]
            data[aqi["date"]]["aqi_min"] = aqi["min"]
            data[aqi["date"]]["aqi_avg"] = aqi["avg"]
        for pm25 in r["pm25"]:
            data[pm25["date"]]["pm25_max"] = pm25["max"]
            data[pm25["date"]]["pm25_min"] = pm25["min"]
            data[pm25["date"]]["pm25_avg"] = pm25["avg"]
        for day_con in r["skycon_08h_20h"]:
            data[day_con["date"]]["day_con"] = self.skycon[day_con["value"]]
        for night_con in r["skycon_20h_32h"]:
            data[night_con["date"]]["night_con"] = self.skycon[night_con["value"]]
        for comfort in r["comfort"]:
            data[comfort["datetime"]]["comfort"] = self.comfort[int(comfort["index"])]
        for ul in r["ultraviolet"]:
            data[ul["datetime"]]["ul_index"] = ul["index"]
            data[ul["datetime"]]["ul_desc"] = ul["desc"]

        for info in data:
            string += f"""预报天气：{info}
日间天气状况：{data[info]["day_con"]} 夜间天气状况：{data[info]["night_con"]}
日出时间：{data[info]["sunrise"]}，日落时间：{data[info]["sunset"]}
最高温度：{data[info]["tmp_max"]}℃，最低温度：{data[info]["tmp_min"]}℃，平均温度：{data[info]["tmp_avg"]}℃；感觉{data[info]["comfort"]}
最高能见度：{data[info]["vis_max"]}公里，最低能见度：{data[info]["vis_min"]}公里，平均能见度：{data[info]["vis_avg"]}公里
紫外线强度指数为{data[info]["ul_index"]}级（{data[info]["ul_desc"]}）
当日降水量：{data[info]["jiangshui_min"]:0.2f}~{data[info]["jiangshui_max"]:0.2f}(平均降水量：{data[info]["jiangshui_avg"]:0.2f})
当日湿度：{data[info]["hum_min"]:0.2f}%~{data[info]["hum_max"]:0.2f}%(平均湿度：{data[info]["hum_avg"]})
当日云量：{data[info]["cloud_min"]:0.2f}~{data[info]["cloud_max"]:0.2f}(平均云量：{data[info]["cloud_avg"]:0.2f})
当日气压：{data[info]["pres_min"]:0.2f}~{data[info]["pres_max"]:0.2f}(平均气压：{data[info]["pres_avg"]:0.2f})
最低风速：{data[info]["wind_min_spd"]}公里/小时({data[info]["wind_min_dir"]}°)，最高风速：{data[info]["wind_max_spd"]}公里/小时({data[info]["wind_max_dir"]}°)
空气质量：{data[info]["aqi_min"]}μg/m3~{data[info]["aqi_max"]}μg/m3（平均：{data[info]["aqi_avg"]}μg/m3）
PM2.5浓度：{data[info]["pm25_min"]}μg/m3~{data[info]["pm25_max"]}μg/m3（平均：{data[info]["pm25_avg"]:0.2f}μg/m3）\n\n"""
        # 删除末尾多出来的两行换行符
        string = "".join(list(string)[:len(string) - 2])
        return string

    def debugging(self, pos, mode):
        if mode == 1:
            request_mode = "realtime"
        elif mode == 2:
            request_mode = "forecast"
        else:
            return self.error_meg
        url = f"https://api.caiyunapp.com/v2/{self.token}/{pos[0]},{pos[1]}/{request_mode}.json?lang=zh_CN&unit=metric&tzshift=28800"
        try:
            res = requests.get(url, timeout=5).json()
        except Exception as e:
            res = e
        status = res["status"]

        string = f"""请求URL：{url}
请求头：Python Requests默认请求头
请求状态：{status}

响应：{res}"""
        return string
