# PyQtWeatherQuerying

这个程序目前经过作者精心调试后可以随时用于各种环境中。

## 技术参数

#### 使用的库

- requests
- PyQt5

#### 安装所使用的库

```cmd
pip install reqeusts
pip install PyQt5
```

或者：

```cmd
py -m pip install requests
py -m pip install PyQt5
```

Tips：PyQt5由于国内网络原因下载速度极慢，建议使用Proxifier+科学上网工具代理`python.exe` `pip.exe`进程下载PyQt5。

## 开发者实时调试代码

通过输入开发者调试代码，可允许开发者直接在应用内直接检测api的返回结果，以确定bug究竟是由什么引起的。

开发者调试代码的一些提示放置在“something.json”文件中，使用

```python
with open("something.json", encoding="UTF-8", mode='r') as file:
    introduction = json.load(file)
```

来从文件中读取数据到**introduction**变量中，使用

```python
import random
random.choice(introduction)
```

来随机选择一条提示语句。

<small><del>开发者由于非常喜爱[WARFRAME](https://warframe.com)，因此将WF的一些东西放进了这个文件里</del></small>

## API key

本程序目前支持和风天气 (www.heweather.com) 与 彩云天气 (caiyunapp.com) 的API进行数据的提供。其在使用时均需要提供API key。

欲配置API key，可在**main.py**的

```python
class App:
    def __init__(self):
        self.hefeng = Hefeng(self.hefeng_editcity, self.debugging, self.weather_info, self.query_time, "Your key here")
        self.caiyun = Caiyun(self.caiyun_editcity, self.debugging, self.weather_info, self.query_time, "Your key here")
```

找到如下片段，并将**“Your key here”**片段替换为您自己的API。

#### 彩云天气Tips

请注意，彩云天气有一个公用API：`TAkhjf8d1nlSlspN`。该API可提供基本数据的供给，但不保证数据7×24实时可用。

## 版本记录

```
V1.1 2019-12-21
提交到GitHub上
```

## 其它

如果有啥好想法请开个issue来跟我说说

要魔改自己拿去