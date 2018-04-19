#-*- coding:utf-8 -*-
import twitter
import threading
import datetime
import urllib
import json
from get_data import GetData

#설정 불러오기
f = open('information.json','r')
settings = json.loads(f.read())

# API설정
api = twitter.Api(consumer_key=settings["consumer_key"],
                  consumer_secret=settings["consumer_secret"],
                  access_token_key=settings["access_token_key"],
                  access_token_secret=settings["access_token_secret"])

# 지역설정
top = settings["top"]
mdl = settings["mdl"]
leaf = settings["leaf"]
service_key = settings["service_key"]

# 강수형태
pty = ['なし','雨','雨/雪','雪']

f.close()

class Task:

    # 트윗 형태
    template = "#Prokumaの地元天気BOT\n\n今の地元の天気\n地元：{}\n気温：{}\n降水形態：{}\n風速：{}\n\n基準日付：{}\n基準時刻：{}"

    time = "" # 이전시간

    refresh_time = 3600 # 갱신시간 : 1시간
    weather_dictionary = {} # 날씨정보 저장

    def __init__(self):
        pass

    def weatherTask(self):
        data = GetData(top, mdl, leaf, service_key)
        # 기상청으로부터 지역의 X, Y좌표를 획득
        data.setRegion()
        # 기상청에서 요구하는 형태의 날짜와 시간 문자열 설정
        date, time = self.timeString()
        data.setTime(date, time)
        # 정보수집
        weather = data.getData()
        # 딕셔너리에 정보 저장
        for i in weather['response']['body']['items']['item']:
            self.weather_dictionary[i['category']] = i['obsrValue']

        if time != self.time:
            # 템플릿에 정보 대입
            post = self.template.format(str(settings["region"]),str(self.weather_dictionary['T1H']) + "°C",
             pty[self.weather_dictionary['PTY']], 
            str(self.weather_dictionary['WSD']) + "m/s", str(date), str(time))

            # 투고
            api.PostUpdate(post)
            #시간 갱신
            self.time = time
        threading.Timer(self.refresh_time, self.weatherTask).start()

    # 기상청에서 요구하는 형태로 현재시각을 알려주는 함수
    def timeString(self):
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        time = int(now.strftime('%H'))
        time_string = str(time) + "00"
        if len(time_string) < 4:
            time_string = "0" + time_string
        return date, time_string

def main():
    task = Task()
    task.weatherTask()

if __name__ == '__main__':
    main()