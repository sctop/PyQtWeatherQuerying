import requests
import playsound
from urllib.parse import quote


class BaiduTTS:
    def __init__(self, apikey, apisecret):
        self.key = apikey
        self.secret = apisecret
        self.get_token()

    def get_token(self):
        r = requests.get(
            f"https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.key}&client_secret={self.secret}").json()
        if "audio_tts_post" in str(r["scope"]).split(" "):
            self.token = r["access_token"]

    def get_sound(self, text):
        temp = quote(quote(text))
        r = requests.get(
            f"http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok={self.token}&tex={temp}&vol=9&per=0&spd=5&pit=5&aue=3")
        try:
            error = r.json()["err_msg"]
        except Exception as e:
            with open("sound.mp3", "wb") as file:
                file.write(r.content)
        playsound.playsound("sound.mp3")
BaiduTTS("U7ZYOpNhTM9LF160BioGZefM","AOQSyouhnaqjFYlMptWQM3n3f3AQy6x5").get_sound("你好")
